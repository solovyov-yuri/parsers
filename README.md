# YAML Parser

## Overview
This module provides a flexible and easy-to-use YAML parser for loading, modifying, and saving YAML files. It supports both dictionary-style and attribute-style access to YAML data.

## Features
- Load YAML data from a file or dictionary
- Access YAML keys as attributes
- Modify, add, and delete keys dynamically
- Save changes back to the original YAML file
- Supports iteration and dictionary-like operations

## Installation
Ensure you have Python installed (version 3.7+ recommended). Install the required dependencies using:

```sh
pip install pyyaml
```

## Usage
### Loading a YAML File
```python
from yaml_parser import YamlParser

parser = YamlParser("config.yaml")
```

### Accessing Data
```python
# Attribute-style access
print(parser.some_key)

# Dictionary-style access
print(parser["some_key"])
```

### Modifying Data
```python
parser.new_key = "new_value"  # Add a new key
parser["existing_key"] = "updated_value"  # Modify an existing key
```

### Saving Changes
```python
parser.save_yaml()
```

## Error Handling
- Raises `FileNotFoundError` if the YAML file does not exist.
- Raises `TypeError` for invalid input types.
- Raises `ValueError` for YAML parsing errors.

## Contributing
Feel free to submit issues or pull requests for improvements and bug fixes.

## License
This project is licensed under the MIT License.