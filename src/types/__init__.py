from typing import TypedDict, Union, List, Dict

# Define basic type aliases
SchemaType = Union[str, bool, Dict, List[str]]
SchemaPath = List[str]
SchemaName = str
FieldName = str
TypeString = str


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
    required: Dict[FieldName, TypeString]
    optional: Dict[FieldName, TypeString]


class PartialSchema(TypedDict, total=False):
    required: Dict[FieldName, TypeString]
    optional: Dict[FieldName, TypeString]


class TypeMismatch(TypedDict):
    field: FieldName
    expected: TypeString
    actual: TypeString


class ValidationResult(TypedDict):
    missing_required: List[FieldName]
    extra_required: List[FieldName]
    missing_optional: List[FieldName]
    extra_optional: List[FieldName]
    type_mismatches: List[TypeMismatch]


SchemaPathMap = Dict[str, SchemaPath]
SchemaNameMap = Dict[str, SchemaName]
RawSchemaData = Dict[str, Dict[str, Dict[str, Schema]]]
ConfigData = Dict[str, Union[str, int, float, bool, List, Dict]]

__all__ = ["Schema", "PartialSchema", "SchemaFields", "SchemaType", "SchemaPath", "SchemaName", "FieldName",
    "TypeString", "TypeMismatch", "ValidationResult", "SchemaPathMap", "SchemaNameMap", "RawSchemaData", "ConfigData"]
