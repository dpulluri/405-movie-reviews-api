import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import requests
import pandas as pd
# from helpers.key_finder import api_key
# from helpers.api_call import *


########### Define a few variables ######

tabtitle = 'Show me the Coin'
sourceurl = 'https://api.coingecko.com/api/v3/coins/markets'
#sourceurl = 'https://www.kaggle.com/tmdb/tmdb-movie-metadata'
#sourceurl2 = 'https://developers.themoviedb.org/3/getting-started/introduction'
githublink = 'https://github.com/dpulluri/405-movie-reviews-api'
ids='bitcoin,ethereum,solana,cardano,tether,ripple,dogecoin,litecoin'


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
                html.Div('Get all crypto coins data'),
                html.Button(id='eek-button', n_clicks=0, children='API call', style={'color': 'rgb(255, 255, 255)'}),
                html.Div(id='movie-title', children=[]),

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
  #   elif n_clicks==0:
  #       data = [{'id': 'bitcoin',
  # 'symbol': 'btc',
  # 'name': 'Bitcoin',
  # 'image': 'https://assets.coingecko.com/coins/images/1/large/bitcoin.png?1547033579',
  # 'current_price': 45238,
  # 'market_cap': 859441924088,
  # 'market_cap_rank': 1,
  # 'fully_diluted_valuation': 949715503157,
  # 'total_volume': 27812502144,
  # 'high_24h': 47077,
  # 'low_24h': 44787,
  # 'price_change_24h': -1447.797400405951,
  # 'price_change_percentage_24h': -3.10117,
  # 'market_cap_change_24h': -25413045157.389893,
  # 'market_cap_change_percentage_24h': -2.872,
  # 'circulating_supply': 19003881.0,
  # 'total_supply': 21000000.0,
  # 'max_supply': 21000000.0,
  # 'ath': 69045,
  # 'ath_change_percentage': -34.49968,
  # 'ath_date': '2021-11-10T14:24:11.849Z',
  # 'atl': 67.81,
  # 'atl_change_percentage': 66594.01963,
  # 'atl_date': '2013-07-06T00:00:00.000Z',
  # 'roi': None,
  # 'last_updated': '2022-04-06T01:43:30.093Z'}]
    elif n_clicks>0:
        data = api_pull()
    return data

@app.callback([Output('movie-title', 'children'),
                #Output('movie-release', 'children'),
                #Output('movie-overview', 'children'),
                ],
              [Input('tmdb-store', 'modified_timestamp')],
              [State('tmdb-store', 'data')])
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate
    else:
        #return data['title'], data['release_date'], data['overview']
        #print(data)
        df= pd.DataFrame.from_records(data)
        table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
        return table

    
def api_pull():
    payload = {'vs_currency':'usd','ids':ids}
    response = requests.get(sourceurl, params=payload).json()
    # json_file = json_normalize(response)
    # dictionary = json.load(response)
    return response
    # return df[['title', 'overview', 'release_date']]

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
