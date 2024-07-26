"""Return a valid config object from a json file for the application."""
from pathlib import Path
import json
from termcolor import cprint
import colorama

from .config import Config
from .constants import (ERROR_COLOUR, DEFAULTS_ERR_MSG, INVALID_JSON_MSG)

colorama.init()


class JsonConfig(Config):
    """
        A class to handle config files in json format
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_config(self) -> dict[str, object]:
        # Open the config file and return the contents as a dict
        try:
            with open(self.path, 'r') as f_config:
                try:
                    return json.load(f_config)
                except json.decoder.JSONDecodeError:
                    if self.defaults:
                        return self.defaults
                    else:
                        cprint(f"{INVALID_JSON_MSG} {self.path}",
                               ERROR_COLOUR)
        except FileNotFoundError:
            if self.defaults:
                return self.defaults
            else:
                cprint(DEFAULTS_ERR_MSG, ERROR_COLOUR)
        return {}

    def save(self):
        if not self.path.parent.is_dir():
            self.create_directories()
        try:
            with open(self.path, 'w') as f_config:
                json.dump(self.__dict__['config'], f_config)
            return self.STATUS_OK
        except Exception as err:
            return err
