import pytest
from configer.core import DynamicConfig, BaseConfig
import json
import yaml
from pathlib import Path


class SampleClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_params(self):
        return {"a": self.a, "b": self.b}


@pytest.fixture
def sample_class_config_json(tmp_path: Path):
    config_data = {
        "dynamic_field": {
            "classname": "tests.test_core.SampleClass",
            "params": {"a": 5, "b": 6},
        }
    }
    config_file = tmp_path / "config.json"
    config_file.write_text(json.dumps(config_data))
    return config_file


@pytest.fixture
def sample_class_config_yaml(tmp_path: Path):
    config_data = {
        "dynamic_field": {
            "classname": "tests.test_core.SampleClass",
            "params": {"a": 5, "b": 6},
        }
    }
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.safe_dump(config_data))
    return config_file


def test_dynamic_instantiate():
    obj = DynamicConfig(
        classname="tests.test_core.SampleClass", params={"a": 1, "b": 2}
    ).to_object()
    assert isinstance(obj, SampleClass)
    assert obj.a == 1
    assert obj.b == 2


def test_baseconfig_from_object():
    obj = SampleClass(a=3, b=4)
    dynamic_config = DynamicConfig.from_object(obj)
    assert dynamic_config.classname == "tests.test_core.SampleClass"
    assert dynamic_config.params == {"a": 3, "b": 4}


def test_baseconfig_load_from_json_file(sample_class_config_json):
    class Config(BaseConfig):
        dynamic_field: SampleClass

    config = Config.load_from_file(str(sample_class_config_json))
    assert isinstance(config.dynamic_field, SampleClass)
    assert config.dynamic_field.a == 5
    assert config.dynamic_field.b == 6


def test_baseconfig_load_from_yaml_file(sample_class_config_yaml):
    class Config(BaseConfig):
        dynamic_field: SampleClass

    config = Config.load_from_file(str(sample_class_config_yaml))
    assert isinstance(config.example, SampleClass)
    assert config.dynamic_field.a == 5
    assert config.dynamic_field.b == 6
