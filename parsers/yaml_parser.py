from typing import Any, Dict, Iterator, List

import yaml


class CustomDumper(yaml.SafeDumper):
    """Custom Dumper to add indentation for arrays."""

    def increase_indent(self, *args, **kwargs):
        return super().increase_indent(flow=False, indentless=False)


class YamlParser:
    """
    A class for parsing, modifying, and saving YAML files.
    Supports both attribute-style and dictionary-style access.
    """

    def __init__(self, yaml_path: str | Dict[str, Any], _parent: "YamlParser" = None) -> None:
        """
        Initializes the YamlParser instance.
        If given a file path, loads the YAML data from the file.
        If given a dictionary, uses it as the internal data.
        """
        if isinstance(yaml_path, str):
            self._path = yaml_path
            self._data = self.load_yaml(yaml_path)
        elif isinstance(yaml_path, dict):
            self._data = yaml_path
        else:
            raise TypeError("config_path must be a file path (str) or a dictionary.")
        self._parent = _parent  # Prevent infinite recursion

    def __getattr__(self, key: str) -> Any:
        """Allows access to dictionary keys as attributes."""
        if key in self._data:
            value = self._data[key]
            if isinstance(value, dict):
                return YamlParser(value, self)  # Pass parent to prevent recursion
            elif isinstance(value, list):
                return [YamlParser(item, self) if isinstance(item, dict) else item for item in value]
            return value
        raise AttributeError(f"No such key: {key}")

    def __setattr__(self, key: str, value: Any) -> None:
        """Allows setting values using attribute-style access."""
        if key in {"_data", "_path", "_parent"}:
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def __delattr__(self, key: str) -> None:
        """Allows deleting keys using attribute-style access."""
        if key in self._data:
            del self._data[key]
        else:
            raise AttributeError(f"No such key: {key}")

    def __getitem__(self, key: str) -> Any:
        """Enables dictionary-style key access, raising an informative error if the key is missing."""
        try:
            return self._data[key]
        except KeyError:
            raise KeyError(f"Key '{key}' not found in YAML data.")

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Enables dictionary-style key assignment.
        """
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        """Enables dictionary-style key deletion."""
        del self._data[key]

    def __str__(self) -> str:
        """Returns a string representation of the stored data."""
        return str(self._data)

    def __dir__(self) -> List[str]:
        """Returns available attributes, including YAML keys."""
        return list(self._data.keys()) + super().__dir__()

    def __contains__(self, key: str) -> bool:
        """Checks if a key exists in the data."""
        return key in self._data

    def __iter__(self) -> Iterator[str]:
        """Returns an iterator over the keys in the data."""
        return iter(self._data)

    def keys(self) -> List[str]:
        """Returns the keys in the YAML data."""
        return list(self._data.keys())

    def values(self) -> List[Any]:
        """Returns the values in the YAML data."""
        return list(self._data.values())

    def items(self) -> List[tuple]:
        """Returns key-value pairs from the YAML data."""
        return list(self._data.items())

    def update(self, new_data: Dict[str, Any]) -> None:
        """Updates the YAML data with the provided dictionary."""
        if not isinstance(new_data, dict):
            raise TypeError("update() expects a dictionary.")
        self._data.update(new_data)

    def load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Loads YAML data from a file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            raise FileNotFoundError(f"File '{file_path}' not found.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file: {e}")

    def save_yaml(self, path: str = None) -> None:
        """Saves the current data to a YAML file."""
        path_to_save = path if path else self._path
        try:
            with open(path_to_save, "w", encoding="utf-8") as file:
                yaml.dump(
                    self._data,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                    indent=2,
                    Dumper=CustomDumper,
                )
        except IOError as e:
            raise IOError(f"Error saving YAML file: {e}")
