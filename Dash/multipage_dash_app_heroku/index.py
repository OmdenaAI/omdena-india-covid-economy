import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import home, vaccines_stats, covid_social_factors

app.layout = html.Div([
    dcc.Location(id='url', refresh=False, pathname='/'),
    html.Nav([
        dcc.Link('Welcome | ', href='/apps/home'),
        dcc.Link('Covid Vaccines Stats | ', href='/apps/vaccines_stats'),
        # dcc.Link('Covid Vaccines Export | ', href='/apps/vacci_exports'),
        dcc.Link('Covid Social Analysis', href='/apps/covid_social_factors')
    ], className="row", style={'padding':'5px 5px', 'margin':'20px auto', 'borderWidth':'2px 0 2px 0', 'borderStyle': 'solid', 'border-color': 'coral', 'textAlign': 'center'}),
    html.Img(src=app.get_asset_url('../assets/imgs/OmdenaLogoHeight330.png'), style={'maxWidth':'100%', 'height': 'auto'}),
    html.Div(id='page-content', children=[]),
    html.Hr(),
    html.Div([
        html.Footer([
            dcc.Markdown('''
            **Leveraging AI to analyse Socio-Economic impacts due to covid19 in India, June-Aug 2021**
            '''),
            html.A('Omdena India Chapter', href='https://omdena.com/omdena-chapter-page-india/', target='_blank', style={'fontSize': 9}),
            html.P('All the contents are copyright protected')
        ])
        # html.Link('Omdena India Chapter', href='https://omdena.com/omdena-chapter-page-india/')
    ], style={'textAlign': 'center', 'margin': '1rem 1rem 0 1rem'})
], className='container')
# , style={'height':'20%', 'width':'20%'}

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/home' or pathname == '/':
        return home.layout
    elif pathname == '/apps/vaccines_stats':
        return vaccines_stats.layout
    # if pathname == '/apps/vacci_exports':
    #     return vacci_exports.layout
    elif pathname == '/apps/covid_social_factors':
        return covid_social_factors.layout
    else:
        # return "404 Page Error! Please choose a link"
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=False)
