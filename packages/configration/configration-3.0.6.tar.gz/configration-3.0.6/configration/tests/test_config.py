import os
from pathlib import Path

from ..src.json_config import JsonConfig
from ..src.toml_config import TomlConfig
from ..src.constants import DEFAULTS_ERR_MSG

CONFIG_ATTRS = {
    'month': [int],
    'payment': [float],
    'transactions': [list],
}
ANSI_COLOR_RED = "\x1b[31m"
ANSI_COLOR_RESET = "\x1b[0m"
ANSI_COLOR_RED = ""
ANSI_COLOR_RESET = ""

TEST_DATA_PATH = Path(Path(__file__).parent, 'test_data')


def test_all(capsys):
    for index, config_class in enumerate([JsonConfig, TomlConfig]):
        extension = ['json', 'toml'][index]
        config_structure(config_class, extension)
        config_missing(capsys, config_class, extension)
        config_invalid_format(capsys, config_class, extension)


def config_structure(config_class, extension):
    path = Path(TEST_DATA_PATH, f'config.{extension}')
    config = config_class(path)
    assert isinstance(config.config, dict)
    assert len(config.config) == 3


def config_missing(capsys, config_class, extension):
    path = Path(TEST_DATA_PATH, f'not_a_file.{extension}')
    err_msg = DEFAULTS_ERR_MSG
    config_class(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'

def config_invalid_format(capsys, config_class, extension):
    path = Path(TEST_DATA_PATH, f'config_invalid_{extension}.{extension}')
    err_msg = f"Invalid {extension} format in {path}"
    config_class(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def test_update_config():
    # TODO add tests
    ...
