import dash
import dash_design_kit as ddk
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import requests
from datetime import datetime as dt
r = requests.get("https://financialmodelingprep.com/api/v3/quote/BTCUSD")


time = []
price = []



app = dash.Dash()

server=app.server

app.layout = ddk.App(children=[ddk.Card(ddk.Graph(id="graph")
),
dcc.Interval(id="liveupdate",interval=10000,n_intervals=0),

]

)

@app.callback(Output("graph","figure"),[Input("liveupdate","n_intervals")])
def gaph_update(n):

    price.append(requests.get("https://financialmodelingprep.com/api/v3/quote/BTCUSD").json()[0]["price"])
    time.append(dt.utcfromtimestamp(int(requests.get("https://financialmodelingprep.com/api/v3/quote/BTCUSD").json()[0]["timestamp"])).strftime('%H:%M:%S'))
    return {"data": [go.Scatter(x=time,y=price)],
            "layout": go.Layout(xaxis={
        'showgrid': False
    },
        yaxis={
            'showgrid': False
        })}






app.run_server(debug=True,port=8010)