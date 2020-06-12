# settings.py
class BlockchainSecurity:
    MEM_POOL_ONLY = 0
    MEM_POOL_AND_BLOCKCHAIN = -1
    IN_A_BLOCK = 1
    FULLY_CONFIRMED = 10


def init():
    global security_level
    security_level = BlockchainSecurity.MEM_POOL_ONLY
    global server_config
    server_config = None
    global logging_config_file
    logging_config_file = "logging_config.ini"
