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

from Zerion_parser import Zerion_parser

es = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=es)


Strong_Data = Zerion_parser("/Users/eamonmcandrew/Desktop/Portfolio_tools/StrongBlock/0x3598f618d45e02b92d9b4d8129d45dbd1b0beb5d transactions 01_14_2022 14_18 from Zerion.csv")


Price_df = pd.read_csv ("/Users/eamonmcandrew/Desktop/Portfolio_tools/StrongBlock/strong-usd-max.csv")
Price_df = Price_df.rename(columns={"snapped_at": "Date"})

Node_creation_df = Strong_Data.Node_creation_transactions
Node_creation_df_display = Strong_Data.Node_creation_transactions_display

 
Claim_data = Strong_Data.Claims_df
Claim_data_df_display = Strong_Data.Claims_display


Price_df['Date'] = pd.to_datetime(Price_df['Date'])
Price_df.Date = Price_df.Date.apply(lambda x: x.date())

Node_creation_df = Node_creation_df.set_index('Date')
Price_df = Price_df.set_index('Date')

Claim_data["Date"] = pd.to_datetime(Claim_data["Date"])
Claim_data = Claim_data.set_index("Date")


Price_data = Price_df
Node_creation_df = Node_creation_df.merge(Price_df, left_index=True, right_index=True, how='inner')
Claim_data = Claim_data.merge(Price_df, left_index=True, right_index=True, how='inner')





fig = go.Figure([go.Scatter(x=Price_data.index, y=Price_data['price'], line_color="black",  name = "Strong Price")])
fig.add_traces(go.Scatter(x=Node_creation_df.index, y=Node_creation_df['price'],name = "Node Creation",
                          textposition='top left',
                          textfont=dict(color='#233a77'),
                          opacity=0.6,
                          mode='markers+text',
                          marker=dict(color='#AB63FA', size=8),
                        #   text = Node_creation_df["tgl"])
                        )),
fig.add_traces(go.Scatter(x=Claim_data.index, y=Claim_data['price'],name = "Rewards Claimed",
                          textposition='top left',
                          textfont=dict(color='#233a77'),
                          opacity=0.6,
                          mode='markers+text',
                          marker=dict(color='#19D3F3', size=8),
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
 


app.layout = html.Div([
    html.H1(children='StrongBlock Asset Manager'),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
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
    html.Div(id="output-line-plot")
    html.Div('output-datatable')
])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])



@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))


if __name__ == '__main__':
    app.run_server(debug=True)