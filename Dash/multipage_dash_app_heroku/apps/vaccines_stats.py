import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import pathlib
from app import app

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

vaccines_doses_df = pd.read_csv(DATA_PATH.joinpath("vaccine_doses_statewise_v2.csv"))

# Renaming the columns:
vaccines_doses_df.rename(
    columns={'Vaccinated As of': 'date', 'State': 'state', 'First Dose Administered': 'first_dose_administered', 'Second Dose Administered': 'second_dose_administered', 'Total Doses Administered': 'total_dose_administered'}, 
    inplace=True)

vaccines_doses_df = vaccines_doses_df.loc[vaccines_doses_df['state'] != 'Total']                                   

# State-wise vaccines in India:
stateswise_vaccines = vaccines_doses_df.groupby(['state']).agg({'first_dose_administered': 'sum', 'second_dose_administered': 'sum'})
stateswise_vaccines = stateswise_vaccines.reset_index()
stateswise_vaccines = stateswise_vaccines.sort_values(by='second_dose_administered', ascending=False)

"""
Horizontal Bar graph - fully vaccinated pop (graph-1)
"""
h_bar_graph = go.Figure(go.Bar(
    x=stateswise_vaccines['second_dose_administered'],
    y=stateswise_vaccines['state'],
    orientation='h',
    marker_color='rgb(55, 83, 109)'
))
h_bar_graph.update_layout(autosize=False, width=1000, height=760)

"""
Line graph for daily vaccines:
"""
# Get the dataset:
gh_raw_global_csv_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv'
vaccinations_global = pd.read_csv(gh_raw_global_csv_url)
vaccinations_india_wise = vaccinations_global[vaccinations_global.iso_code == 'IND']
daily_vaccines_india_df = vaccinations_india_wise[['date', 'daily_vaccinations', 'location']]
daily_vaccines_india_df = daily_vaccines_india_df.fillna(0)
daily_vaccines_india_df['date'] = pd.to_datetime(daily_vaccines_india_df['date'])
daily_vaccines_india_df['day'] = pd.DatetimeIndex(daily_vaccines_india_df.date).day
daily_vaccines_india_df['month'] = pd.DatetimeIndex(daily_vaccines_india_df.date).month
daily_vaccines_india_df['year'] = pd.DatetimeIndex(daily_vaccines_india_df.date).year
daily_vaccines_india_monthly_df = daily_vaccines_india_df.groupby('month').agg({'daily_vaccinations': 'sum'})
daily_vaccines_india_monthly_df = daily_vaccines_india_monthly_df.reset_index()
# Line graph to show the daily vaccines trend:
daily_vaccines_trend_graph = px.line(daily_vaccines_india_monthly_df, x='month', y='daily_vaccinations', title='Visual trend of Vaccinations (in Millions) every month since Jan 2021')  
# rgb(147, 95, 29)
"""
Covid vaccines export stats:
"""                         
vaccines_exports_df = pd.read_csv(DATA_PATH.joinpath("india_vacci_export_metrics.csv"))
vaccines_exports_df = vaccines_exports_df.sort_values(by='total_supplies', ascending=False).reset_index(drop=True)
fig = px.bar(vaccines_exports_df, x='total_supplies', y='country', barmode='group')
fig.update_layout(autosize=False, width=1000, height=890)

# For maps:
map_graph = px.scatter_mapbox(vaccines_exports_df, lat="latitude", lon="longitude", color="country", size="total_supplies", color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=1, mapbox_style="carto-positron")
map_graph.update_layout(autosize=False, width=1000, height=660, margin={'t':0, 'r':0, 'b':0, 'l':8})  

# For overview dataset:
overview_exports_df = vaccines_exports_df[['country', 'total_supplies']]

