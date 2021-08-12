# import dash
# import dash_table
# from dash.dependencies import Input, Output
# import dash_core_components as dcc
# import dash_html_components as html
# import pandas as pd
# import plotly.graph_objects as go
# import plotly.express as px
# import pathlib
# from app import app

# # ext_styles = ['../assets/css/bWLwgP.css']

# # app = dash.Dash(
# #     __name__,
# #     external_stylesheets=ext_styles,
# #     meta_tags=[{"name": "viewport", "content": "width=device-width"}]
# # )

# # server = app.server

# # get relative data folder
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("../datasets").resolve()

# vaccines_exports_df = pd.read_csv(DATA_PATH.joinpath("india_vacci_export_metrics.csv"))
# fig = px.bar(vaccines_exports_df, x='total_supplies', y='country', barmode='group')
# fig.update_layout(autosize=False, width=1000, height=890)

# # For maps:
# map_graph = px.scatter_mapbox(vaccines_exports_df, 
#                         lat="latitude", 
#                         lon="longitude", 
#                         color="country", 
#                         size="total_supplies",
#                         color_continuous_scale=px.colors.cyclical.IceFire, 
#                         size_max=15, 
#                         zoom=1,
#                         mapbox_style="carto-positron")
# map_graph.update_layout(autosize=False, width=1000, height=760)                        

# """
# App's Layout
# """
# layout = html.Div([
#     html.H1('Covid vaccines export by India'),
#     html.A("Datasource", href='https://www.mea.gov.in/vaccine-supply.htm', target="_blank", style={'fontSize': '1.5rem'}),
#     dcc.Markdown('''
#     > #### Overview of the dataset:
#     '''),
#     dash_table.DataTable(
#         id='df_table',
#         columns=[{"name": col, "id": col} for col in vaccines_exports_df.columns],
#         data=vaccines_exports_df.to_dict('records')[:10],
#         style_header={
#             # 'backgroundColor': 'white',
#             'fontWeight': 'bold'
#         }
#     ),

#     dcc.Markdown('''
#     > #### Countries and Total supplies:
#     '''),
#     dcc.Graph(
#         id='exports-graph',
#         figure=fig
#     ),

#     dcc.Markdown('''
#     > #### Countries and total covid vaccines supplied (hover over the markers on the map)
#     '''),
#     html.P('Note: marker size are based on the quantity of supply - larger the supply bigger the size of the marker.'),
#     dcc.Graph(
#         id='maps-graph',
#         figure=map_graph
#     ),

#     dcc.Markdown('''
#     > #### Select a country from the below dropdown to get the text information about its total supply from India:
#     '''),
#     dcc.Dropdown(
#         id='countries-list',
#         options = [{'label': country, 'value': country} for country in vaccines_exports_df['country']],
#         value = 'India'
#     ),
#     html.Br(),
#     html.P(id='country-info-container', children=[]),

#     html.Br(),

#     dcc.Markdown('''
#     > #### Inference/Summary:
#     '''),
#     dcc.Markdown(
#         '''
#         * Provides Overview of the Dataset.
#         * Graph-1: Visual graph of the total covid vaccines supplied to countries in descending order.
#         * Graph-2: Map view of the world with countries to which India has exported covid vaccines. If you hover on the markers on the map, that displays quantities in the pop-up box. Note, the larger the size of marker higher the quantities supplied.
#         * Fact about the total supplies made from India by selecting specific country from dropdown list.
#         '''
#     )
# ], className='container')

# @app.callback(
#     Output(component_id='country-info-container', component_property='children'),
#     [Input(component_id='countries-list', component_property='value')]
# )
# def display_info(value):
#     export_quantity = vaccines_exports_df.loc[vaccines_exports_df['country'] == value]['total_supplies'].values
#     return 'To "{}" country, {} total supplies were made by India'.format(value, export_quantity)
