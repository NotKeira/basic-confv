# basic-confv

A lightweight configuration file validator based on pre-defined schemas. Validates configuration files against schemas to ensure structural correctness and type safety.

## Features

- Schema-based validation for configuration files
- Support for multiple file formats (JSON, with extensibility for YAML and others)
- Automatic schema detection based on filename
- Manual schema selection
- Detailed validation error reporting
- Type checking for configuration fields
- Required and optional field validation

## Installation

```bash
# Clone the repository
git clone https://github.com/NotKeira/basic-confv.git
# Enter the directory
cd basic-confv
# Install the dependencies (not that we have any!)
pip install -r requirements.txt
```

## Usage

Run the validator:

```bash
python init.py
```

The CLI will prompt you for:
1. The configuration file to validate
2. Schema selection (automatic or manual)

### Example Session

```
Confv Validator @ vX.Y.Z
What file are we validating?
package.json
What schema are we using?
(A) automatic, (anything else = schema name)
a
🔍 Detecting schema automatically...
📄 Parsing package.json...
🔍 Validating against schema...
✅ Configuration is valid.
```

## Supported Schemas

Currently supported configuration files:

- `package.json` - Node.js package configuration
- `nginx.conf` - Nginx web server configuration
- `docker-compose.yml` - Docker Compose configuration
- `config.yaml` - Generic YAML configuration

## Project Structure

```
basic-confv/
├── init.py                    # Entry point
├── v.py                       # Version information
├── src/
│   ├── cli/
│   │   └── __init__.py       # CLI interface
│   ├── schemas/
│   │   ├── analyser.py       # Schema detection
│   │   ├── comparator.py     # Schema comparison logic
│   │   └── list.json         # Schema definitions
│   ├── types/
│   │   └── __init__.py       # Type definitions
│   └── utils.py              # Utility functions
```

## Adding Custom Schemas

Schemas are defined in `src/schemas/list.json`. To add a new schema:

1. Add the schema definition to `list.json`:

```json
{
  "category": {
    "subcategory": {
      "filename.ext": {
        "required": {
          "field_name": "field_type"
        },
        "optional": {
          "optional_field": "field_type"
        }
      }
    }
  }
}
```

2. Update the schema mappings in `src/cli/__init__.py`:
   - Add filename mapping in `get_schema_by_filename`
   - Add name mapping in `request_schema`

## Type System

The validator uses a comprehensive type system defined in `src/types/__init__.py`:

- `string` - String values
- `boolean` - Boolean values
- `number` - Numeric values
- `array` - Array/list values
- `object` - Object/dictionary values

## Development

### Requirements

- Python 3.10+
- Type hints support
- pathlib for path operations

### Code Style

- Formal, concise code structure
- Full type annotations
- British English in comments and documentation

## License

MIT License - see LICENSE file for details

## Author

Keira Hopkins

## Repository

https://github.com/NotKeira/basic-confv

## Version

Current version: 1.4.0