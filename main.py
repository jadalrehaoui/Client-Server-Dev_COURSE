from jupyter_plotly_dash import JupyterDash
import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
from bson.json_util import dumps
import base64
# import AnimalShelter Model
from AnimalShelter import AnimalShelter
# Set username and password
username = "aacuser"
password = "jadrehaoui"
shelter = AnimalShelter(username, password)

# class read method must support return of cursor object 
df = pd.DataFrame.from_records(shelter.read())
# Getting distinct animal types to make the radio buttons
rescue_types = pd.DataFrame(df, columns=['rescue_type']).drop_duplicates(keep="last").dropna().append({'rescue_type': "Reset"}, ignore_index=True)
# app declaration and initialization
app = JupyterDash("SimpleExample")
# preparing the image and encoding it
image_filename = 'grazioso_logo.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
# starting the layout
app.layout = html.Div(
    [
        html.Div(id="hidden-div", style={'display': 'none'}),
        # the image in the center
        html.Center(
            html.Img(src="data:image/png;base64,{}".format(encoded_image.decode()), style={"width": "100px", "height": "100px"})
        ),
        # the header in the center
        html.Center(
            html.Center(
                html.H1('Credit to: Jad Alrehaoui')
            )
        ),
        html.Hr(),
        # radio buttons, all have the same id in order to listen to the value change
        dcc.RadioItems(id="radio-id", 
                       options=[
                           {'label': i, 'value': i} for i in rescue_types.get("rescue_type")
                       ], 
                       value='Reset'),
        html.Hr(),
        # data table starting here
        dash_table.DataTable(
            # ID and the data gotten from the database
            id='datatable-id', data=df.to_dict('records'),
            # specifying the columns we want to show.
            columns=[
                {'name': i, 'id': i, 'deletable': False, 'selectable': True} for i in df.columns
            ],
            # checking on and off features of the datatable
            editable=False,
            filter_action="native",
            row_selectable="single",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10 # 10 rows in a page.
            
        ),
        html.Br(),
        html.Hr(),
        # last section holding the Pie chart and the map
        html.Div(
            className="row",
            style={"display": "flex"},
            children=[
                # pie chart
                dcc.Graph(id="graph-id", className="col s12 m6"),
                # map
                html.Div(
                    id="map-id", 
                    className="col s12 m6",
                ), 
            ]
        ) 
    ]
)
# listening to radio buttons value change
# changing data in the databale
@app.callback(
    Output("datatable-id","data"),
    [Input("radio-id", "value")]
)
def radio_button_clicked(value):
    # if reset is checked
    if value == "Reset":
        # show all records no filter applied
        df = pd.DataFrame(list(shelter.read()))
    else:
        # show only data with filter applied
        df = pd.DataFrame(list(shelter.read({"rescue_type":value}))) 
    return df.to_dict('records')
    
@app.callback(
    Output('datatable-id', 'style_data_conditional'),
    [Input('datatable-id', 'selected_columns')]
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

# changing the pie chart data
# getting input from datatable
@app.callback(
    Output("graph-id", "figure"),
    [Input("datatable-id", "derived_viewport_data")]
)
def update_graph(viewData):
    # getting the data from dict to a DataFrame
    dff = pd.DataFrame.from_dict(viewData)
    # filtering breed to get distinct breed
    breeds = pd.DataFrame(viewData, columns=['breed']).drop_duplicates(keep="last").dropna().get('breed').to_numpy()
    # declaring percentages to be filled by calculating
    perc = []
    # filling perc
    for i in dff['breed'].value_counts(): 
        # formula applied
        perc.append(i/len(viewData))
    # constructing the fig to be shown
    fig = px.pie(dff, values=perc, names=breeds, hole=0)
    return fig

# changing map section
# listening to datatable 
@app.callback(
    Output('map-id', "children"),
    [
        Input('datatable-id', "derived_viewport_data")
    ]
)
def update_map(viewData):
    # data from dict to DataFrame
    dff = pd.DataFrame.from_dict(viewData)
    return [
                dl.Map(
                    id="map-update",
                    # specifying w and h
                    style={"width": "1000px", "height": "500px"},
                    # specifying where is the center of the map
                    center=[dff.iloc[1,13], dff.iloc[1,14]],
                    # specifying zoom
                    zoom=10,
                    children=[
                        dl.TileLayer(id="base-layer-id"),
                        # marker
                        dl.Marker(
                            id="marker-id",
                            # where is the marker pointing to
                            position=[dff.iloc[1,13], dff.iloc[1,14]],
                            children=[
                                # on hover
                                dl.Tooltip(dff.iloc[1,4]),
                                # on popup
                                dl.Popup([
                                    html.H1("Animal Name"),
                                    html.P(dff.iloc[1,9])
                                ])
                            ]
                        )
                    ]
                )
            ]



app
