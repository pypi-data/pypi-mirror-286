"""Some file-system related functions."""

import os
from typing import Union

import chardet

import epyfun


def get_latest_file(folder_path: str) -> str:
    """Retrieve the path of the latest file in a specified folder.

    Args:
        folder_path (str): The path to the folder containing the files.

    Returns:
        str: The full path of the latest file in the specified folder.
    """
    # Get a list of all files in the folder
    files = [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]

    # Sort the list of files in lexicographical order, using the key parameter
    # of the sorted function along with a lambda function that converts each
    # file name to lowercase, otherwise, sort will put first uppercase, hence,
    # README.md will go before all.md
    sorted_files = sorted(files, key=lambda x: x.lower())

    # Get the path of the latest file (the last one in the sorted list)
    latest_file = sorted_files[-1]

    # Return the full path of the latest file
    return os.path.join(folder_path, latest_file)


def create_dir(path: str) -> None:
    """Create a directory at the specified path if it does not already exist.

    This function checks if the directory already exists; if it does, it takes
    no action. If the directory does not exist, it creates the directory along
    with any necessary parent directories. If the path has an extension, it is
    assumed to be a file, and the directory is created based on the path's
    directory component.

    Args:
        path (str): The path to the directory to be created.
    """
    # this function just wants to make sure the directory exists, so if the path
    # already exists, either as a file or a directory, do nothing at all
    if not os.path.exists(path):
        # work with absolute path to prevent dirname() to be empty string
        abs_path = os.path.abspath(path)

        # we will assume that if path does not have extension, will be considered
        # a directory and will be created as is
        directory_path, ext = os.path.splitext(abs_path)
        if ext != "":
            directory_path = os.path.dirname(abs_path)

        if not os.path.exists(directory_path):
            os.makedirs(directory_path)


def convert_to_utf8(file_path: str, outputfile_path: Union[str, None] = None) -> str:
    """Convert the content of a text file to UTF-8 encoding.

    - file_path (str): The path to the input file.
    - outputfile_path (str, optional): The path to the output file. If not provided,
      the input file will be overwritten with its content converted to UTF-8.

    Returns:
    - str: The detected encoding of the input file.

    Note:
    - The function uses the `chardet` library to automatically detect the encoding
      of the input file.
    - If the detected encoding is not UTF-8, the file's content is decoded and then
      re-encoded in UTF-8 before writing to the output file or overwriting the input
      file.
    - If no output file path is provided, the input file will be overwritten.
    """
    with open(file_path, "rb") as file:
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)["encoding"]
        assert detected_encoding is not None

        if outputfile_path is None:
            outputfile_path = file_path

        # if detected_encoding != "utf-8":
        decoded_data = raw_data.decode(detected_encoding)
        epyfun.fs.create_dir(outputfile_path)
        with open(outputfile_path, "w", encoding="utf-8") as utf8_file:
            utf8_file.write(decoded_data)

        return detected_encoding
