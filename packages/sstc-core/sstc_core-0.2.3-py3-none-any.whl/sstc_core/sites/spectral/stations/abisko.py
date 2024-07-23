from ..io_tools import load_yaml
from pathlib import Path


stations_dirpath = Path(__file__).parent
spectral_dirpath = Path(stations_dirpath).parent
config_dirpath = spectral_dirpath / "config"


meta ={
    "version": '2024_v0.1',
    "acronym": "ANS",
    "name": "Abisko Scientific Research Station",
    "is_active": True,
    "short_name": "Abisko",
    "system_name": "abisko",    
    "locations_dirpath": config_dirpath / 'locations' / 'locations_abisko.yaml',
    "platforms_dirpath": config_dirpath / 'platforms' / 'platforms_abisko.yaml',
    
}


# Loading station locations config
locations = load_yaml(meta["locations_dirpath"])

# Loading station platforms config
platforms = load_yaml(meta["platforms_dirpath"] )

