from turtle import width
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table

import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


import pandas as pd
from strong_utils import Zerion_parser
from strong_utils import get_price_to_date

es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=es)


Strong_Data = Zerion_parser("/Users/eamonmcandrew/Desktop/Portfolio_tools/StrongBlock/0x3598f618d45e02b92d9b4d8129d45dbd1b0beb5d transactions 01_20_2022 09_33 from Zerion.csv")




Node_creation_df = Strong_Data.Node_creation_transactions
Node_creation_df_display = Strong_Data.Node_creation_transactions_display

 
Claim_data = Strong_Data.Claims_df
Claim_data_df_display = Strong_Data.Claims_display



Node_creation_df["Date"] = pd.to_datetime(Node_creation_df["Date"])
Node_creation_df = Node_creation_df.set_index("Date")


Claim_data["Date"] = pd.to_datetime(Claim_data["Date"])
Claim_data = Claim_data.set_index("Date")



Price_df = get_price_to_date()

Node_creation_df = Node_creation_df.merge(Price_df, left_index=True, right_index=True, how='inner')
Claim_data = Claim_data.merge(Price_df, left_index=True, right_index=True, how='inner')

Price_data = Price_df 


fig = go.Figure([go.Scatter(x=Price_data.index, y=Price_data['price'], line_color="grey",  name = "Strong Price")])

fig.add_traces(go.Scatter(x=Claim_data.index, y=Claim_data['price'],name = "Rewards Claimed",
                          textposition='top left',
                          textfont=dict(color='#233a77'),
                          opacity=0.6,
                          mode='markers+text',
                          marker=dict(color='#19D3F3', size=8),
                        #   text = Node_creation_df["tgl"])
                        )),

fig.add_traces(go.Scatter(x=Node_creation_df.index, y=Node_creation_df['price'],name = "Node Creation",
                          textposition='top left',
                          textfont=dict(color='#233a77'),
                          opacity=0.6,
                          mode='markers+text',
                          marker=dict(color='#AB63FA', size=8),
                        #   text = Node_creation_df["tgl"])
                        ))

fig.update_layout(xaxis_title='Date', yaxis_title='Price in $')
fig.update_xaxes(
    rangeslider_visible=True,
    rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    )
)
 
app.layout = html.Div(children=[
    html.H1(children='StrongBlock Asset Manager'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop Zerion CSV or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-data-upload'),
    dcc.Graph(figure=fig),
    dash_table.DataTable(
    id='table',
    columns=[{"name": i, "id": i} for i in Node_creation_df_display.columns],
    data=Node_creation_df_display.to_dict('records'),
    fixed_rows={'headers': True},
    style_table={'height': 400} 
)

])
if __name__ == '__main__':
    app.run_server(debug=True)