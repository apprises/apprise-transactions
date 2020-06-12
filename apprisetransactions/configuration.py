import json
import os


class ServerConfig:
    protocol = ""
    host = ""
    port = ""
    path = ""
    user = ""
    password = ""
    access_token = ""
    default = False

    def __init__(self, config_file: str, **kwargs):
        self.config_file = config_file
        self.protocol = kwargs.pop("protocol", self.protocol)
        self.host = kwargs.pop("host", self.host)
        self.port = kwargs.pop("port", self.port)
        self.path = kwargs.pop("path", self.path)
        self.user = kwargs.pop("user", self.user)
        self.password = kwargs.pop("password", self.password)
        self.access_token = kwargs.pop("access_token", self.access_token)
        self.set_config()

    def set_config(self):
        if self.config_file is not None:
            if os.path.isfile(self.config_file):
                with open(self.config_file) as infile:
                    self.__dict__ = json.load(infile)
            else:
                self.default = True
        else:
            self.default = True
