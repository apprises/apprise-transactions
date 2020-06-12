import json
from datetime import datetime
from decimal import Decimal
from ..exceptions import NoRawTXData
from unittest import TestCase
from unittest.mock import MagicMock, patch
from xml.dom.minidom import parseString

from dicttoxml import dicttoxml

from apprisetransactions import settings
from apprisetransactions.transactions import MoneroTransaction


class TestCase_Notify(TestCase):
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

    def setUp(self):
        settings.init()
        self.transaction = MoneroTransaction(
            tx_id="4ea70add5d0c7db33557551b15cd174972fcfc73bf0f6a6b47b7837564b708d3",
            payment_provider="Monero",
            amount=Decimal("4.000000000000"),
            fee=Decimal("0.000962550000"),
            note="",
            recipient="9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNCUukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC",
            timestamp=datetime(2018, 1, 29, 13, 17, 18),
            confirmations=1,
            _raw_data=self.raw_data,
        )

    @patch("apprisetransactions.transactions.transaction.Apprise")
    def test_notify_json(self, mock_apprise):
        def notify_json_sideeffect(json_body):
            self.assertEqual(json_body, json.dumps(self.raw_data))
            return True

        mock_apprise.notify = MagicMock(side_effect=notify_json_sideeffect)
        mock_apprise.return_value = mock_apprise
        self.assertTrue(self.transaction.notify(urls=["json://blah", "sns://blah"]))
        self.assertEqual(mock_apprise.notify.call_count, 1)

    def test_notify_exception(self):

        with self.assertRaises(NoRawTXData):
            MoneroTransaction(tx_id="txexample").notify(
                urls=["json://blah", "sns://blah"]
            )

        with self.assertRaises(NoRawTXData):
            MoneroTransaction(tx_id="txexample").notify(urls=["xml://blah"])

    @patch("apprisetransactions.transactions.transaction.Apprise")
    def test_notify_xml(self, mock_apprise):
        def notify_xml_sideeffect(xml_body):
            self.assertEqual(
                xml_body, parseString(dicttoxml(self.raw_data)).toprettyxml()
            )
            return True

        mock_apprise.notify = MagicMock(side_effect=notify_xml_sideeffect)
        mock_apprise.return_value = mock_apprise
        self.assertTrue(self.transaction.notify(urls=["xml://blah"]))
        self.assertEqual(mock_apprise.notify.call_count, 1)

    @patch("apprisetransactions.transactions.transaction.Apprise")
    def test_notify_other(self, mock_apprise):
        pass

        def notify_sideeffect(body, title, attach):
            self.assertEqual(body, "New XMR received")
            self.assertEqual(title, "Private Notification")
            return True

        mock_apprise.notify = MagicMock(side_effect=notify_sideeffect)
        mock_apprise.return_value = mock_apprise
        self.assertTrue(
            self.transaction.notify(
                urls=["pbul://asdfasdf"],
                body="New {currency} received",
                title="Private Notification",
            )
        )
        self.assertEqual(mock_apprise.notify.call_count, 1)

    @patch("apprisetransactions.transactions.transaction.parse_placeholders")
    @patch("apprisetransactions.transactions.transaction.Apprise")
    def test_znotify_other(self, mock_apprise, mock_parse_placeholders):
        def notify_sideeffect(body, title, attach):
            self.assertEqual(body, "New XMR received")
            self.assertEqual(title, "Private Notification")
            return True

        # prase_placeholders is tested in test_utils
        mock_parse_placeholders.return_value = (
            "New XMR received",
            "Private Notification",
        )
        mock_apprise.notify = MagicMock(side_effect=notify_sideeffect)
        mock_apprise.return_value = mock_apprise
        self.assertTrue(
            self.transaction.notify(
                urls=["pbul://asdfasdf"],
                body="New {currency} received",
                title="Private Notification",
            )
        )
        self.assertEqual(mock_apprise.notify.call_count, 1)
        self.assertEqual(mock_parse_placeholders.call_count, 1)
