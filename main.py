import dash
import iex
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_design_kit as ddk

app = dash.Dash(__name__)
server = app.server
app.title = "AKDEL"

app.layout = ddk.App(children=[
    ddk.Block(ddk.ControlCard(width=100,rounded=True,
        children=[ddk.ControlItem(children=[dcc.Dropdown(id="dropdown", options=iex.companies, value="AAPL"),
                                            ddk.ControlItem(width=50,children=[dcc.DatePickerRange(id="datepicker",start_date="2015-01-01",end_date="2016-01-01",display_format="YYYY-MM-DD")])])],



        )),
    ddk.Block(children=[ddk.DataCard(id="dc1", width=25, label="Dividend Yield", value="-"),
                        ddk.DataCard(id="dc2", width=25, label="Peg Ratio", value="-"),
                        ddk.DataCard(id="dc3", width=25, label="Beta", value="%"),
                        ddk.DataCard(id="dc4", width=25, label="Country", value="-"),
                        ]),
    ddk.Block(children=[ddk.Card(rounded=True, children=[ddk.Graph(id="graph", figure={
        "data": [go.Scatter(x=iex.get_prices("AAPL","2015-01-01","2016-01-01").index, y=iex.get_prices("AAPL","2015-01-01","2016-01-01")["Adj Close"])], "layout": go.Layout(xaxis={
            'showgrid': False
        },
            yaxis={
                'showgrid': False
            })
    }
                                                                   )])])

])



@app.callback([Output("graph", "figure"),Output("dc4", "value"),
               Output("dc3", "value"),
               Output("dc2", "value"),
               Output("dc1", "value")], [Input("dropdown", "value"),Input("datepicker","start_date"),Input("datepicker","end_date")])
def update_card1(value,start_date,end_date):
    profile = iex.get_company(value)
    return {"data":[go.Scatter(x=iex.get_prices(value,start_date,end_date).index, y=iex.get_prices(value,start_date,end_date)["Adj Close"])],"layout": go.Layout(xaxis={
        'showgrid': False
    },
        yaxis={
            'showgrid': False
        })}, profile["country"],profile["beta"],"{:,}".format(profile["pegRatio"]),profile["dividendYield"]



if __name__ == "__main__":
    app.run_server(port=8070)