"""
App's Layout
"""
layout = html.Div([
    html.H1('Covid vaccinations detail in India:'),
    html.P('These are insights about the covid19 vaccines statistics on vaccinated population and export data from real-time data sources. Hover-over on graps for information'),

    html.Br(),

    dcc.Tabs([
        dcc.Tab(label='Vaccines Administered Datasource', children=[
            html.Br(),
            dcc.Markdown('''
            Indian states with fully vaccinated population since 16-Jan-2021 in descending order
            '''),
            html.A("Datasource", href='https://api.covid19india.org/', target="_blank"),
            dash_table.DataTable(
                id='statewise_vaccines_table',
                columns=[{"name": col, "id": col} for col in stateswise_vaccines.columns],
                data=stateswise_vaccines.to_dict('records')[:10],
                style_header={
                    'fontWeight': 'bold'
                }
            )
        ]),
        dcc.Tab(label='Vaccines Export Dataset', children=[
            html.Br(),
            dcc.Markdown('''
            India has exported covid vaccines to the countries based on below dataset.
            '''),
            html.A("Datasource", href='https://www.mea.gov.in/vaccine-supply.htm', target="_blank"),
            dash_table.DataTable(
                id='df_table',
                columns=[{"name": col, "id": col} for col in overview_exports_df.columns],
                data=overview_exports_df.to_dict('records')[:10],
                style_header={
                    'fontWeight': 'bold',
                    'padding': '5px'
                },
                style_table={'maxWidth': '100%'},
                style_cell={
                    'height': 'auto',
                    'padding': '5px'
                }
            )
        ])
    ]),

    html.Br(),

    dcc.Markdown('''
    #### Select a country to get the text information on total supply by India:
    '''),
    dcc.Dropdown(
        id='countries-list',
        options = [{'label': country, 'value': country} for country in vaccines_exports_df['country']],
        value = 'India'
    ),
    html.Br(),
    html.P(id='country-info-container', children=[], style={'fontWeight': 'bold'}),

    dcc.Markdown('''
    > #### Countries and Total supplies (Graph-1):
    '''),
    dcc.Graph(
        id='exports-graph',
        figure=fig
    ),

    html.Br(),

    dcc.Tabs([
        dcc.Tab(label='Fully Vaccinated Pop', children=[
            html.H5('Fully Vaccinated population in India (state-wise) since Jan-2021'),
            dcc.Graph(
                id='bar-graph-1',
                figure=h_bar_graph
            )
        ]),
        dcc.Tab(label='Daily Vaccines Trends', children=[
            html.H5('Visual trend of daily vaccines in India and monthly from real-time data:'),
            html.A("Real-time datasource", href=gh_raw_global_csv_url, target="_blank"),
            dcc.Graph(
                id='daily-vaccines-trend',
                figure=daily_vaccines_trend_graph
            )
        ]),
        dcc.Tab(label='Covid Vaccines Export', children=[
            html.H5('Map of countries supplied with covid vaccines by India'),
            dcc.Graph(
                id='maps-graph',
                figure=map_graph
            )
        ])
    ]),

    dcc.Markdown('''
    > #### Inference / Summary:
    '''),
    dcc.Markdown(
        '''
        * **Overview of the Datasets** with their fields and factors.
        * **Graph-1**: Countries and total covid vaccines supplied in descending order by India.
        * And below tabs summarises on:
            * **Fully Vaccinated Pop**: State-wise population of fully vaccinated counts in India.
            * **Daily Vaccines Trends**: Displays the trend of vaccines administered in India on a monthly basis.
            * **Covid Vaccines Export**: World Map with countries to which India has exported covid vaccines. If you hover on the markers on the map, that displays quantities in the pop-up box. Note, the larger the size of marker higher the quantities supplied.
        * For **textual information** about vaccines exported, by selecting country from dropdown.
        '''
    )
], className='container')

@app.callback(
    Output(component_id='country-info-container', component_property='children'),
    [Input(component_id='countries-list', component_property='value')]
)
def display_info(value):
    export_quantity = vaccines_exports_df.loc[vaccines_exports_df['country'] == value]['total_supplies'].values
    return 'Total of {} covid supplies were made to {} by India.'.format(export_quantity, value)