import dash_bootstrap_components as dbc
from dash import dcc
from dash import html, dash_table
from pages.utils import create_modal, create_empty_figure
from settings import *

def create_control_panel() -> dbc.Container:
    return dbc.Container(
        id="control-card",
        children=[
            html.Br(),
            html.P("Select Device"),
            dcc.Dropdown(id="select-device", options=[], style={"width": "100%"}, className='dbc'),
            html.Br(),
            dbc.Button("Refresh Device List", id="refresh-devices", n_clicks=0),
            html.Br(),
            html.Div(
                children=[
                    dbc.Button(id="data-btn", children="Load", n_clicks=0),
                    dbc.Button(id="data-cancel-btn", children="Cancel", style={"margin-left": "15px"}),
                ],
                style={"textAlign": "center"},
            ),
            html.Br(),
            html.P("Download Trained Model"),
            html.Div(
                id="data-download-parent",
                children=[dcc.Dropdown(id="data-download", options=[], style={"width": "100%"})],
            ),
            html.Br(),
            html.Div(
                children=[
                    dbc.Button(id="data-download-btn", children="Download", n_clicks=0),
                    dcc.Download(id="download-data"),
                ],
                style={"textAlign": "center"},
            ),
            html.Br(),
            create_modal(
                modal_id="data-exception-modal",
                header="An Exception Occurred",
                content="An exception occurred. Please click OK to continue.",
                content_id="data-exception-modal-content",
                button_id="data-exception-modal-close",
            ),
            create_modal(
                modal_id="data-download-exception-modal",
                header="An Exception Occurred",
                content="An exception occurred. Please click OK to continue.",
                content_id="data-download-exception-modal-content",
                button_id="data-download-exception-modal-close",
            ),
        ],
    )

def create_violations_layout() -> html.Div:
    return html.Div(
        id="data_views",
        children=[
            html.Div(id="violations-table", children=[create_control_panel()])
        ],
    )
