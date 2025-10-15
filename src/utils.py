import json
from pathlib import Path

from .types import Schema, PartialSchema, ConfigData, TypeString


class Utils:
    def __init__(self):
        self.schemas_path = Path("src/schemas/list.json")

    def get_schema(self, file_name: str) -> Schema:
        raw_schemas = self.get_raw_schemas()
        return self.convert_to_schema(raw_schemas)

    def get_raw_schemas(self) -> str:
        return self.schemas_path.read_text(encoding="utf-8")

    @staticmethod
    def convert_to_schema(raw: str) -> Schema:
        try:
            data = json.loads(raw)
            schema_data = data["javascript"]["nodejs"]["package.json"]
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Schema parsing failed: {e}")

        return {
            "required": {str(k): str(v) for k, v in schema_data.get("required", {}).items()},
            "optional": {str(k): str(v) for k, v in schema_data.get("optional", {}).items()}
        }

    def parse_config(self, file_path: str) -> PartialSchema:
        """Parse configuration file and extract schema structure"""
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")

        if path.suffix == ".json":
            data: ConfigData = json.loads(content)
            return self._extract_schema_from_dict(data)

        # Add YAML parsing if needed
        raise NotImplementedError(f"Parser for {path.suffix} not implemented")

    def _extract_schema_from_dict(self, data: ConfigData) -> PartialSchema:
        """Extract schema structure from parsed data"""
        schema: PartialSchema = {"required": {}, "optional": {}}
        for key, value in data.items():
            type_str: TypeString = self._get_type_string(value)
            schema["required"][key] = type_str
        return schema

    @staticmethod
    def _get_type_string(value) -> TypeString:
        """Convert Python type to schema type string"""
        if isinstance(value, str):
            return "string"
        elif isinstance(value, bool):
            return "boolean"
        elif isinstance(value, (int, float)):
            return "number"
        elif isinstance(value, list):
            return "array"
        elif isinstance(value, dict):
            return "object"
        return "unknown"