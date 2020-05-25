import configparser
import os

if 'PYB_CONFIG_FILE' in os.environ:
    CONFIG_FILE = os.environ['PYB_CONFIG_FILE']
else:
    CONFIG_FILE = os.path.expanduser("~/.scopus/config.ini")
try:
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(CONFIG_FILE)
except FileNotFoundError:
    import warnings
    text = "pybliometrics did not find a configuration file.  Please issue "\
           "pybliometrics.scopus.utils.create_config() to start the process "\
           "which guides you through the generation of the configuration "\
           "file or read https://pybliometrics.readthedocs.io/en/stable/configuration.html."
    warnings.warn(text, UserWarning)
