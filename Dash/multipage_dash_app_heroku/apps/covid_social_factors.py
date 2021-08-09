import dash
import dash_table
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import pathlib
import requests
from app import app

# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()

# vaccines_doses_df = pd.read_csv(DATA_PATH.joinpath("vaccine_doses_statewise_v2.csv"))

data_source_url = 'https://api.covid19india.org/v4/min/timeseries.min.json'
pop_data_source_url = 'https://api.covid19india.org/v4/min/data.min.json'

"""
Data pre-processing for real-time source:
"""
response = requests.get("https://api.covid19india.org/v4/min/timeseries.min.json")
if response.status_code == 200:
    crdt_api_data = response.json()
    
    date_on = []
    state_abbv = []
    delta_confirmed = []
    delta_recovered = []
    delta_deceased = []
    delta_tested = []
    delta_vaccinated1 = []
    delta_vaccinated2 = []
    
    for state in crdt_api_data.keys():
        for date in crdt_api_data[state]['dates'].keys():
            state_abbv.append(state)
            date_on.append(date)
            try:
                delta_confirmed.append(crdt_api_data[state]['dates'][date]['delta']['confirmed'])
            except:
                delta_confirmed.append(0)
            try:
                delta_recovered.append(crdt_api_data[state]['dates'][date]['delta']['recovered'])
            except:
                delta_recovered.append(0)
            try:
                delta_deceased.append(crdt_api_data[state]['dates'][date]['delta']['deceased'])
            except:
                delta_deceased.append(0)
            try:
                delta_tested.append(crdt_api_data[state]['dates'][date]['delta']['tested'])
            except:
                delta_tested.append(0)
            try:
                delta_vaccinated1.append(crdt_api_data[state]['dates'][date]['delta']['vaccinated1'])
            except:
                delta_vaccinated1.append(0)
            try:
                delta_vaccinated2.append(crdt_api_data[state]['dates'][date]['delta']['vaccinated2'])
            except:
                delta_vaccinated2.append(0)

    crdt_api_data = pd.DataFrame(
        {
            "state_abbv": state_abbv,
            "date": date_on,
            "delta_confirmed": delta_confirmed,
            "delta_recovered": delta_recovered,
            "delta_deceased": delta_deceased,
            "delta_tested": delta_tested,
            "delta_vaccinated1": delta_vaccinated1,
            "delta_vaccinated2": delta_vaccinated2,
       }
    )

else:
    print("Error while calling API: {}".format(response.status_code, response.reason))

crdt_api_data['date'] = pd.to_datetime(crdt_api_data['date'])

def datetime_split(df):
    df['month'] = df.date.dt.month
    df['day'] = df.date.dt.day
    df['year'] = df.date.dt.year

datetime_split(crdt_api_data)
crdt_api_data_without_total = crdt_api_data.loc[crdt_api_data['state_abbv'] != 'TT']

state_wise_throughout = crdt_api_data_without_total.groupby(['state_abbv'])['delta_confirmed', 
                                                             'delta_recovered', 
                                                             'delta_deceased', 
                                                             'delta_tested', 
                                                             'delta_vaccinated1', 
                                                             'delta_vaccinated2',
                                                             'month',
                                                             'year'].sum().reset_index()
# print(state_wise_throughout.columns)                                                             
                                                            
state_name = {'AN': 'Andaman and Nicobar Islands', 'AP': 'Andhra Pradesh', 'AR': 'Arunachal Pradesh', 'AS': 'Assam', 'BR': 'Bihar', 'CH': 'Chandigarh', 'CT': 'Chhattisgarh', 'DL': 'Delhi', 'DN': 'Dadra and Nagar Haveli', 'GA': 'Goa', 'GJ': 'Gujarat', 'HP': 'Himachal Pradesh', 'HR': 'Haryana', 'JH': 'Jharkhand', 'JK': 'Jammu and Kashmir', 'KA': 'Karnataka', 'KL': 'Kerala', 'LA': 'Ladakh', 'LD': 'Lakshadweep', 'MH': 'Maharashtra', 'ML': 'Meghalaya', 'MN': 'Manipur', 'MP': 'Madhya Pradesh', 'MZ': 'Mizoram', 'NL': 'Nagaland', 'OR': 'Orissa', 'PB': 'Punjab', 'PY': 'Pondicherry', 'RJ': 'Rajasthan', 'SK': 'Sikkim', 'TG': 'Telangana', 'TN': 'Tamil Nadu', 'TR': 'Tripura', 'UP': 'Uttar Pradesh', 'UT': 'Uttarakhand', 'WB': 'West Bengal', 'UN': 'Unnamed'}                                                             

