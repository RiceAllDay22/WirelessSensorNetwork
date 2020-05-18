"""Unit testing file for datautils.py.

This module provides units tests for the datautils.py module.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
"""

import os
import pytest

from analyzer import data_utils

import numpy as np
import pandas as pd


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

checksum_file_tuples = []
checksum_filenames = []
for name in os.listdir(CHECKSUM_PATH):
    path = os.path.join(CHECKSUM_PATH, name)
    if os.path.isfile(path):
        clean_filename = name.split(".")[0]
        checksum_file_tuples.append((clean_filename, open(path, "rb")))
        checksum_filenames.append(name)

@pytest.mark.parametrize("filename, file_object", checksum_file_tuples, ids=checksum_filenames)
def test_checksum_files(filename, file_object):
    """Test checksums for all files in CHECKSUM_PATH."""
    assert filename.upper() == data_utils.compute_checksum(file_object).upper()



CSV_VALID_PATH = "./test/assets/csv_files/valid"

csv_valid_file_paths = []
csv_valid_filenames = []
for name in os.listdir(CSV_VALID_PATH):
    path = os.path.join(CSV_VALID_PATH, name)
    if os.path.isfile(path):
        csv_valid_file_paths.append(path)
        csv_valid_filenames.append(name)

@pytest.mark.parametrize("file_path", csv_valid_file_paths, ids=csv_valid_filenames)
def test_load_csv_valid(file_path):
    """Assure all csv files in CSV_VALID_PATH are valid."""
    data_utils.load_file(file_path, data_utils.FileType.CSV)


def test_load_csv_1_entry():
    """Assure 1_entry.csv is loaded correctly."""
    correct_array = np.array([[123, 52234]], dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(CSV_VALID_PATH, "1_entry.csv")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.CSV)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)

def test_load_csv_2_entries():
    """Assure 2_entries.csv is loaded correctly."""
    correct_array = np.array([[123, 52234], [124, 49]], dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(CSV_VALID_PATH, "2_entries.csv")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.CSV)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)

def test_load_csv_5_entries():
    """Assure 5_entries.csv is loaded correctly."""
    correct_array = np.array([[20000, 52234], [20001, 49], [20002, 41], [20003, 42], [20004, 42]],
                             dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(CSV_VALID_PATH, "5_entries.csv")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.CSV)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)

def test_load_csv_50_entries():
    """Assure 50_entries.csv is loaded correctly."""
    correct_array = np.array([[1, 3456], [2, 326], [3, 1646], [4, 2562],
                              [5, 8745], [6, 353], [7, 453], [8, 2],
                              [9, 36456], [10, 5674], [11, 45], [12, 64],
                              [13, 1], [14, 6678], [15, 362], [16, 5345677],
                              [17, 345567], [18, 56], [19, 26245], [20, 646787],
                              [21, 8245], [22, 2645], [23, 6546], [24, 3676],
                              [25, 78256], [26, 3678], [27, 1626], [28, 457984],
                              [29, 62], [30, 52], [31, 63657], [32, 678],
                              [33, 256], [34, 1], [35, 647], [36, 876],
                              [37, 8957], [38, 82], [39, 56], [40, 2436],
                              [41, 4768], [42, 678], [43, 9], [44, 457],
                              [45, 2], [46, 45], [47, 6], [48, 23457],
                              [49, 567897], [50, 8095]], dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(CSV_VALID_PATH, "50_entries.csv")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.CSV)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)



CSV_INVALID_PATH = "./test/assets/csv_files/invalid"

csv_invalid_file_paths = []
csv_invalid_filenames = []
for name in os.listdir(CSV_INVALID_PATH):
    path = os.path.join(CSV_INVALID_PATH, name)
    if os.path.isfile(path):
        csv_invalid_file_paths.append(path)
        csv_invalid_filenames.append(name)

@pytest.mark.parametrize("file_path", csv_invalid_file_paths, ids=csv_invalid_filenames)
def test_load_csv_invalid(file_path):
    """Assure all csv files in CSV_INVALID_PATH are invalid."""
    with pytest.raises(data_utils.InvalidFileError) as pytest_wrapped_e:
        data_utils.load_file(file_path, data_utils.FileType.CSV)



