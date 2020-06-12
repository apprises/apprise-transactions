from datetime import datetime
from decimal import Decimal
from ..exceptions import NoTXFound, NoTXToProcess, NumConfirmationsNotMet
from unittest import TestCase
from unittest.mock import MagicMock, patch

from monero.account import Account
from monero.address import address
from monero.numbers import PaymentID
from monero.transaction import IncomingPayment, Transaction

from apprisetransactions import settings
from apprisetransactions.configuration import ServerConfig
from apprisetransactions.transactions import MoneroTransaction


class TestCase_MoneroTX(TestCase):
    raw_data = {
        "transfer": {
            "address": "599BXkvzAPeD6EojXjW99gGeE19rxuS4g99o5xevp3jTFQYTNtSyYtqWAt2jg9MTP8aLTJKiuCJXg1Ro6xLtEUEm9rWHL7V",
            "amount": 100000000,
            "amounts": [100000000],
            "confirmations": 21,
            "double_spend_seen": False,
            "fee": 1006740000,
            "height": 597061,
            "locked": False,
            "note": "",
            "payment_id": "0000000000000000",
            "subaddr_index": {"major": 0, "minor": 0},
            "subaddr_indices": [{"major": 0, "minor": 0}],
            "suggested_confirmations_threshold": 1,
            "timestamp": 1591546700,
            "txid": "d0fb667f2975f79495e973d1437200f7b6c464956d33cd89289411e07a8c0b3a",
            "type": "in",
            "unlock_time": 0,
        },
        "transfers": [
            {
                "address": "599BXkvzAPeD6EojXjW99gGeE19rxuS4g99o5xevp3jTFQYTNtSyYtqWAt2jg9MTP8aLTJKiuCJXg1Ro6xLtEUEm9rWHL7V",
                "amount": 100000000,
                "amounts": [100000000],
                "confirmations": 21,
                "double_spend_seen": False,
                "fee": 1006740000,
                "height": 597061,
                "locked": False,
                "note": "",
                "payment_id": "0000000000000000",
                "subaddr_index": {"major": 0, "minor": 0},
                "subaddr_indices": [{"major": 0, "minor": 0}],
                "suggested_confirmations_threshold": 1,
                "timestamp": 1591546700,
                "txid": "d0fb667f2975f79495e973d1437200f7b6c464956d33cd89289411e07a8c0b3a",
                "type": "in",
                "unlock_time": 0,
            }
        ],
    }

    class MockBackend(object):
        def __init__(self):
            self.transfers = []
            tx = Transaction(
                timestamp=datetime(2018, 1, 29, 15, 0, 25),
                height=1087606,
                hash="a0b876ebcf7c1d499712d84cedec836f9d50b608bb22d6cb49fd2feae3ffed14",
                fee=Decimal("0.00352891"),
            )
            pm = IncomingPayment(
                amount=Decimal("1"),
                local_address=address(
                    "Bf6ngv7q2TBWup13nEm9AjZ36gLE6i4QCaZ7XScZUKDUeGbYEHmPRdegKGwLT8tBBK7P6L32RELNzCR6QzNFkmogDjvypyV"
                ),
                payment_id=PaymentID(
                    "0166d8da6c0045c51273dd65d6f63734beb8a84e0545a185b2cfd053fced9f5d"
                ),
                transaction=tx,
            )
            self.transfers.append(pm)
            tx = Transaction(
                timestamp=datetime(2018, 1, 29, 14, 57, 47),
                height=1087601,
                hash="f34b495cec77822a70f829ec8a5a7f1e727128d62e6b1438e9cb7799654d610e",
                fee=Decimal("0.008661870000"),
            )
            pm = IncomingPayment(
                amount=Decimal("3.000000000000"),
                local_address=address(
                    "BhE3cQvB7VF2uuXcpXp28Wbadez6GgjypdRS1F1Mzqn8Advd6q8VfaX8ZoEDobjejrMfpHeNXoX8MjY8q8prW1PEALgr1En"
                ),
                payment_id=PaymentID("f75ad90e25d71a12"),
                transaction=tx,
            )
            self.transfers.append(pm)
            tx = Transaction(
                timestamp=datetime(2018, 1, 29, 13, 17, 18),
                height=1087530,
                hash="5c3ab739346e9d98d38dc7b8d36a4b7b1e4b6a16276946485a69797dbf887cd8",
                fee=Decimal("0.000962550000"),
            )
            pm = IncomingPayment(
                amount=Decimal("10.000000000000"),
                local_address=address(
                    "9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC"
                ),
                payment_id=PaymentID("f75ad90e25d71a12"),
                transaction=tx,
            )
            self.transfers.append(pm)
            tx = Transaction(
                timestamp=datetime(2018, 1, 29, 13, 17, 18),
                height=1087608,
                hash="4ea70add5d0c7db33557551b15cd174972fcfc73bf0f6a6b47b7837564b708d3",
                fee=Decimal("0.000962550000"),
                confirmations=1,
            )
            pm = IncomingPayment(
                amount=Decimal("4.000000000000"),
                local_address=address(
                    "9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC"
                ),
                payment_id=PaymentID("f75ad90e25d71a12"),
                transaction=tx,
            )
            self.transfers.append(pm)
            tx = Transaction(
                timestamp=datetime(2018, 1, 29, 13, 17, 18),
                height=1087530,
                hash="e9a71c01875bec20812f71d155bfabf42024fde3ec82475562b817dcc8cbf8dc",
                fee=Decimal("0.000962550000"),
            )
            pm = IncomingPayment(
                amount=Decimal("2.120000000000"),
                local_address=address(
                    "9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC"
                ),
                payment_id=PaymentID("cb248105ea6a9189"),
                transaction=tx,
            )
            self.transfers.append(pm)
            tx = Transaction(
                timestamp=datetime(2018, 1, 29, 14, 57, 47),
                height=1087601,
                hash="5ef7ead6a041101ed326568fbb59c128403cba46076c3f353cd110d969dac808",
                fee=Decimal("0.000962430000"),
            )
            pm = IncomingPayment(
                amount=Decimal("7.000000000000"),
                local_address=address(
                    "BhE3cQvB7VF2uuXcpXp28Wbadez6GgjypdRS1F1Mzqn8Advd6q8VfaX8ZoEDobjejrMfpHeNXoX8MjY8q8prW1PEALgr1En"
                ),
                payment_id=PaymentID("0000000000000000"),
                transaction=tx,
            )
            self.transfers.append(pm)
            tx = Transaction(
                timestamp=datetime(2018, 1, 29, 13, 17, 18),
                height=1087606,
                hash="cc44568337a186c2e1ccc080b43b4ae9db26a07b7afd7edeed60ce2fc4a6477f",
                fee=Decimal("0.000962550000"),
            )
            pm = IncomingPayment(
                amount=Decimal("10.000000000000"),
                local_address=address(
                    "9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC"
                ),
                payment_id=PaymentID("0000000000000000"),
                transaction=tx,
            )
            self.transfers.append(pm)
            tx = Transaction(
                timestamp=datetime(2018, 1, 29, 21, 13, 28),
                height=None,
                hash="d29264ad317e8fdb55ea04484c00420430c35be7b3fe6dd663f99aebf41a786c",
                fee=Decimal("0.000961950000"),
            )
            pm = IncomingPayment(
                amount=Decimal("3.140000000000"),
                local_address=address(
                    "9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC"
                ),
                payment_id=PaymentID("03f6649304ea4cb2"),
                transaction=tx,
            )
            self.transfers.append(pm)

        def height(self):
            return 1087607

        def accounts(self):
            return [Account(self, 0)]

        def transfers_in(self, account, pmtfilter):
            return list(pmtfilter.filter(self.transfers))

    @patch("apprisetransactions.transactions.monero_transaction.JSONRPCWallet")
    def test_set_transaction_data(self, mock_backend):
        transaction: MoneroTransaction = MoneroTransaction(
            tx_id="a0b876ebcf7c1d499712d84cedec836f9d50b608bb22d6cb49fd2feae3ffed14",
            server_config=ServerConfig(config_file=None),
        )
        settings.security_level = 1
        mock_backend.side_effect = self.MockBackend
        transaction.set_transaction_data(get_raw_data=False)

        self.assertEqual(
            transaction.tx_id,
            "a0b876ebcf7c1d499712d84cedec836f9d50b608bb22d6cb49fd2feae3ffed14",
        )
        self.assertEqual(transaction.currency, "XMR")
        # no payment provider because we didn't go through the factory
        self.assertEqual(transaction.payment_provider, None)
        self.assertEqual(transaction.amount, Decimal("1"))
        self.assertEqual(transaction.fee, Decimal("0.00352891"))
        self.assertEqual(transaction.note, "")
        self.assertEqual(
            transaction.recipient,
            "Bf6ngv7q2TBWup13nEm9AjZ36gLE6i4QCaZ7XScZUKD"
            "UeGbYEHmPRdegKGwLT8tBBK7P6L32RELNzCR6QzNFkmogDjvypyV",
        )
        self.assertEqual(transaction.timestamp, datetime(2018, 1, 29, 15, 0, 25))
        self.assertEqual(transaction.confirmations, 0)

    @patch("apprisetransactions.transactions.monero_transaction.JSONRPCWallet")
    def test_set_transaction_data_mem_pool(self, mock_backend):
        transaction: MoneroTransaction = MoneroTransaction(
            tx_id="d29264ad317e8fdb55ea04484c00420430c35be7b3fe6dd663f99aebf41a786c",
            server_config=ServerConfig(config_file=None),
        )
        settings.security_level = 0
        mock_backend.side_effect = self.MockBackend
        transaction.set_transaction_data(get_raw_data=False)

        self.assertEqual(
            transaction.tx_id,
            "d29264ad317e8fdb55ea04484c00420430c35be7b3fe6dd663f99aebf41a786c",
        )
        self.assertEqual(transaction.currency, "XMR")
        # no payment provider because we didn't go through the factory
        self.assertEqual(transaction.payment_provider, None)
        self.assertEqual(transaction.amount, Decimal("3.140000000000"))
        self.assertEqual(transaction.fee, Decimal("0.000961950000"))
        self.assertEqual(transaction.note, "")
        self.assertEqual(
            transaction.recipient,
            "9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC",
        )
        self.assertEqual(transaction.timestamp, datetime(2018, 1, 29, 21, 13, 28))
        self.assertEqual(transaction.confirmations, 0)

    @patch("apprisetransactions.transactions.monero_transaction.JSONRPCWallet")
    def test_set_transaction_data_exception_numconfirmations(self, mock_backend):
        transaction: MoneroTransaction = MoneroTransaction(
            tx_id="4ea70add5d0c7db33557551b15cd174972fcfc73bf0f6a6b47b7837564b708d3",
            server_config=ServerConfig(config_file=None),
        )
        settings.security_level = 2
        mock_backend.side_effect = self.MockBackend
        with self.assertRaises(NumConfirmationsNotMet):
            transaction.set_transaction_data(get_raw_data=False)

    @patch("apprisetransactions.transactions.monero_transaction.Wallet")
    @patch("apprisetransactions.transactions.monero_transaction.JSONRPCWallet")
    def test_get_tx_data_exceptions(self, mock_backend, mock_wallet):
        transaction: MoneroTransaction = MoneroTransaction(
            tx_id="not_there", server_config=ServerConfig(config_file=None)
        )
        settings.security_level = -1
        mock_backend.return_value = MagicMock()
        mock_wallet.return_value.incoming.return_value = []
        with self.assertRaises(NoTXFound):
            transaction.set_transaction_data(get_raw_data=False)

    @patch("apprisetransactions.transactions.monero_transaction.JSONRPCWallet")
    def test_get_tx_data_exception_notxtoprocess(self, mock_backend):
        settings.security_level = 0
        # tx in_block, not in mem pool
        transaction: MoneroTransaction = MoneroTransaction(
            tx_id="a0b876ebcf7c1d499712d84cedec836f9d50b608bb22d6cb49fd2feae3ffed14",
            server_config=ServerConfig(config_file=None),
        )
        mock_backend.side_effect = self.MockBackend
        with self.assertRaises(NoTXToProcess):
            transaction.set_transaction_data(get_raw_data=False)

    @patch("apprisetransactions.transactions.monero_transaction.JSONRPCWallet")
    def test_set_raw_transaction_data(self, mock_backend):
        transaction: MoneroTransaction = MoneroTransaction(
            tx_id="d0fb667f2975f79495e973d1437200f7b6c464956d33cd89289411e07a8c0b3a",
            server_config=ServerConfig(config_file=None),
        )
        mock_backend.return_value.raw_request.return_value = self.raw_data
        transaction.set_transaction_data(get_raw_data=True)
        self.assertEqual(transaction._raw_data, self.raw_data)
