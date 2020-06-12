import argparse
import logging
import logging.config
from logging import Logger

from apprise.utils import split_urls

from . import settings
from .factories import MoneroFactory
from pathlib import Path, PurePath


settings.init()
path = str(PurePath(Path(__file__).parent.absolute(), settings.logging_config_file))
logging.config.fileConfig(path)
logger: Logger = logging.getLogger(__name__)


def add_args():
    try:
        parser = argparse.ArgumentParser(description="Publish transactions")
        requiredNamed = parser.add_argument_group("required named arguments")
        requiredNamed.add_argument(
            "-p",
            "--payment_provider",
            dest="payment_provider",
            type=str,
            help="Provide the payment provider that you're notifying on",
            required=True,
        )
        requiredNamed.add_argument(
            "-x",
            "--tx_id",
            dest="tx_id",
            type=str,
            help="Pass %s, for tx-notify",
            required=True,
        )
        requiredNamed.add_argument(
            "-u",
            "--urls",
            dest="urls",
            type=str,
            help="Specify the apprise url(s) that you would like to use for notification(s), "
            "use a comma for multiple"
            "Pushbullet example: pbul://o.gn5kj6nfhv736I7jC3cj3QLRiyhgl98b"
            "E-mail example: mailto://myuserid:mypass@gmail.com",
            required=True,
        )
        parser.add_argument(
            "-b",
            "--body",
            dest="body",
            type=str,
            help="Specify the url encoded body/msg of the notification you would like to receive, "
            "hint: try {amount_in_usd} placeholder to convert to fiat"
            "hint #2: Go to https://www.urlencoder.org/ for easy url encoding",
            default="Check%20your%20wallet%20for%20more%20details",
        )
        parser.add_argument(
            "-t",
            "--title",
            dest="title",
            type=str,
            help="Specify the title of the notification you would like to receive"
            "This argument is ignored when using Amazon SNS.",
            default="Received%20transaction%20from%20%7Bpayment_provider%7D",
        )
        parser.add_argument(
            "-s",
            "--security_level",
            dest="security_level",
            type=int,
            help="-1 - notifies when tx is in mem_pool or block\n"
            "0 - notifies when tx is in mem_pool\n"
            "1:n - notifies when tx has been added to a block and has n confirmations",
            default=settings.BlockchainSecurity.MEM_POOL_ONLY,
        )
        parser.add_argument(
            "-c",
            "--server_config",
            dest="server_config_file",
            type=str,
            help="To retrieve additional data about the transaction, we need to query a server. See the README",
            default=None,
        )
        parser.add_argument(
            "-a",
            "--attach",
            dest="attach",
            type=str,
            help="To retrieve additional data about the transaction, we need to query a server. See the README",
            default=None,
        )
        parser.add_argument(
            "--get_tx_details",
            default=False,
            dest="get_tx_data",
            action="store_true",
            help="Specify this argument if you would like the details of the transaction "
            "I.e. amount, receiver, etc"
            "If you use placeholders such as {amount_in_usd} then you need to have this argument",
        )
        parser.add_argument(
            "--get_raw_tx_data",
            default=False,
            dest="get_raw_data",
            action="store_true",
            help="Specify this argument if you are forwarding the data to another server"
            " via json, xml, sns. "
            "You should be using a redis queue if you want the python object to be passed",
        )
        parser.add_argument(
            "--debug",
            default=False,
            dest="debug",
            action="store_true",
            help="Enable additional logging",
        )

        return parser.parse_args()

    except Exception as e:
        logger.exception(e)
        exit(1)


def main():
    args = add_args()
    logger.info(
        f"PaymentProvider: {args.payment_provider} TXID: {args.tx_id} "
        f"Status: Script executing Action: Processing"
    )

    if args.debug:
        logging.root.setLevel(logging.DEBUG)
    else:
        logging.root.setLevel(logging.INFO)

    settings.security_level = args.security_level

    payment_providers = {"Monero": MoneroFactory}

    if args.payment_provider in payment_providers:
        transaction_factory = payment_providers[args.payment_provider](
            server_config_file=args.server_config_file
        )
    else:
        logger.critical("The supplied payment provider is not supported")
        exit(1)

    try:
        transaction = transaction_factory.get_transaction(
            tx_id=args.tx_id,
            get_tx_data=args.get_tx_data,
            get_raw_data=args.get_raw_data,
        )
    except Exception as e:
        logger.exception(e)
        exit(1)

    try:
        apprise_result = transaction.notify(
            urls=split_urls(args.urls),
            body=args.body,
            title=args.title,
            attach=args.attach,
        )
        if apprise_result:
            logger.info(
                f"PaymentProvider: {transaction.payment_provider} TXID: {transaction.tx_id} "
                f"Status: Notification(s) sent via apprise"
            )
    except Exception as ae:
        logger.exception(ae)
        exit(1)
