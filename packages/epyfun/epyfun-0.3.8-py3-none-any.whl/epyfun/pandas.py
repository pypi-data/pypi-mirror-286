"""Pandas-related helpers."""

import re
from typing import Any
from typing import Union

import pandas as pd


def sanitize_column_name(col_name: Union[str, list[str], Any]) -> str:
    """Sanitize a column name.

    Sanitize a column name for compatibility with data analysis tools.

    This function takes a column name and ensures it meets certain criteria
    suitable for data analysis libraries and tools. The sanitization process
    involves:

    Converting non-strings to strings: If the input col_name is not a string, it
    is converted to a string using an underscore ("_") separator. Preserving
    letters, numbers, and underscores: The function keeps only alphanumeric
    characters (letters and numbers) along with underscores. Any other
    characters are replaced with underscores. Removing leading and trailing
    underscores: Leading and trailing underscores are removed from the sanitized
    column name. Converting to lowercase: The final sanitized column name is
    converted to lowercase for consistency.

    Args:
        col_name (str): The column name to be sanitized.

    Returns:
        str: The sanitized column name suitable for data analysis tools.
    """
    col_name = col_name if isinstance(col_name, str) else "_".join(col_name)
    # We want to keep only letters, numbers, or underscores
    col_name = re.sub(r"[^a-zA-Z0-9_]", "_", col_name)
    col_name = re.sub(r"_+", "_", col_name)  # but don't like repeated _
    col_name = col_name.strip("_")  # and don't like leading or trailing _
    col_name = col_name.lower()
    return col_name


def clean_names(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names in a pandas DataFrame.

    Clean column names in a pandas DataFrame.

    This function iterates through all column names in the provided pandas
    DataFrame (df) and applies the `sanitize_column_name()` function to each
    name. The sanitized names are then assigned back to the DataFrame's columns
    attribute.

    Args:
        df: the DataFrame whose column names need to be cleaned.

    Returns:
        pandas.DataFrame: The DataFrame with sanitized column names.
    """
    df.columns = pd.Index([sanitize_column_name(col) for col in df.columns])
    return df
