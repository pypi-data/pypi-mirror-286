"""Tests for epyfun.web."""

import os
from typing import Union

import requests

import epyfun


def download_file(url: str, destination: Union[str, None] = None) -> str:
    """Download a file from the specified URL.

    Download a file from the specified URL and save it to the specified destination.

    this is quick and dirty. See other approaches in
    https://realpython.com/python-download-file-from-url/

    Args:
        url (str): The URL of the file to be downloaded.
        destination (str): The path to save the downloaded file. If not
            specified, the file will be saved in the current directory with
            the same name as the file at the URL.

    Raises:
        Exception: if it fails to download the file

    Returns:
        None
    """
    if not destination:
        destination = os.path.basename(url)

    # Send the GET request to the URL
    response = requests.get(url, timeout=70)

    # Check if the response was successful
    if response.status_code == 200:
        # Create the destination directory if it doesn't exist
        epyfun.fs.create_dir(destination)

        # Open the destination file for writing
        with open(destination, "wb") as f:
            # Write the content of the response to the file
            f.write(response.content)

        return destination
    else:
        raise Exception(f"Failed to download file: {response.status_code}")
