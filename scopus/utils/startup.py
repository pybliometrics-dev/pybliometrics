import os
import warnings
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

# Temporary Deprecation Warnings flags
warnings.simplefilter('always', DeprecationWarning)
config.add_section('Warnings')
text = "This class is deprecated and its maintenance has been suspended.  "\
       "Please use {}() instead.  For details see https://scopus."\
       "readthedocs.io/en/latest/tips.html#migration-guide-from-0-x-to-1-x."
config.set('Warnings', 'Text', text)
config.set('Warnings', 'Affiliation', '1')
config.set('Warnings', 'Author', '1')
config.set('Warnings', 'Abstract', '1')
