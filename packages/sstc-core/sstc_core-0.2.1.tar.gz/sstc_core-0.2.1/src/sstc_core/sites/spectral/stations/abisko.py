import os
from ..io_tools import load_yaml

version = '2024_v0.1'

stations_dirpath = os.path.dirname(os.path.abspath(__file__))
spectral_dirpath = os.path.basename(stations_dirpath)


meta ={
    "acronym": "ANS",
    "name": "Abisko Scientific Research Station",
    "is_active": True,
    "short_name": "Abisko",
    "system_name": "abisko",
    "config_locations_dirpath": os.path.join(spectral_dirpath,'config/locations', 'locations_abisko.yaml'),
    "config_platforms_dirpath": os.path.join(spectral_dirpath,'config/platforms', 'platforms_abisko.yaml')
}


# Loading station locations config
locations = load_yaml(meta["config_locations_dirpath"])

# Loading station platforms config
platforms = load_yaml(meta["config_platforms-dirpath"] )

