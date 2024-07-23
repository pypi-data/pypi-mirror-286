#!/usr/bin/env python

import argparse
import json
import os
from urllib.request import urlopen, Request
import logging
from .talp_common import TALP_POP_METRICS_KEY, TALP_DEFAULT_REGION_NAME


class TalpBadge:
    def __init__(self, talp_file):
        # Now directly try to create a connection
        with open(talp_file, "r") as json_file:
            # dont catch exception, but fail
            self.raw_data = json.load(json_file)

        logging.debug(f"Created TalpReport and read the json: {self.raw_data}")
        # do some sanity checks
        if not self.raw_data[TALP_POP_METRICS_KEY]:
            logging.error(
                f"No {TALP_POP_METRICS_KEY} found in {talp_file}. Try re-running DLB with arguments --talp --talp-summary=pop-metrics --talp-file={talp_file}"
            )
            raise Exception(f"No {TALP_POP_METRICS_KEY} found")

    def get_badge_svg(self):

        parallel_efficiency = None
        pop_metric_regions = self.raw_data[TALP_POP_METRICS_KEY]
        for region in pop_metric_regions:
            if region["name"] == TALP_DEFAULT_REGION_NAME:
                parallel_efficiency = region["parallelEfficiency"]

        if not parallel_efficiency:
            raise Exception(
                f"Could not find {TALP_DEFAULT_REGION_NAME} in provided json"
            )

        parallel_efficiency = round(parallel_efficiency, 2)

        if parallel_efficiency < 0.6:
            bagde_url = f"https://img.shields.io/badge/Parallel_efficiency-{parallel_efficiency}-red"
        elif parallel_efficiency < 0.8:
            bagde_url = f"https://img.shields.io/badge/Parallel_efficiency-{parallel_efficiency}-orange"
        else:
            bagde_url = f"https://img.shields.io/badge/Parallel_efficiency-{parallel_efficiency}-green"

        return urlopen(Request(url=bagde_url, headers={"User-Agent": "Mozilla"})).read()


def _validate_inputs(args):
    output_file = None
    input_file = None
    # Check if the JSON file exists
    if not os.path.exists(args.input):
        raise Exception(
            f"Error: The specified JSON file '{args.json_file}' does not exist."
        )
    else:
        input_file = args.input
    # Set output
    if args.output:
        output_file = args.output
        if not args.output.endswith(".svg"):
            output_file += ".svg"
            logging.info(f"Appending .svg to '{args.output}'")
        # Check if the HTML file exists
        if os.path.exists(args.output):
            logging.info(f"Overwriting '{args.output}'")
    else:
        output_file = args.input.replace(".json", "")
        output_file += ".svg"

    return output_file, input_file


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Render a SVG badge that can be used in pipelines using shields.io. Therefore internet access is required"
    )
    parser.add_argument(
        "-i", "--input", dest="input", help="Path to the TALP JSON file"
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output",
        help="Name of the svg file beeing generated. If not specified [input].svg will be chosen",
        required=False,
    )

    # Parsing arguments
    try:
        args = parser.parse_args()
        output_file, input_file = _validate_inputs(args)
    except Exception as e:
        logging.error(f"When parsing arguments ecountered the following error: {e}")
        parser.print_help()
        exit(1)

    badge = TalpBadge(input_file)
    rendered_svg = badge.get_badge_svg()
    with open(output_file, "wb") as f:
        f.write(rendered_svg)


if __name__ == "__main__":
    main()
