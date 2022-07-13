import dash
from dash import dcc 
from dash import html 
import plotly.graph_objs as go 
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime
import pandas as pd 


app = dash.Dash()

nsdq = pd.read_csv('assets/data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol',inplace=True)
options = []
for tic in nsdq.index:
    # {'label':'user sees','value':'script sees'}
    mydict = {}
    mydict['label'] = nsdq.loc[tic]['Name'] + ' ' + tic # Apple Co. APPL
    mydict['value'] = tic
    options.append(mydict)


app.layout = html.Div([
                html.H1('Stock Price Dashboard of NASDAQ'),
                html.Div([
                    html.H3('Enter a stock symbol:',style={'paddingRight':'30px'}),
                    dcc.Dropdown(
                                id='my_ticker_symbol',
                                options = options,
                                value=['TSLA'], # sets a default value
                                multi=True
                    )
                ], style={'display':'inline-block','verticalAlign':'top','width':'30%'}),
                html.Div([
                    html.H3('Select a Start and End date:'),
                    dcc.DatePickerRange(
                        id='my_date_picker',
                        min_date_allowed=datetime(2015,1,1),
                        max_date_allowed=datetime.today(),
                        start_date=datetime(2018,1,1),
                        end_date=datetime.today()
                    )
                ], style={'display':'inline-block'}),
                html.Div([
                    html.Button(
                        id='submit-button',
                        n_clicks=0,
                        children='Submit',
                        style={'fontSize':24,'marginLeft':'30px'}
                    ),
                ], style={'display':'inline-block'}),
                dcc.Graph(id='my_graph')
            ])


@app.callback(Output('my_graph', 'figure'),
            [Input('submit-button', 'n_clicks')],
            [State('my_ticker_symbol', 'value'),
                State('my_date_picker', 'start_date'),
                State('my_date_picker', 'end_date')
            ])
def update_graph(n_cliks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')

    traces = []
    for tic in stock_ticker:
        df = web.get_data_tiingo(tic, start, end, api_key="d424b9c3d555167e344179e4531a2298f2987d16")
        traces.append({'x': df.index.get_level_values(1), 'y': df.close, 'name': tic})
        
    # layout = go.Layout(title='Stock Price (USD) vs Date')

    fig = go.Figure(data = traces)

    # Edit the layout
    fig.update_layout(
        title = 'Stock Price (USD) vs Date',
        xaxis_title='Price in USD',
        yaxis_title='Time in Date'
    )
    return fig

if __name__ == '__main__':
    app.run_server()
