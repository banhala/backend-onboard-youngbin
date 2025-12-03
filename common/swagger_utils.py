from __future__ import annotations

from typing import Type

from drf_yasg import openapi
from pydantic import BaseModel


def pydantic_to_openapi_schema(pydantic_model: Type[BaseModel]) -> openapi.Schema:
    schema = pydantic_model.model_json_schema()
    properties = {}
    required = schema.get("required", [])

    for field_name, field_info in schema.get("properties", {}).items():
        field_type = field_info.get("type")
        field_format = field_info.get("format")
        description = field_info.get("description", "")

        openapi_type = openapi.TYPE_STRING
        if field_type == "integer":
            openapi_type = openapi.TYPE_INTEGER
        elif field_type == "number":
            openapi_type = openapi.TYPE_NUMBER
        elif field_type == "boolean":
            openapi_type = openapi.TYPE_BOOLEAN
        elif field_type == "array":
            openapi_type = openapi.TYPE_ARRAY
        elif field_type == "object":
            openapi_type = openapi.TYPE_OBJECT

        properties[field_name] = openapi.Schema(
            type=openapi_type,
            format=field_format,
            description=description,
        )

    return openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties=properties,
        required=required,
    )
