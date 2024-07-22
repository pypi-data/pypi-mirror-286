"""epyfun."""

from . import fs
from . import pandas
from . import plotly
from . import web
from .fs import convert_to_utf8
from .fs import create_dir
from .fs import get_latest_file
from .web import download_file
from .plotly import splom
from .plotly import make_hover_template
from .pandas import sanitize_column_name
from .pandas import clean_names


__all__ = [
    "fs",  #
    "convert_to_utf8",
    "create_dir",
    "get_latest_file",
    "web",  #
    "download_file",
    "plotly",  #
    "splom",
    "make_hover_template",
    "pandas",  #
    "sanitize_column_name",
    "clean_names",
]
