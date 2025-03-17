import configparser
import os


class Section(dict):
    def __init__(self, config: configparser.ConfigParser, section: str):
        self._config = config
        self._section = section
        super().__init__(dict(config.items(section)))

    def __getattr__(self, key: str):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"No such key: {key}")


class Config:
    def __init__(self, config_path: str = "config.ini") -> None:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")
            
        self._config = configparser.ConfigParser()
        self._config.read(config_path, encoding="utf-8")

    def __getattr__(self, section: str):
        if self._config.has_section(section):
            return Section(self._config, section)
        raise AttributeError(f"No such section: {section}")
