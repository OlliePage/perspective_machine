from flask import Flask, render_template, url_for
from perspectivemachineapp import app
import plotly, json
from wrangling_scripts.wrangle_data import return_figures

@app.route('/')
@app.route('/index')
def index():

    figures = return_figures()

    # plot ids for the html id tag
    ids = [f'figure-{i}' for i, _ in enumerate(figures)]

    # convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           title='Home Page',
                           figure_ids=ids,
                           figuresJSON=figuresJSON)
    
@app.route('/project-one')
def project_one():
    return render_template('project_one.html', title='First Project')

# new route
@app.route('/about')
def about():
    return render_template('about.html', title='About')