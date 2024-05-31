# example.py

import json
import yaml
from sklearn.linear_model import LogisticRegression
from .configer import FlexConfig

class CustomClass:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

    def __str__(self):
        return f'{self.name} is {self.age} years old'

    def __repr__(self):
        return f'CustomClass(name={self.name}, age={self.age})'

class AppConfig(FlexConfig):
    name: str
    age: int
    custom: CustomClass
    model: LogisticRegression

def main():
    # Create a JSON config file for demonstration purposes
    json_config_data = {
        "name": "John Doe",
        "age": 30,
        "custom": {
            "classname": "__main__.CustomClass",
            "params": {"name": "John Doe", "age": 30}
        },
        "model": {
            "classname": "sklearn.linear_model.LogisticRegression",
            "params": {"C": 1.0, "max_iter": 100}
        }
    }
    with open('config.json', 'w') as f:
        json.dump(json_config_data, f)
    
    # Create a YAML config file for demonstration purposes
    yaml_config_data = {
        "name": "Jane Doe",
        "age": 25,
        "custom": {
            "classname": "__main__.CustomClass",
            "params": {"name": "Jane Doe", "age": 25}
        },
        "model": {
            "classname": "sklearn.linear_model.LogisticRegression",
            "params": {"C": 1.0, "max_iter": 100}
        }
    }
    with open('config.yaml', 'w') as f:
        yaml.dump(yaml_config_data, f)

    # Load configuration from JSON file
    json_config = AppConfig.load_from_file('config.json')
    print("Config loaded from JSON file:")
    print(json_config)
    print("CustomClass instance from JSON config:")
    print(json_config.custom)
    print("Model instance from JSON config:")
    print(json_config.model)

    # Serialize the config to JSON string
    json_config_str = json_config.model_dump_json()
    print(f"Serialized config to JSON string: {json_config_str}")

    # Load config from JSON string
    new_config = AppConfig.model_validate_json(json_config_str)
    print(f"Loaded config from JSON string: {new_config}")

if __name__ == "__main__":
    main()
