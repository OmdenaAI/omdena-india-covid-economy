import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from app import app

# ext_styles = ['../assets/css/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=ext_styles)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

"""
Team members table:
"""
members_df = pd.read_excel('datasets/socio-economic-team.xlsx')

layout = html.Div([
    html.H1('Leverage AI to analyse Socio-Economic impacts due to covid19 in India'),
    dcc.Tabs([
        dcc.Tab(label='Overview of the project', children=[
            html.Br(),
            html.P('This is the project for Omdena India Local Chapter - To analyse the impact of covid19 in India to understand how it\'s been affected and changed. In this project we have utilised the technologies of AI and Data Science to understand the data (open-source) collected since the time of this pandemic from January 2020'),
            html.P('The datasets we have used are from Our World in Data, MEA, Covid19India websites along with other resources such as Kaggle and GitHub')
        ]),
        dcc.Tab(label='About this App', children=[
            html.Br(),
            html.P('This is the Dash application to interact with the EDA (Exploratory Data Analysis) performed on the related datasets to get the outputs for the objectives and tasks of this project.')
        ]),
        dcc.Tab(label='Objectives of project', children=[
            html.Br(),
            dcc.Markdown('''
            * **Sentiment Analysis**: Analysing the social and to understand the ongoing tweets about the covid19 and coronavirus hanshtags for India to identify the sentiments of tweets during this time period.
            * **Classification** of the Covid cases text-wise and image-wise: Identifying the covid cases based on the historical datasets from the open-source to recognise report or medical images are related covid and its symptoms.
            * **EDA**: Exploring these datasets and categorising them for getting the insights for social and economic changes and effects from the beginning of this pandemic and EDA is a pre-requisite to get the useful insights from the datasets and utilised for building prediction models.
            * **Time-series modelling**: to understand and forecast the factors such as what could be the total confirmed cases, mortality rates, GDP rates, unemployment, inflation and the related factors would be for the future dates.
            ''')
        ])
    ]),
    html.Br(),
    dcc.Markdown('''
    > ### Active contributors and participants of this project:
    '''),
    dash_table.DataTable(
        id='members-df',
        columns=[{"name": col, "id": col} for col in members_df.columns],
        data=members_df.to_dict('records'),
        style_as_list_view=True,
        style_cell_conditional=[
            {
                'if': {'column_id': col},
                'textAlign': 'left'
            } for col in ['Task Leaders & Contributors']
        ],
        style_table={'minWidth': '100%'},
        style_header={
            # 'backgroundColor': 'white',
            'fontWeight': 'bold'
        }
    ),
    # html.Img(src=app.get_asset_url('../assets/imgs/persona_her_1.png')),
    # html.Img(src=app.get_asset_url('../assets/imgs/persona_her_1.png')),
    # html.Img(src=app.get_asset_url('../assets/imgs/persona_him_2.jpg')),
    # html.Img(src=app.get_asset_url('../assets/imgs/persona_him_2.jpg')),
    # html.Img(src=app.get_asset_url('../assets/imgs/persona_him_2.jpg')),
    # html.Img(src=app.get_asset_url('../assets/imgs/persona_her_1.png')),
], className='container')
