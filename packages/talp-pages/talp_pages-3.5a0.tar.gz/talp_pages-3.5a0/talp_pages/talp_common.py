"""
File declaring some global scoped variables and functions
"""

import pathlib
from jinja2 import Environment, FileSystemLoader

TALP_PAGES_DEFAULT_REGION_NAME = "MPI Execution"
TALP_JSON_POP_METRICS_KEY = "popMetrics"
TALP_JSON_TIMESTAMP_KEY = "timestamp"
TALP_JSON_METADATA_KEY = "metadata"

TALP_PAGES_TEMPLATE_PATH = pathlib.Path(__file__).parent.joinpath("templates").resolve()

TALP_METRIC_TO_NAME_MAP = {
    "elapsedTime": "Elapsed time",
    "averageIPC": "Average IPC",
    "parallelEfficiency": "Parallel efficiency",
    "communicationEfficiency": "Communication efficiency",
    "loadBalance": "Load balance",
    "lbIn": "In-node load balance",
    "lbOut": "Inter-node load balance",
}

TALP_PAGES_INDEX_PAGE = "index.html"
TALP_PAGES_REPORT_PAGE = "report.html"


def render_template(directory, template_name, **context):
    # Set up Jinja2 environment and load the template
    env = Environment(loader=FileSystemLoader(directory))
    template = env.get_template(template_name)

    # Render the template with the provided context
    return template.render(context)
