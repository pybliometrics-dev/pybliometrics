from configparser import ConfigParser, NoSectionError
from collections import deque
from pathlib import Path
from typing import List, Optional, Type

from pybliometrics.scopus.utils.constants import CONFIG_FILE, RATELIMITS
from pybliometrics.scopus.utils.create_config import create_config

CONFIG = None
CONFIG_DIR = None
CUSTOM_KEYS = None

_throttling_params = {k: deque(maxlen=v) for k, v in RATELIMITS.items()}

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
    global CONFIG
    global CUSTOM_KEYS
    global CONFIG_DIR

    config_dir = Path(config_dir)

    if not config_dir.exists():
        CONFIG = create_config(config_dir,
                               keys)
    else:
        CONFIG = ConfigParser()
        CONFIG.optionxform = str
        CONFIG.read(config_dir)

    check_sections(CONFIG)

    CUSTOM_KEYS = keys
    CONFIG_DIR = config_dir


def check_sections(config: Type[ConfigParser]) -> None:
    """Auxiliary function to check if all sections exist."""
    for section in ['Directories', 'Authentication', 'Requests']:
        if not config.has_section(section):
            raise NoSectionError(section)


def get_config() -> Type[ConfigParser]:
    """Function to get the config parser."""
    if not CONFIG:
        raise FileNotFoundError('No configuration file found.'
                                'Please initialize Pybliometrics with init().\n'
                                'For more information visit: '
                                'https://pybliometrics.readthedocs.io/en/stable/configuration.html')
    return CONFIG


def get_config_path() -> Type[Path]:
    """Function to get the configuration file path."""
    return CONFIG_DIR or CONFIG_FILE


def get_keys() -> List[str]:
    """Function to get the API keys and overwrite keys in config if needed."""
    if CUSTOM_KEYS:
        keys = CUSTOM_KEYS
    else:
        keys = [k.strip() for k in CONFIG.get('Authentication', 'APIKey').split(",")]
    return keys
