import logging
from abc import ABC, abstractmethod

from ..configuration import ServerConfig
from ..transactions.transaction import Transaction


class TransactionFactory(ABC):
    payment_provider: str = None
    server_config: ServerConfig = None

    def __init__(self, server_config_file: str = None):
        try:
            self.server_config = ServerConfig(config_file=server_config_file)
        except Exception:
            logging.critical(
                f"PaymentProvider: {self.payment_provider} Status: Failed to set server "
                f"config Action: Further debugging needed",
            )

    @abstractmethod
    def get_transaction(
        self, tx_id: str, get_tx_data: bool, get_raw_data: bool = False
    ) -> Transaction:
        pass
