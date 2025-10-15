from typing import Dict, List, Any

from ..types import PartialSchema, Schema


class SchemaComparator:
    def __init__(self):
        pass

    @staticmethod
    def compare_schema(original_schema: PartialSchema, real_schema: Schema) -> Dict[str, List[Any]]:
        result: Dict[str, List[Any]] = {"missing_required": [], "extra_required": [], "missing_optional": [],
                                        "extra_optional": [], "type_mismatches": []}

        # Compare required fields
        orig_required = original_schema.get("required", {})
        real_required = real_schema["required"]

        for key, expected_type in real_required.items():
            if key not in orig_required:
                result["missing_required"].append(key)
            elif orig_required[key] != expected_type:
                result["type_mismatches"].append(
                    {"field": key, "expected": expected_type, "actual": orig_required[key]})

        for key in orig_required:
            if key not in real_required:
                result["extra_required"].append(key)

        # Compare optional fields
        orig_optional = original_schema.get("optional", {})
        real_optional = real_schema["optional"]

        for key, expected_type in real_optional.items():
            if key not in orig_optional:
                result["missing_optional"].append(key)
            elif orig_optional[key] != expected_type:
                result["type_mismatches"].append(
                    {"field": key, "expected": expected_type, "actual": orig_optional[key]})

        for key in orig_optional:
            if key not in real_optional:
                result["extra_optional"].append(key)

        return result
