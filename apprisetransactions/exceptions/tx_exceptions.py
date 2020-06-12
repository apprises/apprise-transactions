class ExchangeRateDataError(Exception):
    pass


class NoTXFound(Exception):
    pass


class NumConfirmationsNotMet(Exception):
    pass


class NoTXToProcess(Exception):
    pass


# something went wrong and no raw data about the tx was retrieved
class NoRawTXData(Exception):
    pass
