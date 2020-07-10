from os import makedirs
from os.path import exists, expanduser

from pybliometrics.scopus.utils.constants import DEFAULT_PATHS
from pybliometrics.scopus.utils.startup import config, CONFIG_FILE


def create_config():
    """Initiates process to generate configuration file."""
    file_exists = exists(CONFIG_FILE)
    if not file_exists:
        # Set directories
        config.add_section('Directories')
        for key, value in DEFAULT_PATHS.items():
            config.set('Directories', key, value)
        # Set authentication
        config.add_section('Authentication')
        prompt_key = "Please enter your API Key(s), obtained from "\
                     "http://dev.elsevier.com/myapikey.html.  Separate "\
                     "multple keys using a comma:\n"
        key = input(prompt_key)
        config.set('Authentication', 'APIKey', key)
        prompt_token = "API Keys are sufficient for most users.  If you "\
                       "have to use Authtoken authentication, please enter "\
                       "the token, otherwise press Enter: \n"
        token = input(prompt_token)
        if token:
            config.set('Authentication', 'InstToken', token)
        # Write out
        try:
            makedirs(expanduser('~/.scopus/'))
        except FileExistsError:
            pass
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
        print(f"Configuration file successfully created at {CONFIG_FILE}")
    else:
        text = f"Configuration file already exists at {CONFIG_FILE}; process "\
               "to create the file aborted.  Please open the file and edit "\
               "the entries manually."
        raise FileExistsError(text)
