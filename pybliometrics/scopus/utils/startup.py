import configparser
from collections import deque
from pathlib import Path

from pybliometrics.scopus.utils.constants import CONFIG_FILE, RATELIMITS
from pybliometrics.scopus.utils.create_config import create_config

# Read/create config file
if not CONFIG_FILE.exists():
    config = create_config()
else:
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(CONFIG_FILE)

# Parse keys with fixture for RTFD.io
try:
    KEYS = [k.strip() for k in config.get('Authentication', 'APIKey').split(",")]
except configparser.NoSectionError:
    pass

# Throttling params
_throttling_params = {k: deque(maxlen=v) for k, v in RATELIMITS.items()}
