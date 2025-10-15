import json
import os
from pathlib import Path

from v import VERSION
from ..schemas.analyser import SchemaAnalyser
from ..schemas.comparator import SchemaComparator
from ..types import Schema, PartialSchema
from ..utils import Utils


class ConfvCLI:
    def __init__(self, utils: Utils):
        self.utils = utils
        self.analyser = SchemaAnalyser()
        self.comparator = SchemaComparator()
        print(f"Confv Validator @ v{VERSION}")

    @staticmethod
    def request_file() -> str:
        print("What file are we validating?")
        while True:
            file = input().strip()
            if os.path.isfile(file):
                return file
            print("File not found. Please enter a valid file path.")

    def get_schema_by_filename(self, file_path: str) -> Schema | None:
        filename = os.path.basename(file_path)

        # Map known filenames to schema paths in list.json
        schema_map = {"package.json": ["javascript", "nodejs", "package.json"],
            "nginx.conf": ["webserver", "nginx", "nginx.conf"],
            "docker-compose.yml": ["containers", "docker", "docker-compose.yml"],
            "config.yaml": ["configuration", "yaml", "config.yaml"]}

        schema_path = schema_map.get(filename)
        if not schema_path:
            print(f"❌ No schema mapping found for file: {filename}")
            return None

        return self.load_schema_by_path(schema_path)

    def request_schema(self, file_path: str) -> dict[str, dict[str, str]] | None:
        print("What schema are we using?")
        print("(A) automatic, (anything else = schema name)")

        while True:
            schema_input = input().strip()
            if schema_input:
                break
            print("Schema not found. Please enter a valid schema name.")

        if schema_input.lower() == "a":
            print("🔍 Detecting schema automatically...")
            schema_data = self.get_schema_by_filename(file_path)
        else:
            # Manual schema name input - you'll need to map these to paths
            schema_name_map = {"package": ["javascript", "nodejs", "package.json"],
                "nginx": ["webserver", "nginx", "nginx.conf"],
                "docker-compose": ["containers", "docker", "docker-compose.yml"],
                "docker": ["containers", "docker", "docker-compose.yml"],
                "config": ["configuration", "yaml", "config.yaml"]}
            schema_path = schema_name_map.get(schema_input.lower())
            if not schema_path:
                print(f"❌ Unknown schema name: {schema_input}")
                return None
            schema_data = self.load_schema_by_path(schema_path)

        if not schema_data:
            print("❌ Schema could not be loaded.")
            return None

        # Validate and convert schema_data to Schema type
        if "required" not in schema_data or "optional" not in schema_data:
            print("❌ Invalid schema format. Must contain 'required' and 'optional'.")
            return None

        return {"required": {str(k): str(v) for k, v in schema_data["required"].items()},
            "optional": {str(k): str(v) for k, v in schema_data["optional"].items()}}

    @staticmethod
    def load_schema_by_path(path: list[str]) -> dict | None:
        """Load schema from list.json using a path like ['javascript', 'nodejs', 'package.json']"""
        schema_file = Path("src/schemas/list.json")
        if not schema_file.is_file():
            print(f"❌ Schema list not found at {schema_file}")
            return None

        try:
            with schema_file.open("r", encoding="utf-8") as f:
                data = json.load(f)

            # Navigate through the nested structure
            current = data
            for key in path:
                if key not in current:
                    print(f"❌ Schema path not found: {' > '.join(path)}")
                    return None
                current = current[key]

            return current
        except (json.JSONDecodeError, KeyError) as e:
            print(f"❌ Error loading schema: {e}")
            return None

    def validate(self, file_path: str, schema: Schema):
        print(f"📄 Parsing {file_path}...")
        parsed_config: PartialSchema = self.utils.parse_config(file_path)

        print("🔍 Validating against schema...")
        result = self.comparator.compare_schema(parsed_config, schema)

        # Check if any validation issues exist
        has_errors = any(result[key] for key in result if result[key])

        if not has_errors:
            print("✅ Configuration is valid.")
        else:
            print("❌ Validation failed:")
            if result["missing_required"]:
                print(f"  Missing required fields: {', '.join(result['missing_required'])}")
            if result["extra_required"]:
                print(f"  Extra required fields: {', '.join(result['extra_required'])}")
            if result["type_mismatches"]:
                for mismatch in result["type_mismatches"]:
                    print(
                        f"  Type mismatch in '{mismatch['field']}': expected {mismatch['expected']}, got {mismatch['actual']}")

    def run(self):
        file_path = self.request_file()
        schema = self.request_schema(file_path)
        if schema:
            self.validate(file_path, schema)
