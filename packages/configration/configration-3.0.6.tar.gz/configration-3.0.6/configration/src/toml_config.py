"""Return a valid config object from a toml file for the application."""
from pathlib import Path
import tomli
import tomli_w
from termcolor import cprint
import colorama

from .config import Config
from .constants import (ERROR_COLOUR, LOCATION_ERR_MSG, DEFAULTS_ERR_MSG,
                        INVALID_TOML_MSG)

colorama.init()


class TomlConfig(Config):
    """
        A class to handle config files in toml format
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _read_config(self) -> dict[str, object]:
        # Open the config file and return the contents as a dict
        try:
            with open(self.path, 'rb') as f_config:
                try:
                    return tomli.load(f_config)
                except tomli.TOMLDecodeError:
                    if self.defaults:
                        return self.defaults
                    else:
                        cprint(f"{INVALID_TOML_MSG} {self.path}",
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
            with open(self.path, mode="wb") as f_config:
                tomli_w.dump(self.__dict__['config'], f_config)
                return self.STATUS_OK
        except Exception as err:
            return err
