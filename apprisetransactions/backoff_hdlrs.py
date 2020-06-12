import logging

from . import settings


def backoff_confirmations_hdlr(details: []):
    tx = details["args"][0]
    logging.info(
        f"PaymentProvider: {tx.payment_provider} TXID: {tx.tx_id} "
        f"Status: Pending Network Confirmations Security_Level: {settings.security_level} Action: Retry #{details['tries']}"
    )


def backoff_connection_hdlr(details: []):
    tx = details["args"][0]

    logging.error(
        f"PaymentProvider: {tx.payment_provider} TXID: {tx.tx_id} "
        f"Status: No Connection to Monero Wallet RPC Action: Retry #{details['tries']}"
    )


def backoff_http_hdlr(details: []):
    tx = details["args"][0]
    logging.error(
        f"PaymentProvider: {tx.payment_provider} TXID: {tx.tx_id} "
        f"Status: Monero Wallet RPC request failed Action: Retry #{details['tries']}"
    )