states_longitude = {'AN': 11.53481, 'AP': 14.94011, 'AR': 28.57062, 'AS': 26.50557, 'BR': 25.63716, 'CH': 30.70101, 'CT': 22.15589, 'DL': 28.34020, 'DN': 20.32083, 'GA': 15.29303, 'GJ': 23.16044, 'HP': 32.06414, 'HR': 29.09708, 'JH': 23.68760, 'JK': 33.69450, 'KA': 14.71898, 'KL': 9.27600, 'LA': 34.60545, 'LD': 10.09318, 'MH': 19.48013, 'ML': 25.58248, 'MN': 24.59341, 'MP': 23.50034, 'MZ': 23.42287, 'NL': 25.99085, 'OR': 20.44459, 'PB': 30.27896, 'PY': 11.86268, 'RJ': 26.74981, 'SK': 27.39195, 'TG': 17.84484, 'TN': 11.51220, 'TR': 23.70733, 'UP': 27.87953, 'UT': 30.00196, 'WB': 23.01753, 'UN': 0.0} 

states_latitude = {'AN': 92.68677, 'AP': 79.08234, 'AR': 94.99054, 'AS': 92.66144, 'BR': 85.84991, 'CH': 76.85348, 'CT': 82.30122, 'DL': 77.18631, 'DN': 72.96830, 'GA': 73.92505, 'GJ': 70.89401, 'HP': 76.83722, 'HR': 76.30233, 'JH': 85.05866, 'JK': 75.50990, 'KA': 75.74763, 'KL': 76.71835, 'LA': 77.24699, 'LD': 73.63830, 'MH': 75.65281, 'ML': 91.02999, 'MN': 93.79062, 'MP': 77.16580, 'MZ': 92.79441, 'NL': 94.61091, 'OR': 84.36696, 'PB': 75.18346, 'PY': 79.95504, 'RJ': 73.48627, 'SK': 88.57663, 'TG': 79.34792, 'TN': 78.82475, 'TR': 91.70517, 'UP': 79.74650, 'UT': 78.95560, 'WB': 87.09422, 'UN': 0.0}

states_pop = {'AN': 397000, 'AP': 52221000, 'AR': 1504000, 'AS': 34293000, 'BR': 119520000, 'CH': 1179000, 'CT': 28724000, 'DL': 19814000, 'DN': 959000, 'GA': 1540000, 'GJ': 67936000, 'HP': 7300000, 'HR': 28672000, 'JH': 37403000, 'JK': 13203000, 'KA': 65798000, 'KL': 35125000, 'LA': 293000, 'LD': 68000, 'MH': 122153000, 'ML': 3224000, 'MN': 3103000, 'MP': 82232000, 'MZ': 1192000, 'NL': 2150000, 'OR': 43671000, 'PB': 29859000, 'PY': 1504000, 'RJ': 77264000, 'SK': 664000, 'TG': 37220000, 'TN': 75695000, 'TR': 3992000, 'UP': 224979000, 'UT': 11141000, 'WB': 96906000, 'UN': 0}

state_wise_throughout_all = state_wise_throughout

state_wise_throughout_all['state_name'] = state_wise_throughout['state_abbv'].map(state_name)
state_wise_throughout_all['longitude'] = state_wise_throughout['state_abbv'].map(states_longitude)
state_wise_throughout_all['latitude'] = state_wise_throughout['state_abbv'].map(states_latitude)
state_wise_throughout_all['population'] = state_wise_throughout['state_abbv'].map(states_pop)

overview_dataset = state_wise_throughout_all[['state_name','delta_confirmed', 'delta_recovered', 'delta_deceased', 'delta_tested', 'population']]

# print(state_wise_throughout_all.columns)                                                  

