import base64
import datetime
import io
import time
from datetime import date
import dash
import dash_auth
from dash.dependencies import Input, Output, State
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

from UI import navbar, help_info
from figPlot import PLOT

VALID_USERNAME_PASSWORD_PAIRS = {
    'ryan': 'dish',
    'nikhil': 'dish',
    'rohit': 'dish',
    'josh': 'dish',
    'levi': 'dish'
}

# TO DO
""" 1. Make faster by using .jpeg 
    2. Show PDF report history list 
    3. Report customization """

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Dish KPI Report Tool'
server = app.server


app.layout = dbc.Container([
    # Nav Bar
    dbc.Row([navbar]),
    # Main Page Container
    dbc.Container([
        dbc.Row([
            dbc.Col([help_info], width=6),
            dbc.Col([
                html.Div(className='mt-4', children=[
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
                            'margin': '0px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=True
                    ),
                    html.Div(id='output-data-upload'),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=html.Div(id="menu-output")
                    )
                ])
            ], width=6)
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Loading(
                    id="loading-2",
                    type="default",
                    children=html.Div(id="menu-2-output")
                )], width=12)
        ])
    ])
], fluid=True)

df_array = []


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
            if "Voice Call" in df:
                df_voice = df
                df_array.append(df_voice)
            elif "5G KPI Total Info Layer1 PDSCH Throughput [Mbps]" in df:
                df_data = df
                df_array.append(df_data)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div(className='mt-4', children=[
        # HTML UL Item
        html.H5(filename),
        html.P(datetime.datetime.fromtimestamp(date)),
        html.Hr(),  # horizontal line
    ])


@app.callback(Output('output-data-upload', 'children'),
              Output('menu-output', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in zip(list_of_contents, list_of_names, list_of_dates)
        ]
        return children, dbc.Row([
            dbc.Col([
                html.P("Set Report Titles & Name"),
                dcc.Input(id="name", type="text", placeholder="Report Name")
            ], width=4),
            dbc.Col([
                html.P("Enter Report Date"),
                dcc.DatePickerSingle(
                    id='date',
                    min_date_allowed=date(2022, 9, 18),
                    max_date_allowed=date(2023, 9, 18),
                    initial_visible_month=date(2022, 9, 19),
                    date=date(2022, 9, 19)
                )
            ], width=4),
            dbc.Col([
                html.P("Generate Report Output"),
                html.Button('Generate Report', className='btn btn-primary', id='generate', n_clicks=0)
            ], width=4)
        ])
    else:
        return False, False


@app.callback(
    Output('menu-2-output', 'children'),
    Input('generate', 'n_clicks'),
    State("name", "value"),
    State('date', 'date'))
def download(n_clicks, value, date):
    if n_clicks > 0:
        print(str(value) + " " + str(date))
        PLOT(df_array, str(value) + " " + str(date))
        time.sleep(1)
        return html.Div(className='mt-4', children=[
            html.Hr(),
            html.H5(str(value) + " " + str(date) + ".pdf", className='mt-4'),
            html.P("SAVED!")
        ]
                    )
    else:
        return False


@app.callback(Output('credits', 'displayed'),
              Input('credits-input', 'n_clicks'))
def display_confirm(n_clicks):
    if n_clicks  > 0:
        return True
    return False


if __name__ == '__main__':
    app.run_server(debug=False)
