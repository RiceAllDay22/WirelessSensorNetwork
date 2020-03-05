"""
Contains tests to see if pytest is working properly.

This file is a part of Jake's C Compiler (JCC)
(c) Copyright 2019 Jacob Larkin
"""

import pytest


def test_func_fast():
    """Simple pass test."""


def test_addition():
    """Test basic addition."""
    if 1 + 1 != 2:
        pytest.fail()


def test_assert():
    """Test assert usage."""
    assert True
    assert 1 + 2 == 3


def test_exception():
    """Test exceptions."""
    with pytest.raises(SystemExit):
        raise SystemExit(1)
