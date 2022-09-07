import json
import os
from os import environ


basedir = os.environ.get('basepath')
conf_path = os.environ.get('configpath', 'conf/')

class ResourceConfigs:

    def __init__(self) -> None:
        with open(os.path.join(conf_path, "model_conf.json"), "r") as jsonfile:
            self.model_config = json.load(jsonfile) # Reading the file
            jsonfile.close()

    def get_model_config(self):
        return self.model_config.get("config",{})