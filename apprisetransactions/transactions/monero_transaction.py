from ..transactions.transaction import Transaction
from monero.wallet import Wallet
from monero.backends.jsonrpc import JSONRPCWallet
from .. import settings
import backoff
from requests.exceptions import HTTPError
from urllib3.exceptions import ConnectionError
from ..backoff_hdlrs import (
    backoff_confirmations_hdlr,
    backoff_connection_hdlr,
    backoff_http_hdlr,
)
from monero.transaction import IncomingPayment
from ..exceptions.tx_exceptions import NoTXFound, NumConfirmationsNotMet, NoTXToProcess


def look_up_max_time() -> int:
    return settings.security_level * 600


# This object shouldn't be used directly, use it's associated factory to generate
class MoneroTransaction(Transaction):
    currency = "XMR"

    def __init__(self, tx_id: str, **kwargs):
        super().__init__(tx_id=tx_id, currency=self.currency, **kwargs)

    @backoff.on_exception(
        backoff.constant, HTTPError, max_time=60, on_backoff=backoff_http_hdlr
    )
    @backoff.on_exception(
        backoff.expo, ConnectionError, max_time=60, on_backoff=backoff_connection_hdlr,
    )
    @backoff.on_exception(
        backoff.constant,
        NumConfirmationsNotMet,
        max_time=look_up_max_time,
        interval=250,
        on_backoff=backoff_confirmations_hdlr,
    )
    # flake8: noqa: C901
    def set_transaction_data(self, get_raw_data: bool = False):
        if self.server_config.default is True:
            jsonrpcwallet = JSONRPCWallet()
        else:
            jsonrpcwallet = JSONRPCWallet(
                protocol=self.server_config.protocol,
                host=self.server_config.host,
                port=self.server_config.port,
                path=self.server_config.path,
                user=self.server_config.user,
                password=self.server_config.password,
            )

        try:
            wallet = Wallet(jsonrpcwallet)
        except Exception as e:
            # for some reason connection error isn't being caught
            if e.__class__.__name__ == "ConnectionError":
                raise ConnectionError
            else:
                raise e

        this_payment = None
        if settings.security_level == 0 or settings.security_level == -1:
            # get transaction in mem_pool
            incoming_payment = wallet.incoming(tx_id=self.tx_id, unconfirmed=True, confirmed=False)
            # https://github.com/monero-ecosystem/monero-python/issues/65
            if incoming_payment:
                tx_in_mem_pool = True
                this_payment: IncomingPayment = incoming_payment.pop()
            else:
                tx_in_mem_pool = False

            if tx_in_mem_pool is False and settings.security_level == 0:
                # raising, because we weren't able to find anything in the mem_pool
                # and security_level=0, which means that we only care about tx's in the mem_pool
                raise NoTXToProcess(
                    f"PaymentProvider: {self.payment_provider} TXID: {self.tx_id} "
                    "Status: No transaction found in mem_pool. "
                    "Your tx probably was processed and has been added to a block. "
                    "This is fine. "
                    f" Security_Level: {settings.security_level} "
                    "Action: Nothing"
                )

        if settings.security_level >= 1 or (
            settings.security_level == -1 and this_payment is None
        ):
            incoming_payments = wallet.incoming(tx_id=self.tx_id)
            if incoming_payments == []:
                raise NoTXFound(
                    f"Currency: {self.currency} TXID: {self.tx_id} "
                    "Status: No transaction found. Your tx probably hasn't been added to a block yet. "
                    "This is fine. "
                    f"Another notification will execute. Action: Nothing"
                )
            this_payment: IncomingPayment = incoming_payments[0]
            if settings.security_level > 1:

                if this_payment.transaction.confirmations < settings.security_level:
                    raise NumConfirmationsNotMet(
                        f"Currency: {self.currency} TXID: {self.tx_id} "
                        f"Confirmations: current {this_payment.transaction.confirmations}, "
                        f"expected {settings.security_level}"
                    )

        self.amount = this_payment.amount
        self.fee = this_payment.transaction.fee
        self.note = this_payment.note
        self.recipient = this_payment.local_address
        self.timestamp = this_payment.transaction.timestamp
        # if the tx is in the mem_pool confirmations will be null, set it to 0 instead
        self.confirmations = (
            this_payment.transaction.confirmations
            if this_payment.transaction.confirmations is not None
            else 0
        )

        if get_raw_data is True:
            self._raw_data = jsonrpcwallet.raw_request(
                "get_transfer_by_txid", {"txid": self.tx_id}
            )
