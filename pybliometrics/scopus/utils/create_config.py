from pybliometrics.scopus.utils.constants import DEFAULT_PATHS
from pybliometrics.scopus.utils.startup import config, CONFIG_FILE


def create_config():
    """Initiates process to generate configuration file."""
    if not CONFIG_FILE.exists():
        # Set directories
        config.add_section('Directories')
        for api, path in DEFAULT_PATHS.items():
            config.set('Directories', api, str(path))
        # Set authentication
        config.add_section('Authentication')
        prompt_key = "Please enter your API Key(s), obtained from "\
                     "http://dev.elsevier.com/myapikey.html.  Separate "\
                     "multiple keys by comma:\n"
        key = input(prompt_key)
        config.set('Authentication', 'APIKey', key)
        prompt_token = "API Keys are sufficient for most users.  If you "\
                       "have an InstToken, please enter the token now;"\
                       "otherwise just press Enter:\n"
        token = input(prompt_token)
        if token:
            config.set('Authentication', 'InstToken', token)
        # Write out
        with open(CONFIG_FILE, "w") as ouf:
            config.write(ouf)
        print(f"Configuration file successfully created at {CONFIG_FILE}\n"
              "For details see https://pybliometrics.rtfd.io/en/stable/configuration.html.")
    else:
        text = f"Configuration file already exists at {CONFIG_FILE}; process "\
               "to create the file aborted.  Please open the file and edit "\
               "the entries manually."
        raise FileExistsError(text)
