#!/usr/bin/env python

import argparse
import os
import logging
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import json
from .talp_common import (
    render_template,
    TALP_PAGES_TEMPLATE_PATH,
    TALP_METRIC_TO_NAME_MAP,
    TALP_PAGES_DEFAULT_REGION_NAME,
    TALP_JSON_POP_METRICS_KEY,
    TALP_JSON_TIMESTAMP_KEY,
    TALP_JSON_METADATA_KEY,
)
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import uuid
from plotly import colors as pcolors

from typing import List


@dataclass
class RunFolder:
    """Class for representing a Folder with a bunch of JSON files that will be all rendered on one html"""

    relative_path: Path
    jsons: List[Path]


@dataclass
class TalpPage:
    """Class for representing a Result page for a runfolder instance"""

    run_folder: RunFolder
    output_path: Path
    html: str


def sample_colorscale(colorscale, num_samples):
    """
    Samples a Plotly color scale and returns a list of discrete colors.

    Parameters:
    colorscale (list or str): The Plotly color scale to sample. It can be a predefined string or a custom color scale list.
    num_samples (int): The number of colors to sample from the color scale.

    Returns:
    list: A list of sampled colors in hexadecimal format.
    """
    if isinstance(colorscale, str):
        colorscale = pcolors.get_colorscale(colorscale)

    # Ensure the colorscale is normalized to [0, 1]
    colorscale = [
        (i / (len(colorscale) - 1), color) for i, color in enumerate(colorscale)
    ]

    # Generate the samples
    samples = [
        colorscale[int(i * (len(colorscale) - 1) / (num_samples - 1))][1]
        for i in range(num_samples)
    ]

    return samples


def find_run_folders(base_path: Path) -> List[RunFolder]:
    run_folders = []

    for root, dirs, files in os.walk(base_path):
        json_files = [Path(root) / file for file in files if file.endswith(".json")]
        if json_files:
            relative_root = Path(root).relative_to(base_path)
            run_folders.append(RunFolder(relative_path=relative_root, jsons=json_files))

    return run_folders


def _verify_input(args):
    path = None

    # Check if the JSON file exists
    if os.path.exists(args.path):
        found_a_json = False
        for _, _, filenames in os.walk(args.path):
            for _ in [f for f in filenames if f.endswith(".json")]:
                found_a_json = True

        if not found_a_json:
            logging.error(
                f"The specified path '{args.path}' doesnt contain any .json files "
            )
            raise Exception("Path empty of .json files")
    else:
        logging.error(f"The specified path '{args.path}' does not exist.")
        raise Exception("Not existing path")

    # Check if output is empty

    if os.path.exists(args.output):
        if len(os.listdir(args.output)) != 0:
            logging.error(f"The specified output folder '{args.output}' is not empty")
            raise Exception("Non Empty output path")

    path = args.path
    output = args.output

    return path, output


