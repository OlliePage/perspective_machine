import pandas as pd
from datetime import datetime, date
from wrangling_scripts.ons_api import get_editions, get_latest_version, get_dimensions, get_dimension_option, get_observations
import pypickle

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

dataset_id = None
dataset_id = input('> insert dataset_id')
print(dataset_id)
editions = get_editions(dataset_id)
print(editions)
if len(editions) > 1:
    edition = input('> select edition')
else:
    edition = editions[0]
print(dataset_id)

version = get_latest_version(dataset_id,edition)
print('> fetching latest version: ' + str(version))
dimensions = get_dimensions(dataset_id, edition, version)
print(dimensions)
print(dataset_id)
payload = {key: None for key in dimensions}

default_pairs = {'time': '*',
                 'geography': 'K02000001'} # united kingdom

for default_key, default_value in default_pairs.items():
    if default_key in payload:
        payload[default_key] = default_value

print(dataset_id)
unassigned_keys = [k for k, v in payload.items() if v is None]

for key in unassigned_keys: # get all the dictionary values where the key is None
    print(dataset_id)
    available_dimension_options = get_dimension_option(dataset_id, edition, version, key)
    print(f'{key}: {available_dimension_options}')
    payload[key] = input(f'> select dimension option for: {key}')

observations = get_observations(dataset_id, edition, version, payload)

print_observations = input('> view observations? (Y/N)')
if print_observations == 'Y':
    print(observations[:20])

save_request = input('> save observations? (Y/N)')
if save_request == 'Y':
    requested_path = input('> enter the directory path to save observations')
    pypickle.save(f'{requested_path}/{dataset_id}-{version}-{date.today()}.pkl', observations)
