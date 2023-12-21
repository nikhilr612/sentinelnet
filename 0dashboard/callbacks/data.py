#
# Copyright (c) 2023 salesforce.com, inc.
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause
# For full license text, see the LICENSE file in the repo root or https://opensource.org/licenses/BSD-3-Clause
#
import json
import logging
import os
import traceback
import redis
import numpy as np

import dash
from dash import Input, Output, State, callback, dcc
from pages.data import create_stats_table, create_metric_stats_table
from utils.file_manager import FileManager
from models.data import DataAnalyzer

logger = logging.getLogger(__name__)
file_manager = FileManager()
r = redis.Redis(host='localhost', port=6379, db=0)


class DefaultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return str(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)

@callback(
    Output("data-select-device", "options"),
    Output("data-select-device", "value"),
    Input("data-refresh-devices", 'n_clicks')
)
def refresh_devices(n_clicks):
    ctx = dash.callback_context
    name = None
    options = []
    prop_id = ctx.triggered_id
    if prop_id == 'data-refresh-devices' and n_clicks>0:
        for dev in r.keys():
            options.append({"label": dev.decode(), "value": dev.decode()})
    return options, name

@callback(
    Output("data-select-file", "options"),
    Output("data-select-file", "value"),
    Input("data-select-device", "value"),
)
def load_data(dev):
    name = None
    options = []
    for attr in {'cpu_usage', 'mem_usage', 'disk_read', 'disk_write'}:
        options.append({"label": attr, "value": attr})
    return options, name


@callback(
    Output("data-stats-table", "children"),
    Output("data-state", "data"),
    Output("data-table", "children"),
    Output("data-plots", "children"),
    Output("data-exception-modal", "is_open"),
    Output("data-exception-modal-content", "children"),
    [Input("data-btn", "n_clicks"), Input("data-exception-modal-close", "n_clicks")],
    [State("data-select-file", "value"), State("data-select-device", "value"), State("data-state", "data")],
    running=[(Output("data-btn", "disabled"), True, False), (Output("data-cancel-btn", "disabled"), False, True)],
    cancel=[Input("data-cancel-btn", "n_clicks")],
    background=True,
    manager=file_manager.get_long_callback_manager(),
)
def click_run(btn_click, modal_close, attr, device, data):
    ctx = dash.callback_context
    stats = json.loads(data) if data is not None else {}

    stats_table = create_stats_table()
    data_table = DataAnalyzer.get_data_table(df=None)
    data_figure = DataAnalyzer.get_data_figure(df=None)
    modal_is_open = False
    modal_content = ""

    prop_id = ctx.triggered_id
    if prop_id == "data-btn" and btn_click > 0:
        try:
            assert attr, "Please select an attribute to load."
            assert device, "Please select a device to monitor."
            df = DataAnalyzer().load_data(device, attr)
            stats = DataAnalyzer.get_stats(df)
            stats_table = create_stats_table(stats)
            data_table = DataAnalyzer.get_data_table(df)
            data_figure = DataAnalyzer.get_data_figure(df)

        except Exception:
            error = traceback.format_exc()
            modal_is_open = True
            modal_content = error
            logger.error(error)

    return stats_table, json.dumps(stats, cls=DefaultEncoder), data_table, data_figure, modal_is_open, modal_content


@callback(Output("select-column", "options"), Input("select-column-parent", "n_clicks"), State("data-state", "data"))
def update_metric_dropdown(n_clicks, data):
    options = []
    ctx = dash.callback_context
    prop_id = ctx.triggered_id
    if prop_id == "select-column-parent":
        stats = json.loads(data)
        options += [{"label": s, "value": s} for s in stats.keys() if s.find("@") == -1]
    return options


@callback(Output("metric-stats-table", "children"), Input("select-column", "value"), State("data-state", "data"))
def update_metric_table(column, data):
    ctx = dash.callback_context
    metric_stats_table = create_metric_stats_table()

    prop_id = ctx.triggered_id
    if prop_id == "select-column":
        stats = json.loads(data)
        metric_stats_table = create_metric_stats_table(stats, column)
    return metric_stats_table


@callback(Output("data-download", "options"), Input("data-download-parent", "n_clicks"))
def select_download_parent(n_clicks):
    options = []
    ctx = dash.callback_context
    prop_id = ctx.triggered_id
    if prop_id == "data-download-parent":
        models = file_manager.get_model_list()
        options += [{"label": s, "value": s} for s in models]
    return options


@callback(
    Output("download-data", "data"),
    Output("data-download-exception-modal", "is_open"),
    Output("data-download-exception-modal-content", "children"),
    [Input("data-download-btn", "n_clicks"), Input("data-download-exception-modal-close", "n_clicks")],
    State("data-download", "value"),
    running=[(Output("data-download-btn", "disabled"), True, False)],
    background=True,
    manager=file_manager.get_long_callback_manager(),
    prevent_initial_call=True,
)
def click_run(btn_click, modal_close, model):
    ctx = dash.callback_context
    modal_is_open = False
    modal_content = ""
    data = None

    prop_id = ctx.triggered_id
    if prop_id == "data-download-btn" and btn_click > 0:
        try:
            assert model, "Please select the model to download."
            path = file_manager.get_model_download_path(model)
            data = dcc.send_file(path)
        except Exception:
            error = traceback.format_exc()
            modal_is_open = True
            modal_content = error
            logger.error(error)

    return data, modal_is_open, modal_content