def get_time_series_html(run_folder):
    # small helper funtion to return the Scatter graph option
    def _get_scatter(df, region, metric, color, show_legend=False):
        return go.Scatter(
            x=df[df["name"] == region]["timestamp"],
            y=df[df["name"] == region][metric],
            text=df[df["name"] == region]["metadata"],
            mode="lines+markers",
            name=region,
            legendgroup=region,
            showlegend=show_legend,
            marker_color=color[1],
            line=dict(color=color[1]),
            visible=True if region == TALP_PAGES_DEFAULT_REGION_NAME else "legendonly",
            # hovertemplate='%{text}'),
        )

    dfs = []
    for json_entry in run_folder.jsons:
        with open(json_entry) as file:
            run_json = json.load(file)
            df_single = pd.DataFrame(run_json[TALP_JSON_POP_METRICS_KEY])
            df_single = df_single.assign(
                timestamp=pd.to_datetime(run_json[TALP_JSON_TIMESTAMP_KEY])
            )
            df_single = df_single.assign(metadata=run_json[TALP_JSON_METADATA_KEY])
            # Normalize to seconds
            df_single["elapsedTime"] = df_single["elapsedTime"] * 1e-9
            df_single = df_single.sort_values(by=["elapsedTime"], ascending=False)
            dfs.append(df_single)

    combined_df = pd.concat(dfs)

    # melted_df = combined_df.melt(id_vars=['timestamp', 'name'], var_name='metric', value_name='value')
    # melted_df.to_html('melted.html')

    regions = combined_df["name"].unique().tolist()

    # for now use aggrnyl
    colorscale = "aggrnyl"

    region_to_colors = {}
    sampled_colors = list(sample_colorscale(colorscale, len(regions)))
    for i, region in enumerate(regions):
        region_to_colors[region] = sampled_colors[i]

    # construct list of metrics
    metrics = []
    for metric in combined_df.columns:
        if metric not in ["name", TALP_JSON_TIMESTAMP_KEY, TALP_JSON_METADATA_KEY]:
            metrics.append(metric)

    fig = make_subplots(
        rows=4,
        cols=6,
        specs=[
            [{"colspan": 6}, None, None, None, None, None],  # elapsed
            [
                {"colspan": 2, "rowspan": 2},
                None,
                {"colspan": 4},
                None,
                None,
                None,
            ],  # IPC pe
            [None, None, {"colspan": 2}, None, {"colspan": 2}, None],  # Comm LB
            [None, None, None, None, {}, {}],  # LB in / out
        ],
        horizontal_spacing=0.05,
        subplot_titles=[TALP_METRIC_TO_NAME_MAP[metric] for metric in metrics],
        print_grid=False,
    )

    # Elapsed time
    metric = "elapsedTime"
    for region in regions:
        fig.add_trace(
            _get_scatter(combined_df, region, metric, region_to_colors[region], True),
            col=1,
            row=1,
        )
    fig["layout"]["yaxis"]["title"] = "Time in [s]"

    # IPC
    metric = "averageIPC"
    for region in regions:
        fig.add_trace(
            _get_scatter(combined_df, region, metric, region_to_colors[region]),
            col=1,
            row=2,
        )
    fig["layout"]["yaxis2"]["title"] = "IPC"

    # Parallel Effiency
    metric = "parallelEfficiency"
    for region in regions:
        fig.add_trace(
            _get_scatter(combined_df, region, metric, region_to_colors[region]),
            col=3,
            row=2,
        )
    fig["layout"]["yaxis3"]["title"] = "Efficiency [0-1]"

    # communicationEfficiency
    metric = "communicationEfficiency"
    for region in regions:
        fig.add_trace(
            _get_scatter(combined_df, region, metric, region_to_colors[region]),
            col=3,
            row=3,
        )
    fig["layout"]["yaxis4"]["title"] = "Efficiency [0-1]"

    # LoadBalance
    metric = "loadBalance"
    for region in regions:
        fig.add_trace(
            _get_scatter(combined_df, region, metric, region_to_colors[region]),
            col=5,
            row=3,
        )
    fig["layout"]["yaxis5"]["title"] = "Efficiency [0-1]"

    # Lb in
    metric = "lbIn"
    for region in regions:
        fig.add_trace(
            _get_scatter(combined_df, region, metric, region_to_colors[region]),
            col=5,
            row=4,
        )
    fig["layout"]["yaxis6"]["title"] = "Efficiency [0-1]"

    # Lb out
    metric = "lbOut"
    for region in regions:
        fig.add_trace(
            _get_scatter(combined_df, region, metric, region_to_colors[region]),
            col=6,
            row=4,
        )
    fig["layout"]["yaxis7"]["title"] = "Efficiency [0-1]"

    fig.update_traces(mode="markers+lines")
    # Update layout
    fig.update_layout(
        title="Performance Metrics Evolution",
        legend_title="Regions",
        autosize=True,
        height=1200,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        font=dict(
            family="Roboto Condensed, monospace",
            # size=18,
        ),
    )
    return render_template(
        TALP_PAGES_TEMPLATE_PATH,
        "time_series.jinja",
        # fig_elapsed_time=fig.to_html(full_html=False),
        figure_ts=fig.to_html(full_html=False),
        metadata=json.dumps({"test": "test"}),
    )


def get_landing_page(pages):
    paths = []
    for page in pages:
        paths.append(page.output_path)
    return render_template(TALP_PAGES_TEMPLATE_PATH, "landing_page.jinja", paths=paths)


def main():
    # Creating the main argument parser
    parser = argparse.ArgumentParser(
        description="Render the complete html pages including a landing page"
    )
    # Adding argument for JSON file
    parser.add_argument(
        "-p", "--path", dest="path", help="Root path to search the *.json files in"
    )
    parser.add_argument(
        "-o",
        "--output-path",
        dest="output",
        help="relative path to create the folder structure of html stuff",
        required=True,
    )
    parser.add_argument(
        "--log-level",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
        default="INFO",
    )

    # Parsing arguments
    try:
        args = parser.parse_args()
        path, output = _verify_input(args)
    except Exception as e:
        logging.error(f"When parsing arguments ecountered the following error: {e}")
        # parser.print_help()
        exit(1)
    
    log_level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(log_level, int):
        raise ValueError("Invalid log level: %s" % args.log_level)

    logging.basicConfig(level=log_level)

    # First detect the folder structure and append to the runs
    run_folders = find_run_folders(path)

    pages = []

    for run_folder in run_folders:
        logging.info(f"Processing folder: {run_folder.relative_path}")
        html = get_time_series_html(run_folder)
        pages.append(
            TalpPage(
                run_folder=run_folder, output_path=run_folder.relative_path, html=html
            )
        )

    for page in pages:
        output_path = os.path.join(output, page.output_path)
        os.makedirs(output_path)
        logging.info(f"Writing output in {output_path}")
        with open(os.path.join(output_path, "index.html"), "w") as json_file:
            json_file.write(page.html)
    # at last write landing page

    landing_page = get_landing_page(pages)
    with open(os.path.join(output, "index.html"), "w") as json_file:
        json_file.write(landing_page)


if __name__ == "__main__":
    main()
