import configparser
from typing import Optional, Union
from pathlib import Path
from pybliometrics.utils.constants import CONFIG_FILE


def create_config(config_dir: Optional[Union[str, Path]] = None,
                  custom_keys: Optional[list[str]] = None,
                  custom_tokens: Optional[list[tuple[str, str]]] = None
                  ):
    """Initiates process to generate configuration file.

    :param config_dir: The location of the configuration file.
    :param keys: If you provide a list of keys, pybliometrics will skip the
                 prompt.  It will also not ask for InstToken.  This is
                 intended for workflows using CI, not for general use.
    :param insttoken: An InstToken to be used alongside the key(s).  Will only
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
    new_keys, new_tokens = None, None
    if custom_keys:
        if not isinstance(custom_keys, list):
            raise ValueError("Parameter `keys` must be a list.")
        new_keys = ", ".join(custom_keys)
    if custom_tokens:
        if not isinstance(custom_tokens, list):
            raise ValueError("Parameter `inst_tokens` must be a list of tuples. "\
                             "E.g. [('key_1', 'token_1'), ('key_2', 'token_2')]")
        new_tokens = ", ".join([f"{key}:{value}" for key, value in custom_tokens])

    # If no keys or tokens are provided, ask for them
    if not (custom_keys or custom_tokens):
        prompt_key = "Please enter your API Key(s), obtained from "\
                     "http://dev.elsevier.com/myapikey.html.  Separate "\
                     "multiple keys by comma:\n"
        new_keys = input(prompt_key)
        prompt_token = "API Keys are sufficient for most users.  If you "\
                       "have an InstToken, please enter the token:key pair now. "\
                       "Separate multiple tokens by a comma, e.g. token1: key1, token2: key2"\
                       "otherwise just press Enter:\n"
        new_tokens = input(prompt_token)

    # Set keys and tokens in config
    if new_keys:
        config.set('Authentication', 'APIKey', new_keys)
    if new_tokens:
        config.set('Authentication', 'InstToken', new_tokens)

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
