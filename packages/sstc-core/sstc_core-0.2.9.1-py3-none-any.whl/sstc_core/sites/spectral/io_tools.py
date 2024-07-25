import os
import yaml
import requests
from pathlib import Path
from typing import Union


def load_yaml(filepath: Union[str, Path]) -> dict:
    """
    Loads a YAML file.

    Can be used as stand-alone script by providing a command-line argument:
        python load_yaml.py --filepath /file/path/to/filename.yaml
        python load_yaml.py --filepath http://example.com/path/to/filename.yaml

    Parameters:
        filepath (str): The absolute path to the YAML file or a URL to the YAML file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If there is an error while loading the YAML file.
        requests.RequestException: If there is an error while making the HTTP request.
        yaml.YAMLError: If there is an error while loading the YAML file.
    """
    
    # Check if the filepath is an instance of Path and convert to string if necessary
    if isinstance(filepath, Path):
        filepath = str(filepath)    
    
    
    if filepath.startswith('http://') or filepath.startswith('https://'):
        try:
            response = requests.get(filepath)
            response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
            yaml_data = yaml.safe_load(response.text)
            return yaml_data
        except requests.RequestException as e:
            raise requests.RequestException(f"Error fetching the YAML file from {filepath}: {e}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing the YAML file from {filepath}: {e}")
    else:
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"The file {filepath} does not exist.")
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"The file {filepath} was not found: {e}")
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"Error parsing the YAML file from {filepath}: {e}")