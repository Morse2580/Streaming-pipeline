import json
from pathlib import Path
from typing import Dict

import yaml
from pydantic import ValidationError

from src.entities.model_entities import TradeEventMessage


def load_dict(filepath: str) -> Dict:
    """Load a dictionary from a JSON's filepath.

    Args:
        filepath (str): location of file.

    Returns:
        Dict: loaded JSON data.
    """
    with open(filepath) as fp:
        d = json.load(fp)
    return d


def load_conf(conf_file_path: str):
    """
    Reads a YAML file and returns the configuration values as a dictionary.
    """
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    conf_file_path = Path(BASE_DIR / "config" / conf_file_path)

    try:
        with open(conf_file_path, 'r') as file:
            try:
                config_values = yaml.safe_load(file)
                if not isinstance(config_values, dict):
                    raise ValueError("The YAML file does not contain valid key-value pairs.")
                return config_values
            except yaml.YAMLError as e:
                print(f"Error parsing YAML: {e}")
                return {}
    except FileNotFoundError:
        print(f"Config file not found: {conf_file_path}")
        return {}
