import tempfile

import pytest

from parsers.config_parser import Config


@pytest.fixture
def temp_config_file():
    config_content = """[database]
    host = localhost
    port = 5432

    [api]
    key = secret_key
    timeout = 30
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8') as temp_file:
        temp_file.write(config_content)
        return temp_file.name


def test_config_sections(temp_config_file):
    config = Config(temp_config_file)
    assert hasattr(config, "database")
    assert hasattr(config, "api")


def test_config_values(temp_config_file):
    config = Config(temp_config_file)
    assert config.database.host == "localhost"
    assert config.database.port == "5432"
    assert config.api.key == "secret_key"
    assert config.api.timeout == "30"


def test_missing_section(temp_config_file):
    config = Config(temp_config_file)
    with pytest.raises(AttributeError, match="No such section: missing"):
        config.missing


def test_missing_key(temp_config_file):
    config = Config(temp_config_file)
    with pytest.raises(AttributeError, match="No such key: unknown_key"):
        config.database.unknown_key


def test_invalid_config_path():
    with pytest.raises(FileNotFoundError, match="Config file not found: invalid_path.ini"):
        Config("invalid_path.ini")
