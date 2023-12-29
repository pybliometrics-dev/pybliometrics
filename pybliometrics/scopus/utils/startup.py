import os
from configparser import ConfigParser
from collections import deque
from pathlib import Path
from typing import List, Dict, Optional, Type
from warnings import warn

from pybliometrics.scopus.utils.constants import CONFIG_FILE, RATELIMITS
from pybliometrics.scopus.utils.create_config import create_config

CUSTOM_DIR = None
CUSTOM_KEYS = None

_throttling_params = {k: deque(maxlen=v) for k, v in RATELIMITS.items()}

def get_config() -> Type[ConfigParser]:
    """Auxiliary function to get the config parser"""
    # Read/create config file (with fixture for RTFD.io)
    config = ConfigParser()
    config.optionxform = str

    if not CUSTOM_DIR and not CONFIG_FILE.exists():
        warn('Please create a configuration file by initializing Pybliometrics with init().\n'
             'For more information visit: '
             'https://pybliometrics.readthedocs.io/en/stable/configuration.html')
    else:
        if CUSTOM_DIR:
            config.read(CUSTOM_DIR)
        else:
            warn('Please initialize Pybliometrics with init().\n'
                 'For more information visit: '
                 'https://pybliometrics.readthedocs.io/en/stable/configuration.html', FutureWarning)
            config.read(CONFIG_FILE)

    return config

def get_config_path() -> Type[Path]:
    """Auxiliary function to get the configuration file path"""
    return CUSTOM_DIR or CONFIG_FILE

def get_keys() -> List[str]:
    """Auxiliary function to get the API keys"""
    if CUSTOM_KEYS:
        keys = CUSTOM_KEYS
    else:
        config = get_config()
        keys = [k.strip() for k in config.get('Authentication', 'APIKey').split(",")]
    return keys

def init(config_dir: Optional[str] = CONFIG_FILE, keys: Optional[List[str]] = None) -> None:
    """
    Function to initialize the Pybliometrics library. For more information go to the
    [documentation](https://pybliometrics.readthedocs.io/en/stable/configuration.html).
    
    Parameters
    ----------
    config_dir : str
        Path to the configuration file
    keys : lst
        List of API keys
    """
    global CUSTOM_DIR
    global CUSTOM_KEYS

    config_dir = Path(config_dir)
    config_dir = _change_folder_path(config_dir)

    if not config_dir.exists():
        create_config(config_dir,
                      keys)

    CUSTOM_DIR = config_dir
    CUSTOM_KEYS = keys

def _change_folder_path(path: Type[Path], default_filename: str='pybliometrics.cfg') -> Type[Path]:
    """Auxiliary function to correct the path for a folder"""
    if os.path.isdir(path):
        return path/default_filename
    return path
