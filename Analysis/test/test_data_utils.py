"""Unit testing file for datautils.py.

This module provides units tests for the datautils.py module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
"""

import os
import pytest

from analyzer import data_utils


def test_compute_checksum_byte():
    """Test computing the checksum of a series of bytes."""
    assert data_utils.compute_checksum_bytes(b"\xA5") == 0x74BEB8EA


def test_compute_checksum_4_bytes_zero():
    """Test computing the checksum of a series of bytes."""
    assert data_utils.compute_checksum_bytes(b"\x00\x00\x00\x00") == 0x2144DF1C

def test_compute_checksum_bytes_large():
    """Test computing the checksum of a series of bytes."""
    assert data_utils.compute_checksum_bytes(b"\xFA\xFF\xFF\x12\x34\x5F\xFF\xFF") == 0xC1D4E671


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
    assert filename == data_utils.compute_checksum(file_object)