DAT_VALID_PATH = "./test/assets/dat_files/valid"

dat_valid_file_paths = []
dat_valid_filenames = []
for dat_valid_name in os.listdir(DAT_VALID_PATH):
    path = os.path.join(DAT_VALID_PATH, dat_valid_name)
    if os.path.isfile(path):
        dat_valid_file_paths.append(path)
        dat_valid_filenames.append(dat_valid_name)

@pytest.mark.parametrize("file_path", dat_valid_file_paths, ids=dat_valid_filenames)
def test_load_dat_valid(file_path):
    """Assure all dat files in DAT_VALID_PATH are valid."""
    data_utils.load_file(file_path, data_utils.FileType.BINARY)


def test_load_dat_1_entry():
    """Assure 1_entry.dat is loaded correctly."""
    correct_array = np.array([[1, 286331153]], dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(DAT_VALID_PATH, "1_entry.dat")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.BINARY)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)

def test_load_dat_2_entries():
    """Assure 2_entries.dat is loaded correctly."""
    correct_array = np.array([[1, 286331153], [2, 572662306]], dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(DAT_VALID_PATH, "2_entries.dat")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.BINARY)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)

def test_load_dat_5_entries():
    """Assure 5_entries.dat is loaded correctly."""
    correct_array = np.array([[1, 286331153], [2, 572662306], [3, 858993459], [4, 1145324612],
                              [5, 1431655765]], dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(DAT_VALID_PATH, "5_entries.dat")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.BINARY)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)

def test_load_dat_5_entries_higher():
    """Assure 5_entries.dat is loaded correctly."""
    correct_array = np.array([[12626695, 286331153], [12626696, 572662306], [12626697, 858993459],
                             [12626698, 1145324612], [12626699, 1431655765]], dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(DAT_VALID_PATH, "5_entries_higher.dat")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.BINARY)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)

def test_load_dat_50_entries():
    """Assure 50_entries.dat is loaded correctly."""
    correct_array = np.array([[1, 16843009], [2, 33686018], [3, 50529027], [4, 67372036],
                              [5, 84215045], [6, 101058054], [7, 117901063], [8, 134744072],
                              [9, 151587081], [10, 269488144], [11, 286331153], [12, 303174162],
                              [13, 320017171], [14, 336860180], [15, 353703189], [16, 370546198],
                              [17, 387389207], [18, 404232216], [19, 421075225], [20, 538976288],
                              [21, 555819297], [22, 572662306], [23, 589505315], [24, 606348324],
                              [25, 623191333], [26, 640034342], [27, 656877351], [28, 673720360],
                              [29, 690563369], [30, 808464432], [31, 825307441], [32, 842150450],
                              [33, 858993459], [34, 875836468], [35, 892679477], [36, 909522486],
                              [37, 926365495], [38, 943208504], [39, 960051513], [40, 1077952576],
                              [41, 1094795585], [42, 1111638594], [43, 1128481603], [44, 1145324612],
                              [45, 1162167621], [46, 1179010630], [47, 1195853639], [48, 1212696648],
                              [49, 1229539657], [50, 1347440720]], dtype="<u4")
    correct_frame = pd.DataFrame(correct_array, columns=["UNIXTIME", "CO2"])
    filepath = os.path.join(DAT_VALID_PATH, "50_entries.dat")
    loaded_frame = data_utils.load_file(filepath, data_utils.FileType.BINARY)
    pd.testing.assert_frame_equal(correct_frame, loaded_frame)



DAT_INVALID_PATH = "./test/assets/dat_files/invalid"

dat_invalid_file_paths = []
dat_invalid_filenames = []
for name in os.listdir(DAT_INVALID_PATH):
    path = os.path.join(DAT_INVALID_PATH, name)
    if os.path.isfile(path):
        dat_invalid_file_paths.append(path)
        dat_invalid_filenames.append(name)

@pytest.mark.parametrize("file_path", dat_invalid_file_paths, ids=dat_invalid_filenames)
def test_load_dat_invalid(file_path):
    """Assure all dat files in DAT_INVALID_PATH are invalid."""
    with pytest.raises(data_utils.InvalidFileError) as pytest_wrapped_e:
        data_utils.load_file(file_path, data_utils.FileType.BINARY)
