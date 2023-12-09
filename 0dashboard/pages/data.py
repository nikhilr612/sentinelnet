#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
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
        id="data-stats",
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
            html.P("Select Data File"),
            dcc.Dropdown(id="select-file", options=[], style={"width": "100%"}),
            html.Br(),
            html.P("Overall Stats"),
            html.Div(id="data-stats-table", children=[create_metric_stats_table()]),
            html.Br(),
            html.P("Per-Variable Stats"),
            html.Div(
                id="select-column-parent",
                children=[dcc.Dropdown(id="select-column", options=[], style={"width": "100%"})],
            ),
            html.Br(),
            html.Div(id="metric-stats-table", children=[create_stats_table()]),
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


def create_right_column() -> html.Div:
    return html.Div(
        id="right-column-data",
        children=[
            html.Div(
                id="result_table_card",
                children=[
                    html.B("Time Series Plots"),
                    html.Hr(),
                    html.Div(id="data-plots", children=[create_empty_figure()]),
                ],
            ),
            html.Div(
                id="result_table_card", children=[html.B("Time Series Samples"), html.Hr(), html.Div(id="data-table")]
            ),
        ],
    )


def create_data_layout() -> html.Div:
    return html.Div(
        id="data_views",
        children=[
            # Left column
            html.Div(id="left-column-data", className="three columns", children=[create_control_panel()]),
            # Right column
            html.Div(className="nine columns", children=create_right_column()),
        ],
    )
