import logging.config
from logging import Logger

from . import settings

settings.init()

logging.config.fileConfig("logging_config.ini")
logger: Logger = logging.getLogger(__name__)
