import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

from scopus.utils import set_authentication, set_directories

# Configuration setup
CONFIG_FILE = os.path.expanduser("~/.scopus/config.ini")
config = configparser.ConfigParser()
config.optionxform = str
config.read(CONFIG_FILE)
if 'Authentication' not in config.sections():
    set_authentication(config, CONFIG_FILE)
if 'Directories' not in config.sections():
    set_directories(config, CONFIG_FILE)

# Create folders if necessary
for _, directory in config.items('Directories'):
    path = os.path.expanduser(directory)
    if not os.path.exists(path):
        os.makedirs(path)
