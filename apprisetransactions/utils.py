import logging
import re
from datetime import datetime
from decimal import Decimal
from .exceptions import ExchangeRateDataError
from urllib import parse

import requests
from requests.exceptions import HTTPError


# flake8: noqa: C901
def parse_placeholders(tx: object, body: str, title: str = None):
    amount_in_fiat = None
    fiat = None
    msg = [body, title]

    # url decode the message just in case the parameters passed are encoded
    i = 0
    for n in msg:
        if msg[i] is not None:
            msg[i] = parse.unquote(msg[i])
            i += 1

    # loop through all the properties of this object
    for prop in dir(tx):
        # we don't care about private and protected attributes
        if prop[0] == "_":
            continue
        # replace any placeholder attributes with the values from this object
        prop_re = f"{{{prop}}}"
        if (
            re.search(f".*{prop_re}.*", msg[0]) is None
            and re.search(f".*{prop_re}.*", msg[1]) is None
            and re.search("{amount_in_(...)}", msg[0]) is None
            and re.search("{amount_in_(...)}", msg[1]) is None
        ):
            continue

        attr = getattr(tx, prop)
        if attr is None:
            logging.debug(
                f"PaymentProvider: {tx.payment_provider} TXID: {tx.tx_id} "
                f'Status: The placeholder "{prop_re}" was specified, but no data was found.'
                f" Network error or user error. Action: Continuing"
            )
            continue

        i = 0
        for n in msg:
            if msg[i] is not None:
                if re.search(f".*{prop_re}.*", msg[i]):
                    # just swap the value with the {placeholder}
                    # .rstrip('0').rstrip('.') is to remove the trailing zeros from decimals i.e. amount
                    msg[i] = re.sub(
                        prop_re, attr.__str__().rstrip("0").rstrip("."), msg[i]
                    )
                if (
                    prop == "amount"
                    and re.search("{amount_in_(...)}", msg[i]) is not None
                ):
                    # convert amount to fiat if necessary
                    fiat = (
                        re.search("{amount_in_(...)}", msg[i]).group(1)
                        if fiat is None
                        else fiat.lower()
                    )
                    prop_fiat = f"{{amount_in_{fiat}}}"
                    fiat = fiat.upper()
                    # no need to make multiple requests for both body and title
                    if amount_in_fiat is None:
                        amount_in_fiat_unformatted = currency_converter(
                            tx.amount, tx.currency, fiat, tx.timestamp
                        )
                        amount_in_fiat = "{0:.2f}".format(amount_in_fiat_unformatted)

                    msg[i] = re.sub(prop_fiat, amount_in_fiat, msg[i])

            i += 1

    return msg[0], msg[1]  # body, title


def currency_converter(
    amount: Decimal, from_currency: str, to_currency: str, timestamp: datetime = None
):
    tx_datetime = timestamp if timestamp is not None else datetime.now()
    # convert to unix time
    tx_datetime = tx_datetime.timestamp()

    uri = "https://min-api.cryptocompare.com"
    path = "/data/histohour"
    queryStr = (
        f"?fsym={from_currency}&tsym={to_currency}&limit=1&e=CCCAGG&toTs={tx_datetime}"
    )
    url = uri + path + queryStr
    try:
        r = requests.get(url)
        r.raise_for_status()
        if r.json()["Response"] == "Error":
            raise ExchangeRateDataError(r.json()["Message"])
        hdp = r.json()["Data"][1]
    except HTTPError as e:
        raise HTTPError
    except KeyError as e:
        raise KeyError

    avgPrice = Decimal((hdp["high"] + hdp["low"]) / 2)
    return avgPrice * amount
