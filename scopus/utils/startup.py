import os
import warnings
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

# Configuration setup
config = configparser.ConfigParser()
config.optionxform = str
CONFIG_FILE = os.path.expanduser("~/.scopus/config.ini")
if not os.path.exists(CONFIG_FILE):
    text = "scopus did not find a configuration file.  Please issue "\
           "scopus.utils.create_config() to start the process which guides "\
           "you through the generation of the configuration file or read "\
           "https://scopus.readthedocs.io/en/stable/configuration.html."
    warnings.warn(text, UserWarning)
else:
    config.read(CONFIG_FILE)

# Temporary Deprecation Warnings flags
warnings.simplefilter('always', DeprecationWarning)
try:
    config.add_section('Warnings')
except configparser.DuplicateSectionError:
    pass
text = "This class is deprecated and its maintenance has been suspended.  "\
       "Please use {}() instead.  For details see https://scopus."\
       "readthedocs.io/en/where/tips.html#migration-guide-from-0-x-to-1-x."
config.set('Warnings', 'Text', text)
config.set('Warnings', 'Affiliation', '1')
config.set('Warnings', 'Author', '1')
config.set('Warnings', 'Abstract', '1')
