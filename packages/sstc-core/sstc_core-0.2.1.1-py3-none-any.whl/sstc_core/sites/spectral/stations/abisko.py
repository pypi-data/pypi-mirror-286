import os
from ..io_tools import load_yaml
from pathlib import Path


stations_dirpath = Path(__file__).parent
spectral_dirpath = Path(stations_dirpath).parent

print(stations_dirpath)
print(spectral_dirpath)


meta ={
    "version": '2024_v0.1',
    "acronym": "ANS",
    "name": "Abisko Scientific Research Station",
    "is_active": True,
    "short_name": "Abisko",
    "system_name": "abisko",
    #"config_locations_dirpath": os.path.join(spectral_dirpath,'config/locations', 'locations_abisko.yaml'),
    #"config_platforms_dirpath": os.path.join(spectral_dirpath,'config/platforms', 'platforms_abisko.yaml')
}


# Loading station locations config
#locations = load_yaml(meta["config_locations_dirpath"])

# Loading station platforms config
#platforms = load_yaml(meta["config_platforms-dirpath"] )

