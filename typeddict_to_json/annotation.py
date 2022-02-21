from __future__ import annotations

from typing import Type, Union, _eval_type


class Annotation:
    TYPES_MAP: dict[Type, str] = {
        int: "integer",
        str: "string",
        float: "number",
        type(None): "null",
        bool: "boolean",
        list: "array",
    }

    def __init__(self, annotation: object):
        evaled_type = _eval_type(annotation, globals(), None)
        self.annotation: Type = evaled_type

    def __repr__(self):
        return f"Annotation({self.annotation})"

    @property
    def name(self):
        return self.annotation.__name__

    @property
    def child_type(self):
        types = getattr(self.annotation, "__args__", None)
        if not types:
            return self.annotation

        non_optional_types = tuple(
            filter(
                lambda x: x is not type(None),  # noqa: E721
                types,
            )
        )

        child_type = Union[non_optional_types]

        return child_type

    @property
    def extra(self) -> dict:
        metadata = getattr(self.annotation, "__metadata__", {})

        keywords = {}
        for keyword in metadata:
            if not isinstance(keyword, dict):
                raise ValueError(f"{keyword} is not a dict")
            keywords = {**keywords, **keyword}

        return keywords

    def is_optional(self) -> bool:
        types = getattr(self.annotation, "__args__", None)
        if not types:
            return False

        # A Union to be optional needs to have at least one None type
        return any(x is type(None) for x in types)  # noqa: E721

    def is_list(self) -> bool:
        annotation_origin = getattr(self.annotation, "__origin__", None)
        return annotation_origin == list

    def is_annotated(self) -> bool:
        metadata = getattr(self.annotation, "__metadata__", None)
        if metadata:
            return True
        return False

    def is_required(self) -> bool:
        return not self.is_optional()

    @property
    def json_type(self) -> str:
        if self.is_list():
            return "object"
        if self.is_optional() or self.is_annotated():
            if Annotation(self.child_type).is_list():
                return "object"
            return self.TYPES_MAP[self.child_type]
        return self.TYPES_MAP[self.annotation]