"""
Plotly graphs:
"""
state_wise_throughout_all_asc = state_wise_throughout_all.drop(state_wise_throughout_all.index[[-4]]).reset_index(drop=True)
state_wise_throughout_all_asc = state_wise_throughout_all_asc.sort_values(by='delta_confirmed', ascending=False)
delta_confirmed_graph = px.bar(state_wise_throughout_all_asc, x='delta_confirmed', y='state_name', barmode='group', color='population')
delta_confirmed_graph.update_layout(autosize=False, width=1000, height=890)

# For CRDT values in dash table:
crdt_data_table = state_wise_throughout_all_asc[['state_name', 'delta_confirmed', 'delta_recovered', 'delta_deceased', 'delta_tested']]

# For maps:
# state_map_graph = px.scatter_mapbox(state_wise_throughout_all_asc, 
#                         lat="latitude", 
#                         lon="longitude", 
#                         color="state_name", 
#                         size="delta_confirmed",
#                         color_continuous_scale=px.colors.cyclical.IceFire, 
#                         size_max=15, 
#                         zoom=1,
#                         mapbox_style="carto-positron")
# state_map_graph.update_layout(autosize=False, width=1000, height=760)

# """
# Compute the percentage of confirmed cases for population (ratio of confirmed to total state population)
# """
# state_wise_throughout_all_asc['pop_total_confirmed_%'] = (state_wise_throughout_all_asc['confirmed_total'] / state_wise_throughout_all_asc['population']) * 100
# state_wise_throughout_all_asc.sort_values(by='pop_total_confirmed_%', ascending=False)

"""
Bar chart using Plotly - pop VS fully vaccinated for state-wise:
"""
# Computing ration of total confirmed cases of each states population:
state_wise_throughout_high_pop = state_wise_throughout.query('population >= 30000000')
state_wise_throughout_high_pop = state_wise_throughout_high_pop.reset_index()
state_wise_throughout_high_pop = state_wise_throughout_high_pop[['state_name', 
                                                                 'population', 
                                                                 'delta_confirmed', 
                                                                 'delta_recovered', 
                                                                 'delta_deceased', 
                                                                 'delta_tested', 
                                                                 'delta_vaccinated1', 
                                                                 'delta_vaccinated2']]
state_wise_throughout_high_pop['pop_total_confirmed_%'] = (state_wise_throughout_high_pop['delta_confirmed'] / state_wise_throughout_high_pop['population']) * 100
state_wise_throughout_high_pop = state_wise_throughout_high_pop.sort_values(by='pop_total_confirmed_%', ascending=False).reset_index(drop=True)

pop_confirmed_ratio_graph = go.Figure()
pop_confirmed_ratio_graph.add_trace(go.Bar(
    x=state_wise_throughout_high_pop.state_name,
    y=state_wise_throughout_high_pop.population,
    name='State Population',
    marker_color='indianred'
))
pop_confirmed_ratio_graph.add_trace(go.Bar(
    x=state_wise_throughout_high_pop.state_name,
    y=state_wise_throughout_high_pop.delta_vaccinated2,
    name='Fully vaccinated population',
    marker_color='lightsalmon'
))

# Here we modify the tickangle of the xaxis, resulting in rotated labels.
pop_confirmed_ratio_graph.update_layout(barmode='group', 
                  xaxis_tickangle=-45, 
                  title='Visual ratio of populated states (more/equals to 30M) VS fully vaccinated population')

# """
# Line graph for each state in 2020:
# """
# covid_total_cases_2020 = state_wise_throughout_all.query('year == 2020')
# fig_line = px.line(covid_total_cases_2020, x="month", y="delta_confirmed", color='state_name', title="layout.hovermode='closest' (the default)")
# fig_line.update_traces(mode="markers+lines")

# """
# State-wise 2021 - total confirmed cases:
# """
# covid_total_cases_2021 = state_wise_throughout_all.query('year == 2021')
# covid_total_cases_2021 = covid_total_cases_2021.groupby('state_name').agg({'delta_confirmed': 'sum', 'month': 'count'})
# covid_total_cases_2021 = covid_total_cases_2021.sort_values(by='delta_confirmed', ascending=False).reset_index()

# graph_2021 = px.bar(covid_total_cases_2021, 
#        x="delta_confirmed", 
#        y="state_name", 
#        title="Total Confirmed Covid cases in 2021 state-wise", 
#        color="delta_confirmed", 
#        hover_data=['month'],
#        barmode='group')

