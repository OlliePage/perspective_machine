import pypickle
import pandas as pd
import plotly.graph_objs as go
import plotly, json
from datetime import datetime

def return_figures():

    # first chart : Index of Private Housing Rental Prices
    observations = pypickle.load('./perspectivemachineapp/observations.pkl')
    observations.sort(key = lambda date: datetime.strptime(date[0], '%b-%y'))
    x, y = zip(*observations)

    # convert string values of x to dates, so that it will be correctly sorted by plotly
    x = [datetime.strptime(x, '%b-%y') for x in x]

    graph_one = [go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name='Month-Year'
    )]

    layout_one = {
        'title':'Index of Private Housing Rental Prices',
        'xaxis':{'title':'Year-Month',
                 'autotick':True},
        'yaxis':{'title': 'Indexed'}
                  }

    figures = [{'data': graph_one,
                'layout': layout_one}]

    # second chart


    return figures