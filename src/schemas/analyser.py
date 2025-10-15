import os


class SchemaAnalyser:
    def __init__(self):
        pass

    @staticmethod
    def analyse_schema(file_path: str) -> str:
        print(f"🔍 Attempting to identify schema from file name...")

        filename = os.path.basename(file_path).lower()
        extension = os.path.splitext(filename)[1]

        # Mapping of known patterns to schema names
        schema_map = {"nginx.conf": "nginx", "package.json": "package", "docker-compose.yml": "docker",
            "settings.yaml": "settings", "config.json": "generic_json", "sys.conf": "conf", ".json": "generic_json",
            ".yaml": "generic_yaml", ".yml": "generic_yaml", ".conf": "conf"}

        # Exact match first
        if filename in schema_map:
            schema_name = schema_map[filename]
            print(f"✅ Detected schema: {schema_name}")
            return schema_name

        # Extension-based fallback
        if extension in schema_map:
            schema_name = schema_map[extension]
            print(f"⚠️ Using fallback schema based on extension: {schema_name}")
            return schema_name

        print("❌ Could not determine schema automatically.")
        return "unknown"
