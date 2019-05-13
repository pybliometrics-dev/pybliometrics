from sys import version_info
from os.path import exists

from scopus.utils.constants import DEFAULT_PATHS
from scopus.utils.startup import config, CONFIG_FILE

py3 = version_info >= (3, 0)


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
        prompt_key = "Please enter your API Key, obtained from "\
                     "http://dev.elsevier.com/myapikey.html: \n"
        if py3:
            key = input(prompt_key)
        else:
            key = raw_input(prompt_key)
        config.set('Authentication', 'APIKey', key)
        prompt_token = "API Keys are sufficient for most users.  If you "\
                       "have to use Authtoken authentication, please enter "\
                       "the token, otherwise press Enter: \n"
        if py3:
            token = input(prompt_token)
        else:
            token = raw_input(prompt_token)
        if len(token) > 0:
            config.set('Authentication', 'InstToken', token)
        # Write out
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
    else:
        text = "Configuration file already exists at {}; process to create "\
               "the file aborted.  Please open the file and edit the "\
               "entries manually.".format(CONFIG_FILE)
        raise FileExistsError(text)
