from configparser import ConfigParser, NoSectionError
from collections import deque
from pathlib import Path
from typing import List, Optional, Type

from pybliometrics.scopus.utils.constants import CONFIG_FILE, RATELIMITS, DEFAULT_PATHS, VIEWS
from pybliometrics.scopus.utils.create_config import create_config

CONFIG = None
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

    config_dir = Path(config_dir)

    if not config_dir.exists():
        CONFIG = create_config(config_dir,
                               keys)
    else:
        CONFIG = ConfigParser()
        CONFIG.optionxform = str
        CONFIG.read(config_dir)

    check_sections(CONFIG)
    check_default_paths(CONFIG, config_dir)
    create_cache_folders(CONFIG)

    CUSTOM_KEYS = keys


def check_sections(config: Type[ConfigParser]) -> None:
    """Auxiliary function to check if all sections exist."""
    for section in ['Directories', 'Authentication', 'Requests']:
        if not config.has_section(section):
            raise NoSectionError(section)


def check_default_paths(config: Type[ConfigParser], config_path: Type[Path]) -> None:
    """Auxiliary function to check if default cache paths exist.
    If not, the paths are writen in the config.
    """
    for api, path in DEFAULT_PATHS.items():
        if not config.has_option('Directories', api):
            config.set('Directories', api, str(path))
            with open(config_path, 'w', encoding='utf-8') as ouf:
                config.write(ouf)


def create_cache_folders(config: Type[ConfigParser]) -> None:
    """Auxiliary function to create cache folders."""
    for api, path in config.items('Directories'):
        for view in VIEWS[api]:
            view_path = Path(path, view)
            view_path.mkdir(parents=True, exist_ok=True)


def get_config() -> Type[ConfigParser]:
    """Function to get the config parser."""
    if not CONFIG:
        raise FileNotFoundError('No configuration file found.'
                                'Please initialize Pybliometrics with init().\n'
                                'For more information visit: '
                                'https://pybliometrics.readthedocs.io/en/stable/configuration.html')
    return CONFIG


def get_keys() -> List[str]:
    """Function to get the API keys and overwrite keys in config if needed."""
    if CUSTOM_KEYS:
        keys = CUSTOM_KEYS
    else:
        keys = [k.strip() for k in CONFIG.get('Authentication', 'APIKey').split(",")]
    return keys

