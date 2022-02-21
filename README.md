# Convert TypedDict into a JSON Schema

## Usage

```python
class Child(TypedDict):
    name: str

class Person(TypedDict):
    name: str
    age: Optional[int]
    children: list[Child]


assert schema == {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "children": {
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"}
                },
                "required": ["name"],
            }
        },
    },
    "required": [
        "name",
        "accessories"
    ],
}
```
