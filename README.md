# configer

## Getting started 

### Installation

```bash
pip install configer
```

### Usage

There are three core concepts in `configer`:
- a config file: `config.yaml` or `config.json`
- a config schema: `schema.yaml` or `schema.json`
- a config object: an object of type `BaseConfig`

#### 1. Create a config file

Create a `config.json` file with the following content:

```json
{
  "name": "John Doe",
  "age": 30,
  "is_student": true
}
```

#### 2. Create a schema file

Create a `schema.json` file with the following content:

```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "type": "integer"
    },
    "is_student": {
      "type": "boolean"
    }
  },
  "required": ["name", "age", "is_student"]
}
```

#### 3. Create a config object

```python
from configer import BaseConfig

config = BaseConfig(config_file="config.json", schema_file="schema.json")
```

