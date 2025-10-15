from typing import TypedDict, Union, List, Dict

# Define basic type aliases
SchemaType = Union[str, bool, Dict, List[str]]


class SchemaFields(TypedDict, total=False):
    # Optional fields can be omitted
    name: SchemaType
    version: SchemaType
    dependencies: SchemaType
    scripts: SchemaType
    description: SchemaType
    http: SchemaType
    server: SchemaType
    events: SchemaType
    worker_processes: SchemaType
    services: SchemaType
    volumes: SchemaType
    networks: SchemaType
    settings: SchemaType
    enabled: SchemaType
    metadata: SchemaType
    logging: SchemaType


class Schema(TypedDict):
    required: Dict[str, str]
    optional: Dict[str, str]


class PartialSchema(TypedDict, total=False):
    required: Dict[str, str]
    optional: Dict[str, str]


__all__ = ["Schema", "PartialSchema", "SchemaFields", "SchemaType"]
