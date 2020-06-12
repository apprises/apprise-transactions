import logging
from ..exceptions import NoTXFound, NoTXToProcess, NumConfirmationsNotMet

from requests.exceptions import HTTPError
from urllib3.exceptions import NewConnectionError

from ..configuration import ServerConfig
from ..factories.transaction_factory import TransactionFactory
from ..transactions.monero_transaction import MoneroTransaction


class MoneroFactory(TransactionFactory):
    payment_provider = "Monero"
    server_config: ServerConfig = None

    # you would specify no_data is True when you only care
    # about the fact that a transaction has been received
    # and you don't care about the details of that transaction
    def get_transaction(
        self, tx_id: str, get_tx_data: bool, get_raw_data: bool = False
    ) -> MoneroTransaction:
        tx = MoneroTransaction(
            server_config=self.server_config,
            tx_id=tx_id,
            payment_provider=self.payment_provider,
        )

        if get_tx_data is True:
            try:
                tx.set_transaction_data(get_raw_data=get_raw_data)
            except (
                NumConfirmationsNotMet,
                NoTXFound,
                NewConnectionError,
                HTTPError,
            ) as ne:
                logging.warning(ne)
                exit(1)
            except NoTXToProcess as e:
                logging.info(e)
                exit(1)

        return tx
