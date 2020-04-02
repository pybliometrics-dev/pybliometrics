import configparser
from os.path import expanduser

CONFIG_FILE = expanduser("~/.scopus/config.ini")
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
