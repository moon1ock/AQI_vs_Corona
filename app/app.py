# -*- coding: utf-8 -*-
# Run this app with `python3 app.py` and
# make sure you activated the venc
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import numpy as np 
from datetime import datetime as dt
import statsmodels.api as sm
import plotly.express as px

from urllib.request import urlopen
import json
import plotly

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

# DATA manipulation
df_clean = pd.read_csv("data/clean_data.csv")
df_clean = df_clean[['date', 'Name', 'state', 'FIPS', 'positive', 'AQI', 'date_str']]
df_clean['date'] = pd.to_datetime(df_clean['date'], format='%Y/%m/%d')
df_clean.sort_values(by=["date", "state"])
df_clean["rank"] =  df_clean[['positive', 'AQI']].apply(lambda x: x[0]/(9.041993e+06) + x[1]/(153.285714) , axis=1)

top_10_states = df_clean.loc[df_clean["date"] == dt.strptime('2020-09-21', '%Y-%m-%d')].sort_values(by = 'positive').tail(10)['state']
df_top10_select = df_clean.loc[(df_clean["state"].isin(top_10_states)) & (df_clean["date"] >= dt.strptime('2020-03-15', '%Y-%m-%d')),].copy()

########################################################################

############### US RANKS
rank = px.choropleth(df_clean, 
                           color='rank',
                           locationmode = 'USA-states',
                           locations='state',
                           color_continuous_scale="thermal_r",
                           hover_name = 'Name',
                           hover_data = ['AQI', 'positive'],
                           scope = 'usa',template = 'plotly_dark',
                           animation_frame = 'date_str',
                           animation_group = 'date_str', 
                           width = 1600,
                           height = 800,)
rank.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

############## US MAP positvive
positive = px.choropleth(df_clean,
                           color='positive',
                           locationmode = 'USA-states',
                           locations='state',
                           color_continuous_scale="thermal_r",
                           hover_name = 'Name',
                           scope = 'usa',
                           animation_frame = 'date_str',
                           animation_group = 'date_str',
                           template = 'plotly_dark',
                           labels={'tests_per_1000':'Tests Per 1000 People'},
                           #title = "US State-By-State Corona Cases"
                            )
positive.update_layout(margin={"r":0,"t":50,"l":0,"b":0})

aqi = px.choropleth(df_clean, 
                           color='AQI',
                           locationmode = 'USA-states',
                           locations='state',
                           color_continuous_scale="thermal_r",
                           hover_name = 'Name',
                           hover_data = ['positive'],
                           scope = 'usa',
                           animation_frame = 'date_str',
                           animation_group = 'date_str', template = 'plotly_dark', )
aqi.update_layout(margin={"r":0,"t":45,"l":0,"b":0})


bubbles = px.scatter(df_clean, x="date_str", y="AQI",
	               size="positive", color="state",
                 hover_name="Name", size_max=60,
                 template = 'plotly_dark',
                 title = "Correlation of AQI vs Positives in Bubbles")

ols = px.scatter(df_top10_select,
                 x="rank", y="AQI", 
                 color = "state", trendline = "ols",template = 'plotly_dark',
                 hover_name = "Name", title = "OLS timeless RANK vs AQI")

########################################################################

app.layout = html.Div(
    id="root",
    children=[
        html.Div(
            id="header",
            children=[
                html.H4(id = "NAME1", children="Data Analysis of Corona vs AQI"),
                html.P(
                    id="description",
                    children="Projects in Data Science Final Project by Andriy, Daniella, and Nurgazy.",
                ),
            ],
        ), ###### RANK MAP ############3333
        html.Div(
            className="app-container",
            children=[
                html.Div(

                    children=[
                        html.Div(
                            className="heatmap-container",
                            children=[
                                html.P(
                                    "US States Ranks over Time",
                                    className ="heatmap-title",
                                ),
                                dcc.Graph(

                                    className='county-choropleth',
                                    figure=rank
                                )
                            ],
                        )
                    ]
                )
            ]
        ),
        html.Div(
            className="float-container",
            children=[
                html.Div(
                    children=[
                        html.Div(
                            className="heatmap-container",
                            children=[
                                html.P(
                                    "US States AQI over time",
                                    className ="heatmap-title",
                                ),
                                dcc.Graph(

                                    className='county-choropleth',
                                    figure=aqi
                                )
                            ],
                        ),
                        html.Div(
                            className="heatmap-container",

                            children=[
                                html.P(
                                    "US States Positive Corona Cases over time",
                                    className ="heatmap-title",
                                ),
                                dcc.Graph(

                                    className='county-choropleth',
                                    figure=positive
                                )
                            ],
                        ),
                        html.Div(
                            className="heatmap-container",

                            children=[
                                html.P(
                                    "Correlation of AQI and Positive Tests",
                                    className ="heatmap-title",
                                ),
                                dcc.Graph(
                                    className='county-choropleth',
                                    figure=bubbles
                                )
                            ],
                        ),
                        html.Div(
                            className="heatmap-container",

                            children=[
                                html.P(
                                    "Regression fit on the data",
                                    className ="heatmap-title",
                                ),
                                dcc.Graph(
                                    className='county-choropleth',
                                    figure=ols
                                )
                            ],
                        )
                    ]
                )
            ]
        )
    ]
)


########################################################################




if __name__ == '__main__':
    app.run_server(debug=True)