import os
import importlib
import importlib.util
from dataclasses import dataclass
from typing import List, Optional, Union
from sstc_core.sites.spectral.catalog import table_name_decorator


@dataclass
class PlatformData:
    """
    A data class to represent a station's platform's data with attributes for station acronym,
    location ID, platform ID, and the file path to a DuckDB database.

    Attributes:
        acronym (str):
            The acronym or system name of the station.
        location_id (str):
            The unique identifier for the location of the station.
        platform_id (str):
            The unique identifier for the platform at the station.
        duckdb_filepath (str):
            The file path to the DuckDB database.

    Methods:
    
        get_table_name() -> str
            Constructs the table name from the station acronym, location ID, and platform ID.
    """

    acronym: str
    location_id: str
    platform_id: str
    duckdb_filepath: str
    
    
    @table_name_decorator 
    def get_table_name(self, table_name):
        """
        Gets the constructed table name.

        Parameters:        
            table_name (str):
                The constructed table name in the format <acronym>_<location_id>_<platform_id>.
            """
        return table_name
    

    
        
def stations_names()->dict:
    """
    Retrieve a dictionary of station names with their respective system names and acronyms.

    Returns:
        dict: A dictionary where each key is a station name and the value is another dictionary
              containing the system name and acronym for the station.

    Example:
        ```python
        stations_names()
        {
            'Abisko': {'system_name': 'abisko', 'acronym': 'ANS'},
            'Asa': {'system_name': 'asa', 'acronym': 'ASA'},
            'Grimsö': {'system_name': 'grimso', 'acronym': 'GRI'},
            'Lonnstorp': {'system_name': 'lonnstorp', 'acronym': 'LON'},
            'Robacksdalen': {'system_name': 'robacksdalen', 'acronym': 'RBD'},
            'Skogaryd': {'system_name': 'skogaryd', 'acronym': 'SKC'},
            'Svartberget': {'system_name': 'svartberget', 'acronym': 'SVB'}
        }
        ```
    """
    return {
        'Abisko': {'system_name': 'abisko', 'acronym': 'ANS'},
        'Asa': {'system_name': 'asa', 'acronym': 'ASA'},
        'Grimsö': {'system_name': 'grimso', 'acronym': 'GRI'},
        'Lonnstorp': {'system_name': 'lonnstorp', 'acronym': 'LON'},
        'Robacksdalen': {'system_name': 'robacksdalen', 'acronym': 'RBD'},
        'Skogaryd': {'system_name': 'skogaryd', 'acronym': 'SKC'},
        'Svartberget': {'system_name': 'svartberget', 'acronym': 'SVB'}
    }


# using Lazy Loading to improve performance and flexibility.
 
def load_station_module(system_name: str):
    """
    DEPRECIATION WARNING: 
        Better to load using `from sstc_core.sites.spectral.stations import <station_name>
                
    Load a Python module dynamically based on the provided system name.

    Parameters:
        system_name (str): The name of the system for which the module should be loaded. 
                       The function expects a file named `<system_name>.py` to be 
                       present in the same directory as this script.

    Returns:
        module: The loaded module object if the module exists and is successfully loaded.

    Raises:
        FileNotFoundError: If the module file does not exist.
        ImportError: If the module cannot be imported.
    """
    filename = f'{system_name}.py'
    filepath = os.path.join(os.path.dirname(__file__), filename)
    
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"No module file found for system '{system_name}' at '{filepath}'")
    
    spec = importlib.util.spec_from_file_location(system_name, filepath)
    if spec is None:
        raise ImportError(f"Could not create a module specification for '{filename}'")
    
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        raise ImportError(f"Failed to load the module '{filename}': {e}")
    
    return module