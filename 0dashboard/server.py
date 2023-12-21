#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import dash
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import logging

from utils.layout import create_banner, create_layout
from pages.data import create_data_layout
from pages.anomaly import create_anomaly_layout
from pages.violations import create_violations_layout

from callbacks import data
from callbacks import anomaly
from callbacks import violations

logging.basicConfig(
    format="%(asctime)s (%(module)s:%(lineno)d) %(levelname)s: %(message)s", level=logging.INFO)


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport",
                "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[
        dbc.themes.LUX, "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"],
    title="SentinelNet Dashboard",
)
app.config["suppress_callback_exceptions"] = True
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content"),
        dcc.Store(id="data-state"),
        dcc.Store(id="anomaly-state"),
        dcc.Store(id="forecasting-state"),
        dcc.Store(id="violations-state"),
    ], className='dbc')
server = app.server


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def _display_page(pathname):
    return html.Div(id="app-container", children=[create_banner(app), html.Br(), create_layout()])


@app.callback(
    Output("plots", "children"),
    Input("tabs", "value"),
    [State("data-state", "data"), State("anomaly-state", "data"),]
)
def _click_tab(tab, data_state, anomaly_state):
    if tab == "file-manager":
        return create_data_layout()
    elif tab == "anomaly":
        return create_anomaly_layout()
    elif tab == "violations":
        return create_violations_layout()
