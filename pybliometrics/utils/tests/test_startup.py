"""Tests for the startup and configuraition module."""
import os

import pytest

from pybliometrics.scopus import init
from pybliometrics.utils import get_insttokens, get_keys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def test_custom_insttokens():
    """Test whether custom insttokens are correctly set."""
    init(keys=['1', '2', '3'], inst_tokens=['a', 'b'])
    assert get_insttokens() == ['a', 'b']


def test_custom_keys():
    """Test whether custom keys are correctly set."""
    init(keys=['1', '2', '3'])
    assert get_keys() == ['1', '2', '3']


def test_new_config():
    """Test whether a new config file is created."""
    # Remove test config file if it exists
    config_path = f'{CURRENT_DIR}/test_config.cfg'
    if os.path.exists(config_path):
        os.remove(config_path)

    # Create new config
    init(config_dir=f'{CURRENT_DIR}/test_config.cfg',
         keys=['3', '4', '5'],
         inst_tokens=['c', 'd'])

    # Use custom keys and tokens
    assert get_keys() == ['3', '4', '5']
    assert get_insttokens() == ['c', 'd']


def test_new_test_config():
    """Test whether the new test config file is correctly read."""
    init(config_dir=f'{CURRENT_DIR}/test_config.cfg',
         keys=['3', '4', '5'])

    # Use keys and tokens from test config
    assert get_keys() == ['3', '4', '5'] # from previous test
    assert get_insttokens() == [] # no insttokens since only keys are provided

    init(config_dir=f'{CURRENT_DIR}/test_config.cfg',
         keys=['5', '6', '7'],
         inst_tokens=['e', 'f'])

    # Use custom keys and tokens
    assert get_keys() == ['5', '6', '7']
    assert get_insttokens() == ['e', 'f']

def test_error_more_tokens_than_keys():
    """Test whether an error is raised if more tokens than keys are provided."""
    with pytest.raises(ValueError):
        init(keys=['1'], inst_tokens=['a', 'b'])
