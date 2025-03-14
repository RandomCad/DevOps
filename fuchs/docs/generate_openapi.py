"""Save this FastAPI app's OpenAPI specification to JSON and YAML"""

import json
import yaml

import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# So now we can import the module
from fuchs.main import app

DIR_PATH = "docs"


def save_openapi_to_json():
    """Save OpenAPI spec to JSON"""

    with open(f"{DIR_PATH}/openapi.json", "w", encoding="utf-8") as json_file:
        json.dump(
            app.openapi(),
            json_file,
            indent=2,
        )


def save_openapi_to_yaml():
    """Save OpenAPI spec to YAML"""

    with open(f"{DIR_PATH}/openapi.yaml", "w", encoding="utf-8") as yaml_file:
        yaml.dump(
            app.openapi(),
            yaml_file,
        )


save_openapi_to_json()
save_openapi_to_yaml()
