"""Base class for config object for the application."""

from pathlib import Path
from termcolor import cprint
import colorama

from .constants import ERROR_COLOUR, STATUS_OK, FIELD, NOT_IN_DICT

colorama.init()

MODULE_COLOUR = 'red'


class Config():
    """
    The class takes a path to a config file and if valid, returns a config dict.

    Attributes
    ----------

    path: str
        The path to the config file

    defaults: dict[str, object]
        The defaults are used if the path does not contain a valid config file.
    """

    def __init__(
            self,
            path: str,
            defaults: dict[str, str] = {}
            ):
        self.STATUS_OK = STATUS_OK
        self.path = path
        self.defaults = defaults
        self.config = self._get_config()
        for key, item in self.config.items():
            self.__dict__[key] = item

    def __repr__(self):
        output = ['Config:']
        for key, item in self.__dict__.items():
            output .append(f'{key}: {item}')
        return '\n'.join(output)

    def _get_config(self) -> dict[str, object]:
        # Return config, if contents are valid.
        config = self._read_config()
        for key, item in config.items():
            self.__dict__[key] = item

        if config:
            return config

        if self.defaults:
            return self.defaults
        return {}

    def update(self, field: str, value: object, force: bool = False) -> None:
        """Update the value of an attribute in config."""
        if not force and field not in self.__dict__['config']:
            cprint(f'{FIELD} {field} {NOT_IN_DICT}', ERROR_COLOUR)
            return

        self.__dict__['config'][field] = value

    def create_directories(self) -> bool:
        """Create directories recursively."""
        create_parts = []
        create_path = Path(self.path).parent
        for part in create_path.parts:
            create_parts.append(part)
            new_path = Path(*create_parts)
            if not Path(new_path).is_dir():
                try:
                    Path(new_path).mkdir()
                except FileExistsError:
                    continue
                except PermissionError:
                    print(f'Invalid file path: {new_path}')
                    return False
        return True
