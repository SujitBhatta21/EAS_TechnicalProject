"""
Code to load config file
"""
import yaml 


def load_config(file) -> dict:
    # test_missing_required_field_is_rejected showed vunlnerability with reading file.
    # File is not validated and returned after parsing.
    with open(file, 'r') as f:
        file_read = yaml.safe_load(f)

    # Checking if the file is structured as yaml.
    if not isinstance(file_read, dict):
        raise ValueError("Configuration must be YAML.")
    # Checking if sites field is missing. 
    if "sites" not in file_read:
        raise ValueError("Missing required field: sites")
    # Checking if warn_days field is missing.
    if "warn_days" not in file_read:
            raise ValueError("Missing required field: warn_days")
    # Checking if timeout_sec field is missing.
    if "timeout_sec" not in file_read:
        raise ValueError("Missing required field: timeout_sec")
    # Checking if sites contain list of hostnames.
    if not isinstance(file_read['sites'], list):
        raise ValueError("Sites must be a list with all hostnames")
    # Checking if list of sites is not empty,
    if len(file_read['sites']) < 1: 
        raise ValueError("Sites field must not be empty")

    # Checking if all hostnames inside sites are in correct format.
    for hostname in file_read['sites']:
        if not isinstance(hostname, dict):
            raise ValueError("Each hostname must be in YAML format")

        for item in hostname:
            if item not in hostname:    # Empty
                raise ValueError(f"Item missing in: {item}")
    return file_read