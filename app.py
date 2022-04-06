import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
# from helpers.key_finder import api_key
# from helpers.api_call import *


########### Define a few variables ######

tabtitle = 'Show me the Coin'
sourceurl = 'http://api.coinlayer.com/api/live'
#sourceurl = 'https://www.kaggle.com/tmdb/tmdb-movie-metadata'
#sourceurl2 = 'https://developers.themoviedb.org/3/getting-started/introduction'
githublink = 'https://github.com/dpulluri/405-movie-reviews-api'



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout

app.layout = html.Div(children=[
    dcc.Store(id='tmdb-store', storage_type='session'),
    dcc.Store(id='summary-store', storage_type='session'),
    html.Div([
        html.H1(['Show me the Coin']),
        html.Div([
            html.Div([
                html.Div('Randomly select a movie summary'),
                html.Button(id='eek-button', n_clicks=0, children='API call', style={'color': 'rgb(255, 255, 255)'}),
                html.Div(id='movie-title', children=[]),
                html.Div(id='movie-release', children=[]),
                html.Div(id='movie-overview', children=[]),

            ], style={ 'padding': '12px',
                    'font-size': '22px',
                    # 'height': '400px',
                    'border': 'thick red solid',
                    'color': 'rgb(255, 255, 255)',
                    'backgroundColor': '#536869',
                    'textAlign': 'left',
                    },
            className='six columns'),

        ], className='twelve columns'),
        html.Br(),

    ], className='twelve columns'),


        # Output
    html.Div([
        # Footer
        html.Br(),
        html.A('Code on Github', href=githublink, target="_blank"),
        html.Br(),
        html.A("Data Source: coinlayer", href=sourceurl, target="_blank"),
        html.Br(),
    ], className='twelve columns'),



    ]
)

########## Callbacks

# TMDB API call
@app.callback(Output('tmdb-store', 'data'),
              [Input('eek-button', 'n_clicks')],
              [State('tmdb-store', 'data')])
def on_click(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate
    elif n_clicks==0:
        data = {'success': True,
 'terms': 'https://coinlayer.com/terms',
 'privacy': 'https://coinlayer.com/privacy',
 'timestamp': 1649199786,
 'target': 'USD',
 'rates': {'BTC': 46086.561278, 'ETH': 3441.073039}}
    elif n_clicks>0:
        data = api_pull()
    return data

@app.callback([Output('movie-title', 'children'),
                Output('movie-release', 'children'),
                Output('movie-overview', 'children'),
                ],
              [Input('tmdb-store', 'modified_timestamp')],
              [State('tmdb-store', 'data')])
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate
    else:
        #return data['title'], data['release_date'], data['overview']
        print(data)
        return data['target'], data['rates']['BTC'], data['rates']['ETH']

    
def api_pull():
    payload = {'access_key':'f994000dc1a1bc422a9d418df5cdb409', 'symbols':'BTC,ETH'}
    response = requests.get(sourceurl, params=payload).json()
    # json_file = json_normalize(response)
    # dictionary = json.load(response)
    return response
    # return df[['title', 'overview', 'release_date']]

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
