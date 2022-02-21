from typing import Annotated, Optional, TypedDict

from typeddict_to_json.schema import resolve_schema


def test_type_str_is_converted_to_string():
    class MyType(TypedDict):
        name: str

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
        },
        "required": [
            "name",
        ],
    }


def test_type_int_is_converted_to_integer():
    class MyType(TypedDict):
        age: int

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "age": {"type": "integer"},
        },
        "required": [
            "age",
        ],
    }


def test_none_type_is_converted_to_null():
    class MyType(TypedDict):
        death: None

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "death": {"type": "null"},
        },
        "required": [
            "death",
        ],
    }


def test_bool_is_converted_to_boolean():
    class MyType(TypedDict):
        merried: bool

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "merried": {"type": "boolean"},
        },
        "required": [
            "merried",
        ],
    }


def test_list_is_converted_to_array():
    class MyType(TypedDict):
        children: list

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "children": {"type": "array"},
        },
        "required": [
            "children",
        ],
    }


def test_type_float_is_converted_to_number():
    class MyType(TypedDict):
        weight: float

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "weight": {"type": "number"},
        },
        "required": ["weight"],
    }


def test_optional_field_is_not_in_required_fields():
    class MyType(TypedDict):
        name: str
        age: Optional[int]

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        "required": ["name"],
    }


def test_nested_fields():
    class Nested(TypedDict):
        wtf: str

    class MyType(TypedDict):
        name: str
        accessories: list[Nested]

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "accessories": {
                "items": {
                    "type": "object",
                    "properties": {"wtf": {"type": "string"}},
                    "required": ["wtf"],
                }
            },
        },
        "required": ["name", "accessories"],
    }


def test_additional_annotated_fields():
    class MyType(TypedDict):
        name: Annotated[str, {"maxLength": 10}]

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "name": {"type": "string", "maxLength": 10},
        },
        "required": [
            "name",
        ],
    }


def test_optional_nested_field():
    class Nested(TypedDict):
        wtf: str

    class MyType(TypedDict):
        name: str
        accessories: Optional[list[Nested]]

    schema = resolve_schema(MyType)

    assert schema == {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "accessories": {
                "items": {
                    "type": "object",
                    "properties": {"wtf": {"type": "string"}},
                    "required": ["wtf"],
                }
            },
        },
        "required": ["name"],
    }
