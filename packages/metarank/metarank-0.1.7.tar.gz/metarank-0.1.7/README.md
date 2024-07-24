# metarank

> A Python client for [metarank](https://www.metarank.ai/).

## Usage

```bash
pip install metarank
```

## Example

```python
from metarank import Client
from metarank.schemas import FeedbackSchema, FieldSchema

base_url = "http://localhost:8080"
    
client = Client(base_url)
is_healthy = client.health_check() # True

events = [
    FeedbackSchema(
        event="item",
        id="event:1",
        timestamp="1985-07-03T14:31:43+13:00",
        item="item:1",
        fields=[
            FieldSchema(
                name="color",
                value="red"
            )
        ]
    )
]
```
