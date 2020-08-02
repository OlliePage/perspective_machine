# %%

from typing import List, Any, Dict
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# %%
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


# %%

## find information about a dataset
# we need to know the following items to make a correct api call:
# * edition
# * version
# * time
# * aggregate
# * geography
# * dimension

# %% md
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

# %%

def post(extension, is_ok=False):
    r = requests.get(f'https://api.beta.ons.gov.uk/v1/' + extension)
    if is_ok:
        print(r)
    return r.json()


# %% md

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

# %%

dataset_id = 'mid-year-pop-est'
uk_population_dataset = post(f'/datasets/{dataset_id}', is_ok=True)
list(uk_population_dataset.keys())

# %%

uk_population_dataset

# %%

uk_population_dataset.keys()

# %% md

## fetch the latest version of this dataset

# %%

uk_pop_latest_version = uk_population_dataset['links']['latest_version']['id']
uk_pop_latest_version

# %%

uk_population_editions = post(f'/datasets/{dataset_id}/editions/time-series/versions/{uk_pop_latest_version}',
                              is_ok=True)
uk_population_editions

# %% md

##### fetch the dimensions that this dataset has to build the rest of the api.
##### We use the code list for this, a separate service

# # %%
#
# uk_population_code_list = post(f'/code-lists/{dataset_id}', is_ok=True)

# %%

dimensions = post(f'/datasets/{dataset_id}/editions/time-series/versions/{uk_pop_latest_version}/dimensions',
                  is_ok=True)

# %%

dimensions['items'][3]
# 'time'
# 'sex'
# 'geography'
# 'age'

# %%

# check options for each dimension
dimension = 'sex'
options: Dict = post(
    f'/datasets/{dataset_id}/editions/time-series/versions/{uk_pop_latest_version}/dimensions/{dimension}/options',
    is_ok=True)
options['items']

# %%

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

# %%

# extract the individual values

observations: Dict = post(f'/datasets/{dataset_id}'
                          f'/editions/time-series'
                          f'/versions/4/'
                          f'observations?'
                          f'time=2017&'
                          f'geography=K02000001&'
                          f'sex=0&'
                          f'age=*', is_ok=True)

# %%

list(observations.keys())

# %%

len(observations['observations'])

# %%

observations_values = pd.DataFrame.from_dict(observations['observations'])['observation']
# %%

data = []
for i in range(len(observations['observations'])):
    try:
        data.append((int(observations['observations'][i]['dimensions']['age']['label']),
                     int(observations['observations'][i]['observation'])))
    except ValueError:
        data.append((observations['observations'][i]['dimensions']['age']['label'],
                     observations['observations'][i]['observation']))
    # %%
# the below list comprehension removes these two string formatted arrays
#  ('Total', '66040229'),
#  ('90+', '579776'),
data_ints = [item for item in data if type(item[0]) == int]
remaining = [item for item in data if type(item[0]) == str]

data_sorted = sorted(data_ints, key=lambda x: x[0])

x, y = zip(*data_sorted)

# %%
fig, ax = plt.subplots()
ax.bar(x, height=y)
ax.set_title('Population Estimates for UK, Wales, etc by age, 2017')
ax.set_xlabel('Age (years)')
ax.set_ylabel('Amount of people')
plt.show()

# %% md

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
# %%

dataset_id = 'index-private-housing-rental-prices'
dataset = post(f'/datasets/{dataset_id}', is_ok=True)
list(dataset.keys())

# %%
dataset_latest_version = dataset['links']['latest_version']['id']
dataset_latest_version # 20

# %%

dataset_editions = post(f'/datasets/{dataset_id}/editions/time-series/versions/{dataset_latest_version}',
                              is_ok=True)
dataset_editions


# %%
dataset_dimensions = post(f'/datasets/{dataset_id}/editions/time-series/versions/{dataset_latest_version}/dimensions',
                  is_ok=True)
# %%
# dataset_dimensions
# print(dataset_dimensions['items'][0]['links']['code_list']['id'])
code_list = []
for i, v in enumerate(dataset_dimensions['items']):
    code_list.append(dataset_dimensions['items'][i]['links']['code_list']['id'])

print(code_list)
# ['housing-rental-prices-variable', 'mmm-yy', 'admin-geography']
# %%
dimension = 'housing-rental-prices-variable'
post(f'/datasets/{dataset_id}/editions/time-series/versions/{dataset_latest_version}/dimensions/{dimension}',
    is_ok=True)
# no options

# %%
post(f'/datasets/{dataset_id}'
                          f'/editions/time-series'
                          f'/versions/25/'
                          f'observations?'
                          f'time=mar-08&'
                          f'admin-geography=K02000001&', is_ok=True)