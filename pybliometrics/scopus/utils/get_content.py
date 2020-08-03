import os

import requests

from pybliometrics.scopus import exception
from pybliometrics.scopus.utils import CONFIG_FILE, DEFAULT_PATHS, config
from pybliometrics.scopus.utils.create_config import create_config
from pybliometrics import version_info

# Define user agent string for HTTP requests
user_agent = 'pybliometrics-v' + '.'.join([str(e) for e in version_info[:3]])

errors = {400: exception.Scopus400Error, 401: exception.Scopus401Error,
          403: exception.Scopus403Error, 404: exception.Scopus404Error,
          429: exception.Scopus429Error, 500: exception.Scopus500Error}


def get_content(url, params={}, *args, **kwds):
    """Helper function to download a file and return its content.

    Parameters
    ----------
    url : string
        The URL to be parsed.

    params : dict (optional)
        Dictionary containing query parameters.  For required keys
        and accepted values see e.g.
        https://api.elsevier.com/documentation/AuthorRetrievalAPI.wadl

    *args, **kwds : key-value parings, optional
        Keywords passed on to as query parameters.  Must contain fields
        and values specified in the respective API specification.

    Raises
    ------
    ScopusHtmlError or HTTPError
        If the status of the response is not ok.

    ValueError
        If the accept parameter is not one of the accepted values.

    Returns
    -------
    resp : byte-like object
        The content of the file, which needs to be serialized.
    """
    from random import shuffle

    from simplejson import JSONDecodeError

    # Set header, params and proxy
    keys = config.get('Authentication', 'APIKey').split(",")
    header = {'X-ELS-APIKey': keys[0].strip(),
              'Accept': 'application/json',
              'User-Agent': user_agent}
    if config.has_option('Authentication', 'InstToken'):
        token = config.get('Authentication', 'InstToken')
        header['X-ELS-Insttoken'] = token
    params.update(**kwds)
    proxies = dict(config._sections.get("Proxy", {}))

    # Perform request, eventually replacing the current key
    resp = requests.get(url, headers=header, proxies=proxies, params=params)
    while resp.status_code == 429:
        try:
            keys.pop(0)  # Remove current key
            shuffle(keys)
            header['X-ELS-APIKey'] = keys[0].strip()
            resp = requests.get(url, headers=header, proxies=proxies,
                                params=params)
            config['Authentication']['APIKey'] = ",".join(list(keys))
        except IndexError:  # All keys depleted
            break

    # Eventually raise error, if possible with supplied error message
    try:
        error_type = errors[resp.status_code]
        try:
            reason = resp.json()['service-error']['status']['statusText']
        except (JSONDecodeError, KeyError):
            try:
                reason = resp.json()['message']
            except:
                reason = ""
        raise errors[resp.status_code](reason)
    except KeyError:
        resp.raise_for_status()
    return resp


def detect_id_type(sid):
    """Method that tries to infer the type of abstract ID.

    Parameters
    ----------
    sid : str
        The ID of an abstract on Scopus.

    Raises
    ------
    ValueError
        If the ID type cannot be inferred.

    Notes
    -----
    Scopus IDs and Pubmed IDs are sometimes hard to distinguish.  If you
    work with both types, consider specifying the ID type manually.
    """
    sid = str(sid)
    try:
        isnumeric = sid.isnumeric()
    except AttributeError:  # Python2
        isnumeric = unicode(sid, 'utf-8').isnumeric()
    if not isnumeric:
        if sid.startswith('1-s2.0-') or sid.startswith('2-s2.0-'):
            id_type = 'eid'
        elif '/' in sid or "." in sid:
            id_type = 'doi'
        elif 16 <= len(sid) <= 17:
            id_type = 'pii'
    elif isnumeric:
        if len(sid) < 10:
            id_type = 'pubmed_id'
        else:
            id_type = 'scopus_id'
    try:
        return id_type
    except UnboundLocalError:
        raise ValueError(f'ID type detection failed for "{sid}".')


def get_folder(api, view):
    """Auxiliary function to get the cache folder belonging to an API,
    eventually create the folder.
    """
    from configparser import NoOptionError
    if not config.has_section('Directories'):
        create_config()
    try:
        folder = config.get('Directories', api)
    except NoOptionError:
        folder = DEFAULT_PATHS[api]
        config.set('Directories', api, folder)
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
    folder = os.path.join(folder, view or '')
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder


def print_progress(iteration, total, length=50):
    """Print terminal progress bar."""
    share = iteration / float(total)
    filled_len = int(length * iteration // total)
    bar = '█' * filled_len + '-' * (length - filled_len)
    print(f'\rProgress: |{bar}| {share:.2%} Complete', end='\r')
    if iteration == total:
        print()
