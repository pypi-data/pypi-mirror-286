
from pathlib import Path

from ..src.toml_config import TomlConfig
from ..src.constants import STATUS_OK

CONFIG_ATTRS = {
    'month': [int],
    'payment_bbo': [int, float],
    'period_months': [int],
}
ANSI_COLOR_RED = "\x1b[31m"
ANSI_COLOR_RESET = "\x1b[0m"
ANSI_COLOR_RED = ""
ANSI_COLOR_RESET = ""

TEST_DATA_PATH = Path(Path(__file__).parent, 'test_data')


def test_config_structure():
    path = Path(TEST_DATA_PATH, 'config.toml')
    config = TomlConfig(path)
    assert isinstance(config.config, dict)
    assert len(config.config) == 3


def test_config_missing(capsys):
    path = Path(TEST_DATA_PATH, 'not_a_file.toml')
    err_msg = f'No default config defined'
    TomlConfig(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def test_config_invalid_toml(capsys):
    path = Path(TEST_DATA_PATH, 'config_invalid_toml.toml')
    err_msg = f"Invalid toml format in {path}"
    TomlConfig(path)
    captured = capsys.readouterr()
    assert captured.out.strip() == f'{ANSI_COLOR_RED}{err_msg}{ANSI_COLOR_RESET}'


def test_config_save_status():
    path = Path(TEST_DATA_PATH, 'config.toml')
    config = TomlConfig(path)
    saved = config.save()
    assert saved == STATUS_OK
