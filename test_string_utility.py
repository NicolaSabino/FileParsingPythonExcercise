"""String utility module unit tests"""

from collections import namedtuple
import pytest
from string_utility import is_string_valid, compute_checksum, is_checksum_valid

UsecaseString = namedtuple("usecase_acc_string", "input_str expected_value notes")

string_validation_testdata = [
    UsecaseString(notes="Empty", input_str="", expected_value=False),
    UsecaseString(notes="None", input_str=None, expected_value=False),
    UsecaseString(
        notes="Invalid lenght", input_str="#G400FFF03DA8\r\n", expected_value=False
    ),
    UsecaseString(
        notes="Invalid string beginning", input_str="?G4001FFF03DA8\r\n", expected_value=False
    ),
    UsecaseString(
        notes="Invalid string end", input_str="#G4001FFF03DA8\n", expected_value=False
    ),
    UsecaseString(notes="Valid string", input_str="#G4001FFF03DA8\r\n", expected_value=True)
]

string_checksum_testdata = [
    UsecaseString(notes="Example", input_str="#G4001FFF03DA8\r\n", expected_value=168)
]

string_checksum_validity_testdata = [
    UsecaseString(notes="Invalid CHecksum", input_str="#G4001AFF03DA8\r\n", expected_value=False),
    UsecaseString(notes="Example", input_str="#G4001FFF03DA8\r\n", expected_value=True)
]


@pytest.mark.parametrize(
    "input_str, expected_value, notes", string_validation_testdata
)
def test_acc_string_validation(input_str, expected_value, notes):
    """Test acceleration string validation"""
    assert (
        is_string_valid(input_str) == expected_value
    ), f"{input_str}: {notes}"


@pytest.mark.parametrize(
        "input_str, expected_value, notes", string_checksum_testdata
)
def test_acc_string_checksum(input_str, expected_value, notes):
    """Test acceleration string checksum calculation"""
    assert(
        compute_checksum(input_str) == expected_value
    ), f"{input_str}: {notes}"

@pytest.mark.parametrize(
        "input_str, expected_value, notes", string_checksum_validity_testdata
)
def test_acc_string_checksum_validity(input_str, expected_value, notes):
    """Test acceleration string checksum calculation"""
    assert(
        is_checksum_valid(input_str) == expected_value
    ), f"{input_str}: {notes}"
