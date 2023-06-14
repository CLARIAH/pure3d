import os
import yaml
import pytest

BASE = os.path.expanduser("~/github/clariah/pure3d/pilots/test-pure3d")
SRC = f"{BASE}/src"


def test_yaml_file_exists():
    filename = f"{SRC}/workflow/init.yml"
    assert os.path.exists(filename)


def test_yaml_file_structure():
    filename = f"{SRC}/workflow/init.yml"
    with open(filename, "r") as file:
        try:
            data = yaml.safe_load(file)
            # validate the structure of the YAML file
            assert "userRole" in data
            assert "status" in data
        except yaml.YAMLError as e:
            pytest.fail(f"YAML parsing error: {e}")
