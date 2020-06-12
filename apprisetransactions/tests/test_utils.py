from datetime import datetime
from decimal import Decimal
from ..exceptions import ExchangeRateDataError
from unittest import TestCase
from unittest.mock import MagicMock, patch

from apprisetransactions import settings, utils
from apprisetransactions.transactions import MoneroTransaction
from apprisetransactions.utils import currency_converter, parse_placeholders


class TestCase_Utils(TestCase):
    amount_in_usd_result = {
        "Response": "Success",
        "Type": 100,
        "Aggregated": False,
        "Data": [
            {
                "time": 1517245200,
                "close": 317.22,
                "high": 318.22,
                "low": 315.85,
                "open": 317.88,
                "volumefrom": 480.8,
                "volumeto": 152627.25,
            },
            {
                "time": 1517248800,
                "close": 318.49,
                "high": 318.79,
                "low": 316.04,
                "open": 317.22,
                "volumefrom": 965.1,
                "volumeto": 306274.66,
            },
        ],
        "TimeTo": 1517248800,
        "TimeFrom": 1517245200,
        "FirstValueInArray": True,
        "ConversionType": {"type": "direct", "conversionSymbol": ""},
        "RateLimit": {},
        "HasWarning": False,
    }
    amount_in_error = {
        "Response": "Error",
        "Message": "There is no data for the toSymbol PWD .",
        "HasWarning": False,
        "Type": 2,
        "RateLimit": {},
        "Data": {},
        "ParamWithError": "tsym",
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
        )

    def test_parse_placeholders(self):
        # simple
        body = "Check%20your%20wallet%20for%20more%20details"
        title = "New%20%7Bcurrency%7D%20received"
        title_expected = "New XMR received"
        body_expected = "Check your wallet for more details"
        body_after, title_after = parse_placeholders(self.transaction, body, title)
        self.assertEqual(body_after, body_expected)
        self.assertEqual(title_after, title_expected)

        # all transaction attributes
        body = "tx_id%3A%7Btx_id%7D%2Cpayment_provider" \
               "%3A%7Bpayment_provider%7D%2Camount%3A%7B" \
               "amount%7D%2Cfee%3A%7Bfee%7D"
        title = "note%3A%7Bnote%7D%2Crecipient%3A%7Brecipient" \
                "%7D%2Ctimestamp%3A%7Btimestamp%7D%2Cconfirmations%3A%7Bconfirmations%7D"
        title_expected = "note:,recipient:9tQoHWyZ4yXUgbz9nvMcFZUfDy5hxcdZabQCxmNC" \
                         "UukKYicXegsDL7nQpcUa3A1pF6K3fhq3scsyY88tdB1MqucULcKzWZC," \
                         "timestamp:2018-01-29 13:17:18,confirmations:1"
        body_expected = "tx_id:4ea70add5d0c7db33557551b15cd174972fcfc73bf0f6a6b47b7837564b708d3," \
                        "payment_provider:Monero,amount:4,fee:0.00096255"
        body_after, title_after = parse_placeholders(self.transaction, body, title)
        self.assertEqual(body_after, body_expected)
        self.assertEqual(title_after, title_expected)

        # case when the user specifies a placeholder, but that transaction's attribute was never populated with data
        def side_effect_lonely_tx(log):
            if mock_logger.debug.call_count == 1:
                self.assertEqual(
                    log,
                    'PaymentProvider: Monero TXID: lonelytx Status: The placeholder "{amount}" was specified, '
                    "but no data was found. Network error or user error. Action: Continuing",
                )
            if mock_logger.debug.call_count == 2:
                self.assertEqual(
                    log,
                    'PaymentProvider: Monero TXID: lonelytx Status: The placeholder "{recipient}" was specified, '
                    "but no data was found. Network error or user error. Action: Continuing",
                )

        transaction_with_no_details = MoneroTransaction(
            "lonelytx", payment_provider="Monero"
        )
        with patch.object(utils, "logging") as mock_logger:
            mock_logger.debug = MagicMock(side_effect=side_effect_lonely_tx)
            parse_placeholders(transaction_with_no_details, "{amount}", "{recipient}")

    @patch("apprisetransactions.utils.requests.get")
    def test_currency_converter(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.amount_in_usd_result
        amount_in_usd = currency_converter(
            self.transaction.amount,
            self.transaction.currency,
            "USD",
            self.transaction.timestamp,
        )
        self.assertEqual(amount_in_usd, Decimal("1269.660000000000081854523160"))

    @patch("apprisetransactions.utils.requests.get")
    def test_currency_converter_error(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.amount_in_error
        with self.assertRaises(ExchangeRateDataError):
            currency_converter(
                self.transaction.amount,
                self.transaction.currency,
                "ABCD",
                self.transaction.timestamp,
            )

    @patch("apprisetransactions.utils.requests.get")
    def test_parse_currency_conversion(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.amount_in_usd_result
        # simple
        body = "Congrats%21%20You%27ve%20received%20%24%7Bamount_in_usd%7D"
        title = "%24%7Bamount_in_usd%7D%20received%20via%20%7Bpayment_provider%7D"
        title_expected = "$1269.66 received via Monero"
        body_expected = "Congrats! You've received $1269.66"
        body_after, title_after = parse_placeholders(self.transaction, body, title)
        self.assertEqual(body_after, body_expected)
        self.assertEqual(title_after, title_expected)
