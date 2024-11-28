"""Tests for the startup and configuraition module."""
import os

from pybliometrics.scopus import init
from pybliometrics.utils import get_insttokens, get_keys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

def test_custom_keys():
    """Test whether custom keys are correctly set."""
    init(inst_tokens=[('a', 'b')])
    assert get_insttokens() == [('a', 'b')]


def test_custom_insttokens():
    """Test whether custom insttokens are correctly set."""
    init(keys=['a', 'b'])
    assert get_keys() == ['a', 'b']


def test_new_config():
    """Test whether a new config file is created."""
    # Remove test config file if it exists
    config_path = f'{CURRENT_DIR}/test_config.cfg'
    if os.path.exists(config_path):
        os.remove(config_path)

    # Create new config
    init(config_dir=f'{CURRENT_DIR}/test_config.cfg',
         keys=['e', 'f'],
         inst_tokens=[('g', 'h')])

    # Use custom keys and tokens
    assert get_keys() == ['e', 'f']
    assert get_insttokens() == [('g', 'h')]


def test_new_test_config():
    """Test whether the new test config file is correctly read."""
    init(config_dir=f'{CURRENT_DIR}/test_config.cfg')

    # Use keys and tokens from test config
    assert get_keys() == ['e', 'f']
    assert get_insttokens() == [('g', 'h')]

    init(config_dir=f'{CURRENT_DIR}/test_config.cfg',
         keys=['i', 'j'],
         inst_tokens=[('k', 'l')])

    # Use custom keys and tokens
    assert get_keys() == ['i', 'j']
    assert get_insttokens() == [('k', 'l')]
