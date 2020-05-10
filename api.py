from pathlib import Path

import requests

datasetId = 'cpih01'
edition = 'time-series'
version = 4
timeLabel = '*'
geographyID = 'K02000001'  # K02000001 = United Kingdom
aggregateID = 'cpih1dim1A0'


def post(extension, is_ok=False):
    r = requests.get(f'https://api.beta.ons.gov.uk/v1/' + extension)
    if is_ok:
        print(r)
    return r.json()


# %%
Path()

# TODO: hello world