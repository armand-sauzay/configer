# configer.py

import importlib
import json
import yaml
from typing import Any, Dict, Type, TypeVar
from pydantic_settings import BaseSettings
from pydantic import BaseModel, field_serializer, model_validator

T = TypeVar('T', bound=BaseSettings)

def dynamic_instantiate(class_name: str, params: Dict[str, Any] = None) -> Any:
    module_name, class_name = class_name.rsplit('.', 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls(**params) if params else cls()

class DynamicObjectConfig(BaseModel):
    classname: str
    params: Dict[str, Any] = None

    def to_object(self) -> Any:
        return dynamic_instantiate(self.classname, self.params)

    @staticmethod
    def from_object(obj: Any) -> 'DynamicObjectConfig':
        class_name = f"{obj.__module__}.{obj.__class__.__name__}"
        params = obj.get_params() if hasattr(obj, 'get_params') else obj.__dict__
        return DynamicObjectConfig(classname=class_name, params=params)

class FlexConfig(BaseSettings):
    @model_validator(mode='before')
    @classmethod
    def evaluate_dynamic_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        for key, value in values.items():
            if isinstance(value, dict) and 'classname' in value:
                dynamic_object = DynamicObjectConfig(**value)
                values[key] = dynamic_object.to_object()
        return values

    @field_serializer('*', mode='wrap')
    def serialize_dynamic_fields(self, value, field) -> Any:
        if hasattr(value, '__dict__'):
            return DynamicObjectConfig.from_object(value).dict()
        return value

    def model_dump_json(self, **kwargs) -> str:
        data = self.model_dump(**kwargs)
        return json.dumps(data)

    @classmethod
    def load_from_file(cls: Type[T], file_path: str) -> T:
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                config_data = json.load(f)
        elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
            with open(file_path, 'r') as f:
                config_data = yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file format. Please use a .json or .yaml file.")
        
        return cls(**config_data)
