"""Unit tests for pytest.

Contains unit tests to assure pytest is working properly.

This file is a part of the Wireless Sensor Network project.
(c) Copyright 2020 Jacob Larkin and Adriann Liceralde
"""

import time
import logging
import pytest


LOGGER = logging.getLogger(__name__)


def test_func_pass():
    """Simple pass test."""


def test_func_pass_sleep():
    """Test pass with 1 second sleep."""
    time.sleep(1)


def test_addition():
    """Test basic addition."""
    if (1 + 1) != 2:
        pytest.fail()


def test_assert():
    """Test assert usage."""
    assert True
    assert 1 + 2 == 3


def test_exception():
    """Test expected exceptions."""
    with pytest.raises(SystemExit):
        raise SystemExit(1)


def test_logging():
    """Test basic logging functionality."""
    LOGGER.info('testing LOGGER info')
    LOGGER.warning('testing LOGGER warning')
    LOGGER.error('testing LOGGER error')
    LOGGER.critical('testing LOGGER crtical')
