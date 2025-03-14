import yaml

from parsers.yaml_parser import YamlParser


def test_init_with_dict():
    data = {"key": "value", "nested": {"subkey": 42}}
    config = YamlParser(data)
    assert config.key == "value"
    assert config.nested.subkey == 42


def test_init_with_file(tmp_path):
    yaml_content = """key: value
nested:
  subkey: 42"""
    yaml_file = tmp_path / "config.yaml"
    yaml_file.write_text(yaml_content)

    config = YamlParser(str(yaml_file))
    assert config.key == "value"
    assert config.nested.subkey == 42


def test_getattr():
    data = {"name": "test", "info": {"age": 30}}
    config = YamlParser(data)
    assert config.name == "test"
    assert config.info.age == 30


def test_setattr():
    config = YamlParser({})
    config.new_key = "new_value"
    assert config.new_key == "new_value"
    config.new_key = "very_new_key"
    assert config.new_key == "very_new_key"


def test_getitem():
    config = YamlParser({"key": "value"})
    assert config["key"] == "value"


def test_setitem():
    config = YamlParser({})
    config["key"] = "value"
    assert config.key == "value"


def test_update():
    config = YamlParser({"a": 1})
    config.update({"b": 2, "c": 3})
    assert config.b == 2
    assert config.c == 3


def test_contains():
    config = YamlParser({"exists": True})
    assert "exists" in config
    assert "missing" not in config


def test_delete_attr():
    config = YamlParser({"key": "value"})
    del config.key
    assert "key" not in config


def test_delete_item():
    config = YamlParser({"key": "value"})
    del config["key"]
    assert "key" not in config


def test_save_yaml_from_dict(tmp_path):
    config = YamlParser({"saved": "yes"})
    yaml_file = tmp_path / "saved_config.yaml"
    config.save_yaml(str(yaml_file))
    with open(yaml_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    assert data["saved"] == "yes"