"""
App's Layout
"""
layout = html.Div([
    html.H1('Social impacts Analysis'),
    dcc.Markdown('''
    > #### Overview of the dataset:

    Please note: **'delta_confirmed'** field in the below graphs are Total Confirmed Cases throughout since March 2020 unless date is mentioned.

    '''),
    html.A("Real-time datasource", href=data_source_url, target="_blank", style={'fontSize': '1.5rem'}),
    html.Br(),
    html.A("Real-time population datasource", href=pop_data_source_url, target="_blank", style={'fontSize': '1.5rem'}),
    dash_table.DataTable(
        id='statewise_vaccines_table',
        columns=[{"name": col, "id": col} for col in overview_dataset.columns],
        data=overview_dataset.to_dict('records')[:10],
        style_header={
            # 'backgroundColor': 'white',
            'fontWeight': 'bold',
            'padding': '5px'
        },
        style_cell= {'padding': '5px'},
        style_table={'maxWidth': '100%'},

    ),
    html.Br(),

    dcc.Markdown('''
    > #### Total confirmed cases (state-wise) in India till date since March 2020:
    '''),
    dcc.Graph(
        id='delta-confirmed-graph',
        figure=delta_confirmed_graph
    ),
    html.Br(),

    # dcc.Markdown('''
    # > #### India state-wise total confirmed cases till date:
    # '''),
    # html.P('Note: Higher the total confirmed cases larger the size of the marker.'),
    # dcc.Graph(
    #     id='state-map-graph',
    #     figure=state_map_graph
    # )
    dcc.Markdown('''
    > #### Select a state for text information about confirmed, recovered, deceased and tested factors:
    '''),
    dcc.Dropdown(
        id='states-list',
        options = [{'label': state, 'value': state} for state in state_wise_throughout_all['state_name']],
        value = 'Maharashtra'
    ),
    html.Br(),
    html.P(id='state-info-container', children=[], style={'fontWeight': 'bold'}),

    html.Br(),
    dcc.Markdown('''
    > ### State-wise covid cases in table:

    '''),
    dash_table.DataTable(
        id='statewise_vaccines_table',
        columns=[{"name": col, "id": col} for col in crdt_data_table.columns],
        data=crdt_data_table.to_dict('records'),
        style_header={
            # 'backgroundColor': 'white',
            'fontWeight': 'bold',
            'padding': '5px'
        },
        style_cell= {'padding': '5px'},
        style_table={'maxWidth': '100%'},
    ),

    html.Br(),
    dcc.Markdown('''
    > #### Graph-A: State population (>30M) VS Fully vaccinated:
    '''),
    dcc.Graph(
        id='pop_confirmed_ratio_graph',
        figure=pop_confirmed_ratio_graph
    ),

    # html.Br(),
    # dcc.Markdown('''
    # > #### State-wise Total Confirmed Cases in 2021:
    # '''),
    # dcc.Graph(
    #     id='fig_line',
    #     figure=fig_line
    # )

    dcc.Markdown('''
    > #### Inference / Summary:
    '''),
    dcc.Markdown(
        '''
        * **Overview of the Datasets** with their fields and factors.
        * **Total Confirmed cases**: This graph provides insight on each state with total confirmed cases since March 2020 till date.
        * **The dropdown feature**, helps to get the text information on total confirmed and deceased cases for selected state.
        * **State-wise covid cases in table** provides, info on all covid cases of total confirmed, deceased, recovered and tested.
        * **Graph-A**: provides, visual ratio of the state population versus fully vaccinated population that helps to provide herd immunity for recovering socialization impacts in the communities.
        '''
    )

], className='container')

@app.callback(
    Output(component_id='state-info-container', component_property='children'),
    [Input(component_id='states-list', component_property='value')]
)
def display_info(value):
    total_delta_confirmed = state_wise_throughout_all.loc[state_wise_throughout_all['state_name'] == value]['delta_confirmed'].values[0]

    total_delta_deceased = state_wise_throughout_all.loc[state_wise_throughout_all['state_name'] == value]['delta_deceased'].values[0]
    # return ('Total confirmed cases for {}: {}'.format(value, total_delta_confirmed) + 
    #         'Total deceased for {}: {}'.format(value, total_delta_deceased))
    return(
        'Total confirmed cases for '+value+': '+str(total_delta_confirmed),
        '\nTotal deceased cases for '+value+': '+str(total_delta_deceased)
    )