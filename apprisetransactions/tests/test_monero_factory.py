from unittest import TestCase

from apprisetransactions.factories import MoneroFactory
from apprisetransactions.transactions import MoneroTransaction


class TestCase_MoneroFactory(TestCase):
    def setUp(self) -> None:
        self.monero_factory = MoneroFactory(server_config_file=None)

    def test_instantiation(self):
        self.assertTrue(self.monero_factory.server_config.default)
        self.assertEqual(MoneroFactory, type(self.monero_factory))
        self.assertIsNot(
            Exception,
            type(
                self.monero_factory.get_transaction(
                    tx_id="", get_tx_data=False, get_raw_data=True
                )
            ),
        )

    def test_get_transaction(self):
        transaction = self.monero_factory.get_transaction(
            tx_id="test", get_tx_data=False, get_raw_data=False
        )
        self.assertEqual(MoneroTransaction, type(transaction))
