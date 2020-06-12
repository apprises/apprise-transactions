from abc import ABC, abstractmethod
from ..configuration import ServerConfig
from decimal import Decimal
from datetime import datetime
from ..exceptions import NoRawTXData, AppriseNotificationFailure
from ..utils import parse_placeholders
import re
from xml.dom.minidom import parseString
from dicttoxml import dicttoxml
from apprise import Apprise
import json


# This object shouldn't be used directly, use it's associated factory to generate
class Transaction(ABC):
    tx_id = None
    currency: str = None
    payment_provider: str = None
    amount: Decimal = None
    fee: Decimal = None
    note: str = None
    recipient: str = None
    timestamp: datetime = None
    confirmations: int = None
    server_config: ServerConfig = None
    _raw_data: dict = None

    def __init__(self, **kwargs):
        self.tx_id = kwargs.pop("tx_id", self.tx_id)
        self.currency = kwargs.pop("currency", self.currency)
        self.payment_provider = kwargs.pop("payment_provider", self.payment_provider)
        self.amount = kwargs.pop("amount", self.amount)
        self.fee = kwargs.pop("fee", self.fee)
        self.note = kwargs.pop("note", self.note)
        self.recipient = kwargs.pop("recipient", self.recipient)
        self.timestamp = kwargs.pop("timestamp", self.timestamp)
        self.confirmations = kwargs.pop("confirmations", self.confirmations)
        self.server_config = kwargs.pop("server_config", self.server_config)
        self._raw_data = kwargs.pop("_raw_data", self._raw_data)

    # raw_data should be true when machine to machine communication is intended
    # raw_data will contain the response received from the server in it's entirety
    @abstractmethod
    def set_transaction_data(
        self, server_config: ServerConfig, get_raw_data: bool = False
    ):
        pass

    # flake8: noqa: F401
    def notify(
        self, urls: list, body: str = None, title: str = None, attach: str = None
    ) -> bool:
        # body/title are ignored for xml/json/sns urls
        if body is not None or title is not None:
            new_body, new_title = parse_placeholders(self, body, title)

        m2m_xml_urls = []
        m2m_json_urls = []
        urls_other = []
        while urls:
            url = urls.pop()
            if url[:3] == "xml":
                m2m_xml_urls.append(url)
                continue
            if url[:4] == "json":
                m2m_json_urls.append(url)
                continue
            if url[:3] == "sns":
                # sns can be used to send sms
                # but can also be used for m2m json message passing
                # txt messages shouldn't have json parsing so we want to separate them out
                phone_pattern = r"\+\d\d{3}\d{3}\d{4}"
                if re.search(phone_pattern, url) is None:
                    m2m_json_urls.append(url)
                    continue
            urls_other.append(url)

        # If apprise fails it will return False
        apprise_xml_result = True
        apprise_json_result = True
        apprise_other_result = True

        if m2m_xml_urls != []:
            if self._raw_data is None:
                raise NoRawTXData(
                    f"Currency: {self.currency} TXID: {self.tx_id} "
                    "Status: Raw TX Data Not Found Action: Report Bug"
                )
            xml: bytes = dicttoxml(self._raw_data)
            xml_body: str = parseString(xml).toprettyxml()
            apprise_xml_result = Apprise(servers=m2m_xml_urls).notify(xml_body)

        if m2m_json_urls != []:
            if self._raw_data is None:
                raise NoRawTXData(
                    f"Currency: {self.currency} TXID: {self.tx_id} "
                    "Status: Raw TX Data Not Found Action: Report Bug"
                )
            json_body = json.dumps(self._raw_data)
            apprise_json_result = Apprise(servers=m2m_json_urls).notify(json_body)

        if urls_other != []:
            apprise_other_result = Apprise(servers=urls_other).notify(
                new_body, new_title, attach=attach
            )

        if not apprise_json_result:
            raise AppriseNotificationFailure(
                f"PaymentProvider: {self.payment_provider} TXID: {self.tx_id} "
                f"Status: Apprise Failed To Send M2M JSON/SNS Notification Action: User Action required"
            )
        if not apprise_xml_result:
            raise AppriseNotificationFailure(
                f"PaymentProvider: {self.payment_provider} TXID: {self.tx_id} "
                f"Status: Apprise Failed To Send M2M XML Notification Action: User Action required"
            )
        if not apprise_other_result:
            raise AppriseNotificationFailure(
                f"PaymentProvider: {self.payment_provider} TXID: {self.tx_id} "
                f"Status: Apprise Failed To Send Notification Action: User Action required"
            )

        return apprise_json_result & apprise_xml_result & apprise_other_result
