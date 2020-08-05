from datetime import datetime
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import pypickle

# be able to see dataframe outputs in console
# from IPython.core.display import display

desired_width = 320
pd.set_option('display.width', desired_width)
pd.options.display.max_columns = 100

def get_editions(dataset_id: str, print_text=False) -> list:
    r = requests.get(f'https://api.beta.ons.gov.uk/v1/datasets/{dataset_id}/editions')
    pretty_json = json.loads(r.text)

    if print_text:
        print(json.dumps(pretty_json, indent=2))
    return [x['edition'] for x in pretty_json['items']]

def get_latest_version(dataset_id: str, edition: str, print_text=False) -> str:
    r = requests.get(f'https://api.beta.ons.gov.uk/v1/datasets/{dataset_id}/editions/{edition}/versions')

    pretty_json = json.loads(r.text)

    if print_text:
        print(json.dumps(pretty_json, indent=2))
    return pretty_json['items'][-1]['version']

def get_dimensions(dataset_id: str, edition: str, version: str) -> list:
    r = requests.get(f'https://api.beta.ons.gov.uk/v1/datasets/{dataset_id}/editions/{edition}/versions/{version}')
    pretty_json = json.loads(r.text)
    return [x['name'] for x in pretty_json['dimensions']]

def get_dimension_option(dataset_id, edition, version, dimension):
    r = requests.get(f'https://api.beta.ons.gov.uk/v1/datasets/'
                     f'{dataset_id}/'
                     f'editions/{edition}/'
                     f'versions/{version}/'
                     f'dimensions/{dimension}/'
                     f'options')
    pretty_json = json.loads(r.text)
    print(f"number of options: {len(pretty_json['items'])}")

    available_dimensions = [x['dimension'] for x in pretty_json['items']]
    available_labels = [x['label'] for x in pretty_json['items']]
    available_codes = [x['option'] for x in pretty_json['items']]

    df = pd.DataFrame(data={'dimension': available_dimensions,
                           'label': available_labels,
                           'code': available_codes})


    return df

def get_observations(dataset_id: str, edition: str, version: str, payload: dict):
    r = requests.get(f'https://api.beta.ons.gov.uk/v1/datasets/{dataset_id}/editions/{edition}/versions/{version}/observations?', params=payload)
    observations = json.loads(r.text)['observations']

    time_axis = [x['dimensions']['time']['label'] for x in observations]
    observation_values = [float(x['observation']) for x in observations]

    return list(zip(time_axis, observation_values))

# payload = {
#     'geography':'E12000007',
#     'variable': 'index',
#     'time': '*'
# }

# observations = get_observations('index-private-housing-rental-prices', 'time-series', '20', payload=payload)
# observations.sort(key = lambda date: datetime.strptime(date[0], '%b-%y'))
#
# # print(observations)
# # %%
#
# pypickle.save('./observations.pkl',observations)
# # %%
# with open ('observations', wb) as f:
#     pkl.dump(observation, f)
# # %%
# x, y = zip(*observations)
# # %%
# fig, ax = plt.subplots()
# ax.bar(x[-60:], height=y[-60:])
# ax.set_title('Index of Private Housing Rental Prices')
# ax.set_xlabel('Time')
# ax.set_ylabel('')
# plt.xticks(rotation=90)
# plt.show()
# %%



