# configer

## User experience

To get started, create a config.json (it could also be a config.yaml) with the following content

```
{
    "load_from": "data.csv",
    "save_to": "data.csv"

}
```

Then create a main.py file with the following content


```
import pandas as pd
from configer import Config

class MyConfig(Config):
    load_from: str
    save_to: str
    

cfg = 
df = pd.read_csv(cfg)






