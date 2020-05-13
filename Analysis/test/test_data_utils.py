"""Unit testing file for datautils.py.

This module provides units tests for the datautils.py module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
"""

import os
import pytest

from analyzer import data_utils

CHECKSUM_PATH = "./test/assets/checksum_files"


file_tuples = []
filenames = []
dir_contents = os.listdir(CHECKSUM_PATH)
for name in dir_contents:
    path = os.path.join(CHECKSUM_PATH, name)
    if os.path.isfile(path):
        clean_filename = name.split(".")[0]
        file_tuples.append((clean_filename, open(path, "rb")))
        filenames.append(name)


@pytest.mark.parametrize("filename, file_object", file_tuples, ids=filenames)
def test_checksum_files(filename, file_object):
    """Test checksums for all files in assets/checksum_files."""
    assert filename == data_utils.compute_checksum(file_object).lower()
