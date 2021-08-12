import dash
# import flask

ext_styles = ['assets/css/bWLwgP.css']

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True, meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}], external_stylesheets=ext_styles)

# server = app.server()
# server = flask.Flask(__name__)
server = app.server