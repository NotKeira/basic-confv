from ..types import PartialSchema, Schema, ValidationResult, TypeMismatch, FieldName, TypeString


class SchemaComparator:
    def __init__(self):
        pass

    @staticmethod
    def compare_schema(original_schema: PartialSchema, real_schema: Schema) -> ValidationResult:
        result: ValidationResult = {"missing_required": [], "extra_required": [], "missing_optional": [],
            "extra_optional": [], "type_mismatches": []}

        # Compare required fields
        orig_required = original_schema.get("required", {})
        real_required = real_schema["required"]

        for key, expected_type in real_required.items():
            field_name: FieldName = key
            type_string: TypeString = expected_type

            if field_name not in orig_required:
                result["missing_required"].append(field_name)
            elif orig_required[field_name] != type_string:
                mismatch: TypeMismatch = {"field": field_name, "expected": type_string,
                    "actual": orig_required[field_name]}
                result["type_mismatches"].append(mismatch)

        for key in orig_required:
            field_name: FieldName = key
            if field_name not in real_required:
                result["extra_required"].append(field_name)

        # Compare optional fields
        orig_optional = original_schema.get("optional", {})
        real_optional = real_schema["optional"]

        for key, expected_type in real_optional.items():
            field_name: FieldName = key
            type_string: TypeString = expected_type

            if field_name not in orig_optional:
                result["missing_optional"].append(field_name)
            elif orig_optional[field_name] != type_string:
                mismatch: TypeMismatch = {"field": field_name, "expected": type_string,
                    "actual": orig_optional[field_name]}
                result["type_mismatches"].append(mismatch)

        for key in orig_optional:
            field_name: FieldName = key
            if field_name not in real_optional:
                result["extra_optional"].append(field_name)

        return result
