import configparser
from typing import Optional, Union
from pathlib import Path
from pybliometrics.utils.constants import CONFIG_FILE


def create_config(config_dir: Optional[Union[str, Path]] = None,
                  keys: Optional[list[str]] = None,
                  insttoken: Optional[list[str]] = None
                  ):
    """Initiates process to generate configuration file.

    :param config_dir: The location of the configuration file.
    :param keys: If you provide a list of keys, pybliometrics will skip the
                 prompt.  It will also not ask for InstToken.  This is
                 intended for workflows using CI, not for general use.
    :param insttoken: An InstToken to be used alongside the key(s). Will only
                      be used if `keys` is not empty.
    """
    from pybliometrics.utils.constants import DEFAULT_PATHS

    if not config_dir:
        config_dir = CONFIG_FILE

    config = configparser.ConfigParser()
    config.optionxform = str
    print(f"Creating config file at {config_dir} with default paths...")

    # Set directories
    config.add_section('Directories')
    for api, path in DEFAULT_PATHS.items():
        config.set('Directories', api, str(path))

    # Set authentication
    config.add_section('Authentication')

    # Get keys and tokens
    if keys:
        if not isinstance(keys, list):
            raise ValueError("Parameter `keys` must be a list.")
        keys = ", ".join(keys)
    if insttoken:
        if not isinstance(insttoken, list):
            raise ValueError("Parameter `inst_tokens` must be a list. ")
        insttoken = ", ".join(insttoken)

    # If no keys or tokens are provided, ask for them
    if not (keys or insttoken):
        prompt_key = "Please enter your API Key(s), obtained from "\
                     "http://dev.elsevier.com/myapikey.html.  Separate "\
                     "multiple keys by comma:\n"
        keys = input(prompt_key)
        prompt_token = "API Keys are sufficient for most users.  If you "\
                       "have an InstToken, please enter the tokens pair now. "\
                       "Separate multiple tokens by a comma. The correspondig "\
                       "key's position should match the position of the token."\
                       "If you don't have tokens, just press Enter:\n"
        insttoken = input(prompt_token)

    # Set keys and tokens in config
    config.set('Authentication', 'APIKey', keys)
    if insttoken:
        config.set('Authentication', 'InstToken', insttoken)

    # Set default values
    config.add_section('Requests')
    config.set('Requests', 'Timeout', '20')
    config.set('Requests', 'Retries', '5')

    # Write out
    config_dir.parent.mkdir(parents=True, exist_ok=True)
    with open(config_dir, "w") as ouf:
        config.write(ouf)
    print(f"Configuration file successfully created at {config_dir}\n"
          "For details see https://pybliometrics.rtfd.io/en/stable/configuration.html.")
    return config
