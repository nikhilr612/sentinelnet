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
    Output("select-device", "options"),
    Output("select-device", "value"),
    Input("refresh-devices", 'n_clicks')
)
def refresh_devices(n_clicks):
    ctx = dash.callback_context
    name = None
    options = []
    prop_id = ctx.triggered_id
    if prop_id == 'refresh-devices' and n_clicks > 0:
        for dev in r.keys():
            options.append({"label": dev.decode(), "value": dev.decode()})
    return options, name


@callback(
    Output("select-file", "options"),
    Output("select-file", "value"),
    Input("select-device", "value"),
)
def load_data(dev):
    name = None
    options = []
    for attr in {'cpu_usage', 'mem_usage', 'disk_read', 'disk_write'}:
        options.append({"label": attr, "value": attr})
    return options, name


@callback(
    Output("violations-state", "data"),
    Output("violations-table", "children"),
    Output("violations-exception-modal", "is_open"),
    Output("violations-exception-modal-content", "children"),
    [Input("violations-btn", "n_clicks"),
     Input("violations-exception-modal-close", "n_clicks")],
    [State("select-device",
                                          "value"), State("violations-state", "data")],
    running=[(Output("violations-btn", "disabled"), True, False),
             (Output("violations-cancel-btn", "disabled"), False, True)],
    cancel=[Input("violations-cancel-btn", "n_clicks")],
    background=True,
    manager=file_manager.get_long_callback_manager(),
    prevent_initial_call=True,
)
def click_run(btn_click, modal_close, device, data):
    ctx = dash.callback_context
    stats = json.loads(data) if data is not None else {}

    data_table = DataAnalyzer.get_data_table(df=None)

    modal_is_open = False
    modal_content = ""

    prop_id = ctx.triggered_id
    if prop_id == "violations-btn" and btn_click > 0:
        try:
            assert device, "Please select a device to monitor."
            df = DataAnalyzer().load_data(device, 'processes')
            stats = DataAnalyzer.get_stats(df)
            data_table = DataAnalyzer.get_data_table(df)

        except Exception:
            error = traceback.format_exc()
            modal_is_open = True
            modal_content = error
            logger.error(error)

    return json.dumps(stats, cls=DefaultEncoder), data_table, modal_is_open, modal_content


@callback(Output("violations-download", "options"), Input("violations-download-parent", "n_clicks"))
def select_download_parent(n_clicks):
    options = []
    ctx = dash.callback_context
    prop_id = ctx.triggered_id
    if prop_id == "violations-download-parent":
        models = file_manager.get_model_list()
        options += [{"label": s, "value": s} for s in models]
    return options


@callback(
    # Output("download-data", "data"),
    Output("violations-download-exception-modal", "is_open"),
    Output("violations-download-exception-modal-content", "children"),
    [Input("violations-download-btn", "n_clicks"),
     Input("violations-download-exception-modal-close", "n_clicks")],
    State("violations-download", "value"),
    running=[(Output("violations-download-btn", "disabled"), True, False)],
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
    if prop_id == "violations-download-btn" and btn_click > 0:
        try:
            assert model, "Please select the model to download."
            path = file_manager.get_model_download_path(model)
            data = dcc.send_file(path)
        except Exception:
            error = traceback.format_exc()
            modal_is_open = True
            modal_content = error
            logger.error(error)

    return modal_is_open, modal_content
