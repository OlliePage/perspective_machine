#%%

from typing import List, Any, Dict
import requests
import pandas as pd

#%%
from pandas import Series

r = requests.get('https://api.beta.ons.gov.uk/v1/datasets')
dataset_titles = []
dataset_descriptions: List[Any] = []
dataset_ids: List[Any] = []
for i in range(len(r.json()['items'])):
    dataset_titles.append(r.json()['items'][i]['title'])
    dataset_descriptions.append(r.json()['items'][i]['description'])
    dataset_ids.append(r.json()['items'][i]['id'])

table_of_codes = pd.DataFrame(data={'title': dataset_titles,
                   'description': dataset_descriptions,
                  'dataset_id': dataset_ids})

#%%

## find information about a dataset
# we need to know the following items to make a correct api call:
# * edition
# * version
# * time
# * aggregate
# * geography
# * dimension

#%% md
#
# > This allows querying of a single observation/value by providing one option per dimension, but will also allow one of
# > these dimensions to be a ‘wildcard’ and return all values for this dimension.
#
# `/datasets/{datasetId}/
# editions/{edition}/
# versions/{version}/
# observations?
# time={timeLabel}&
# geography={geographyID}&
# dimension3={dimension3ID}&
# dimension4={dimension4ID}...`

#%%

def post(extension, is_ok=False):
    r = requests.get(f'https://api.beta.ons.gov.uk/v1/' + extension)
    if is_ok:
        print(r)
    return r.json()

#%% md

# Create a chart from Population Estimates for UK, Wales, etc.
#
# * dataset
# * edition
# * version
# * time
# * aggregate
# * geography
# * dimension
#
# code: mid-year-pop-est

#%%

dataset_id = 'mid-year-pop-est'
uk_population_dataset = post(f'/datasets/{dataset_id}', is_ok=True)
list(uk_population_dataset.keys())

#%%

uk_population_dataset

#%%

uk_population_dataset.keys()

#%% md

## fetch the latest version of this dataset

#%%

uk_pop_latest_version = uk_population_dataset['links']['latest_version']['id']
uk_pop_latest_version


#%%

uk_population_editions = post(f'/datasets/{dataset_id}/editions/time-series/versions/{uk_pop_latest_version}', is_ok=True)
uk_population_editions


#%% md

##### fetch the dimensions that this dataset has to build the rest of the api.
##### We use the code list for this, a separate service

#%%

uk_population_code_list = post(f'/code-lists/{dataset_id}', is_ok=True)

#%%

dimensions = post(f'/datasets/{dataset_id}/editions/time-series/versions/{uk_pop_latest_version}/dimensions', is_ok=True)

#%%

dimensions['items'][3]
# 'time'
# 'sex'
# 'geography'
# 'age'

#%%

# check options for each dimension
dimension = 'sex'
options: Dict = post(f'/datasets/{dataset_id}/editions/time-series/versions/{uk_pop_latest_version}/dimensions/{dimension}/options', is_ok=True)
options['items']

#%%

# age = type in int for age, up to '90+'. Use wildcard if possible. e.g '21'
# time = id is the year e.g '2010'
# geography = geography codes. UK = K02000001
# sex = 'All': 0, 'Male': 1, 'Female': 2
# %%

post(f'/datasets/{dataset_id}'
     f'/editions/time-series'
     f'/versions/4/'
     f'observations?'
     f'time=2017&'
     f'geography=K02000001&'
     f'sex=0&'
     f'age=*', is_ok=True)

#%%

# extract the individual values

observations: Dict = post(f'/datasets/{dataset_id}'
     f'/editions/time-series'
     f'/versions/4/'
     f'observations?'
     f'time=2017&'
     f'geography=K02000001&'
     f'sex=0&'
     f'age=*', is_ok=True)

#%%

list(observations.keys())


#%%

len(observations['observations'])

#%%

observations_values = pd.DataFrame.from_dict(observations['observations'])['observation']
#%%
observations['observations'][0]['dimensions']

