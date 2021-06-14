import configparser
from os import environ
from pathlib import Path

if 'PYB_CONFIG_FILE' in environ:
    CONFIG_FILE = environ['PYB_CONFIG_FILE']
else:
    if (Path.home()/".scopus").exists():
        CONFIG_FILE = Path.home()/".scopus"/"config.ini"
    else:
        CONFIG_FILE = Path.home()/".pybliometrics"/"config.ini"

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
