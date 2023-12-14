from configparser import ConfigParser
from collections import deque
from pathlib import Path
from typing import List, Dict, Optional, Type
from os import path
from warnings import warn

from pybliometrics.scopus.utils.constants import CONFIG_FILE, RATELIMITS
from pybliometrics.scopus.utils.create_config import create_config

_custom_config_dir = None
_custom_keys = None

def get_config() -> Type[ConfigParser]:
    """Auxiliary function to get the config parser"""
    # Read/create config file (with fixture for RTFD.io)
    config = ConfigParser()
    config.optionxform = str

    if not _custom_config_dir and not CONFIG_FILE.exists():
            warn('Please create a configuration file by initializing Scopus with init().\n'
                 'For more information visit: https://pybliometrics.readthedocs.io/en/stable/configuration.html')
    else:
        if _custom_config_dir:
            config.read(_custom_config_dir)
        else:
            warn('Please initialize Scopus with init()', FutureWarning)
            config.read(CONFIG_FILE)
    
    return config

def get_config_path() -> Type[Path]:
    """Auxiliary function to get the configuration file path"""
    return _custom_config_dir or CONFIG_FILE

def get_keys() -> List[str]:
    """Auxiliary function to get the API keys"""
    if _custom_keys:
        keys = _custom_keys
    else:
        config = get_config()
        keys = [k.strip() for k in config.get('Authentication', 'APIKey').split(",")]
    return keys

def get_throttling_params() -> Dict:
    """Auxiliary function to get the throttling params"""
    return {k: deque(maxlen=v) for k, v in RATELIMITS.items()}

def init(config_dir: Optional[str] = CONFIG_FILE, keys: Optional[List[str]] = None) -> None:
    """
    Function to initialize the Pybliometrics library. For more information go to the [documentation](https://pybliometrics.readthedocs.io/en/stable/configuration.html).
    
    Parameters
    ----------
    config_dir : str
        Path to the configuration file
    keys : lst
        List of API keys
    """
    global _custom_config_dir
    global _custom_keys

    config_dir = Path(config_dir)

    if not config_dir.exists():
        create_config(config_dir,
                      keys)
    
    _custom_config_dir = config_dir
    _custom_keys = keys

    return None