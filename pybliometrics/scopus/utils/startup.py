import configparser
from collections import deque
from os import environ
from pathlib import Path

from pybliometrics.scopus.utils.constants import RATELIMITS

if 'PYB_CONFIG_FILE' in environ:
    CONFIG_FILE = environ['PYB_CONFIG_FILE']
else:
    if (Path.home()/".scopus").exists():
        CONFIG_FILE = Path.home()/".scopus"/"config.ini"
    else:
        CONFIG_FILE = Path.home()/".pybliometrics"/"config.ini"

# Read config file
try:
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(CONFIG_FILE)
    # Parse keys with fixture for RTFD.io
    try:
        KEYS = [k.strip() for k in config.get('Authentication', 'APIKey').split(",")]
    except configparser.NoSectionError:
        pass
except FileNotFoundError:
    import warnings
    text = "pybliometrics did not find a configuration file.  Please issue "\
          "pybliometrics.scopus.utils.create_config() to start the process "\
          "which guides you through the generation of the configuration "\
          "file or read https://pybliometrics.readthedocs.io/en/stable/configuration.html."
    warnings.warn(text, UserWarning)

# Throttling params
_throttling_params = {k: deque(maxlen=v) for k, v in RATELIMITS.items()}
