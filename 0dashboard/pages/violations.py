import dash_bootstrap_components as dbc
from dash import dcc
from dash import html, dash_table
from pages.utils import create_modal, create_empty_figure
from settings import *


def create_stats_table(data_stats=None):
    if data_stats is None or len(data_stats) == 0:
        data = [{"Stats": "", "Value": ""}]
    else:
        data = [{"Stats": key, "Value": value} for key, value in data_stats["@global"].items()]

    table = dash_table.DataTable(
        id="violations-stats",
        data=data,
        columns=[{"id": "Stats", "name": "Stats"}, {"id": "Value", "name": "Value"}],
        editable=False,
        style_header_conditional=[{"textAlign": "center", "font-family": "Salesforce Sans"}],
        style_cell_conditional=[{"textAlign": "center", "font-family": "Salesforce Sans"}],
        style_header=dict(backgroundColor=TABLE_HEADER_COLOR, color="white"),
        style_data=dict(backgroundColor=TABLE_DATA_COLOR),
    )
    return table


def create_metric_stats_table(metric_stats=None, column=None):
    if metric_stats is None or len(metric_stats) == 0 or column not in metric_stats:
        data = [{"Stats": "", "Value": ""}]
    else:
        data = [{"Stats": key, "Value": value} for key, value in metric_stats[column].items()]

    table = dash_table.DataTable(
        id="metric-stats",
        data=data,
        columns=[{"id": "Stats", "name": "Stats"}, {"id": "Value", "name": "Value"}],
        editable=False,
        style_header_conditional=[{"textAlign": "center", "font-family": "Salesforce Sans"}],
        style_cell_conditional=[{"textAlign": "center", "font-family": "Salesforce Sans"}],
        style_header=dict(backgroundColor=TABLE_HEADER_COLOR, color="white"),
        style_data=dict(backgroundColor=TABLE_DATA_COLOR),
    )
    return table


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
                id="violations_table_card", children=[html.B("Violations Samples"), html.Hr(), html.Div(id="violations-table")]
            ),
            html.Br(),
            html.Div(
                children=[
                    dbc.Button(id="violations-btn", children="Load", n_clicks=0),
                    dbc.Button(id="violations-cancel-btn", children="Cancel", style={"margin-left": "15px"}),
                ],
                style={"textAlign": "center"},
            ),
            html.Br(),
            html.P("Download Trained Model"),
            html.Div(
                id="violations-download-parent",
                children=[dcc.Dropdown(id="violations-download", options=[], style={"width": "100%"})],
            ),
            html.Br(),
            html.Div(
                children=[
                    dbc.Button(id="violations-download-btn", children="Download", n_clicks=0),
                    dcc.Download(id="download-data"),
                ],
                style={"textAlign": "center"},
            ),
            html.Br(),
            create_modal(
                modal_id="violations-exception-modal",
                header="An Exception Occurred",
                content="An exception occurred. Please click OK to continue.",
                content_id="violations-exception-modal-content",
                button_id="violations-exception-modal-close",
            ),
            create_modal(
                modal_id="violations-download-exception-modal",
                header="An Exception Occurred",
                content="An exception occurred. Please click OK to continue.",
                content_id="violations-download-exception-modal-content",
                button_id="violations-download-exception-modal-close",
            ),
        ],
    )


def create_right_column() -> html.Div:
    return html.Div(
        id="right-column-data",
        children=[
            html.Div(
                id="result_table_card",
                children=[
                    html.B("Time Series Plots"),
                    html.Hr(),
                    html.Div(id="violations-plots", children=[create_empty_figure()]),
                ],
            ),
            html.Div(
                id="result_table_card", children=[html.B("Time Series Samples"), html.Hr(), html.Div(id="violations-table")]
            ),
        ],
    )


def create_violations_layout() -> html.Div:
    return html.Div(
        id="data_views",
        children=[
            # Left column
            html.Div(id="left-column-data", children=[create_control_panel()]),
            # Right column
            # html.Div(className="nine columns", children=create_right_column()),
        ],
    )
