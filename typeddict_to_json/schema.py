from typing import get_type_hints, is_typeddict

from typeddict_to_json import Annotation


def resolve_schema(cls):
    if not is_typeddict(cls):
        raise TypeError(f"{cls} is not a TypedDict")

    properties = {}
    required = []

    for field_name, v in get_type_hints(cls, include_extras=True).items():
        annotation = Annotation(v)
        if annotation.is_required():
            required.append(field_name)

        properties[field_name] = {"type": annotation.json_type, **annotation.extra}

        if annotation.is_list():
            child_schema = resolve_schema(annotation.child_type)
            properties[field_name] = {
                "items": {**properties[field_name], **child_schema}
            }

    schema = {"type": "object", "properties": properties, "required": required}
    return schema
