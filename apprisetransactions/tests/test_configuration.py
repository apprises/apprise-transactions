import json
from unittest import TestCase

from apprisetransactions import settings
from apprisetransactions.configuration import ServerConfig


class TestCase_Config(TestCase):
    def setUp(self):
        settings.init()
        self.config = ServerConfig(
            config_file="server.cfg",
            protocol="http",
            host="127.0.0.1",
            port=18088,
            path="/json_rpc",
            user="test",
            password="test",
        )

    def test_config_awrite(self):
        with open(self.config.config_file, "w") as outfile:
            json.dump(self.config.__dict__, outfile)
        pass

    def test_config_read(self):
        read_config = ServerConfig(config_file="server.cfg")
        self.assertEqual(read_config.protocol, self.config.protocol)
        self.assertEqual(read_config.__dict__, self.config.__dict__)
