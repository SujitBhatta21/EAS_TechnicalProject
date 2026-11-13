"""
TESTING REQUIREMENTS:
- Testing if the YAML file exists.
- Malformed YAML e.g. syntax error.
- Missing required fields i.e. sites, warn_days, or timeout_sec.
- Empty hostnames list
"""

import pytest
import yaml

from checker.config import load_config


def test_load_existing_yaml(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("sites:\n  - hostname: example.com\nwarn_days: 30\ntimeout_sec: 5\n")

    assert load_config(path) == {
        "sites": [{"hostname": "example.com"}],
        "warn_days": 30,
        "timeout_sec": 5,
    }


def test_missing_yaml_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "missing.yaml")


def test_malformed_yaml(tmp_path):
    path = tmp_path / "invalid.yaml"
    path.write_text("sites: [unclosed\n")

    with pytest.raises(yaml.YAMLError):
        load_config(path)


@pytest.mark.parametrize("missing_field", ["sites", "warn_days", "timeout_sec"])
def test_missing_required_field_is_rejected(tmp_path, missing_field):
    config = {"sites": [{"hostname": "example.com"}], "warn_days": 30, "timeout_sec": 5}
    del config[missing_field]
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(config))

    # The design requires rejection, but does not specify the exception type.
    with pytest.raises((ValueError, KeyError, TypeError)):
        load_config(path)


def test_empty_hostnames_list_is_rejected(tmp_path):
    path = tmp_path / "config.yaml"
    path.write_text("sites: []\nwarn_days: 30\ntimeout_sec: 5\n")

    with pytest.raises((ValueError, KeyError, TypeError)):
        load_config(path)
