from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from pybliometrics import __version__
from pybliometrics.scopus import exception
from pybliometrics.scopus.utils.startup import config

# Define user agent string for HTTP requests
user_agent = 'pybliometrics-v' + __version__

errors = {400: exception.Scopus400Error, 401: exception.Scopus401Error,
          403: exception.Scopus403Error, 404: exception.Scopus404Error,
          407: exception.Scopus407Error, 413: exception.Scopus413Error, 
          414: exception.Scopus414Error, 429: exception.Scopus429Error}

_retries = config.getint("Requests", "Retries", fallback=5)
retry = Retry(total=_retries, status_forcelist=[500, 501, 502, 503, 504, 524],
              backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retry)
session = Session()
session.mount('http://', adapter)
session.mount('https://', adapter)

def get_content(url, api, params=None, **kwds):
    """Helper function to download a file and return its content.

    Parameters
    ----------
    url : str
        The URL to be parsed.

    api : str
        The Scopus API to be accessed.

    params : dict (optional)
        Dictionary containing query parameters.  For required keys
        and accepted values see e.g.
        https://api.elsevier.com/documentation/AuthorRetrievalAPI.wadl

    **kwds : key-value parings, optional
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
    from time import sleep, time

    from pybliometrics.scopus.utils.startup import _throttling_params, KEYS

    # Set header, params and proxy
    try:
        header = {'X-ELS-APIKey': KEYS[0],
                  'Accept': 'application/json',
                  'User-Agent': user_agent}
    except IndexError:
        raise errors[429]

    if config.has_option('Authentication', 'InstToken'):
        token = config.get('Authentication', 'InstToken')
        header['X-ELS-Insttoken'] = token
    params = params or {}
    params.update(**kwds)
    proxies = dict(config._sections.get("Proxy", {}))

    # Replace credentials if provided
    if "apikey" in params:
        header['X-ELS-APIKey'] = params.pop("apikey")
    if "insttoken" in params:
        header['X-ELS-Insttoken'] = params.pop("insttoken")

    # Eventually wait bc of throttling
    if len(_throttling_params[api]) == _throttling_params[api].maxlen:
        try:
            sleep(1 - (time() - _throttling_params[api][0]))
        except (IndexError, ValueError):
            pass
    
    # Perform request, eventually replacing the current key
    timeout = config.getint("Requests", "Timeout", fallback=20)
    resp = session.get(url, headers=header, proxies=proxies, params=params,
                      timeout=timeout)
    while resp.status_code == 429:
        try:
            KEYS.pop(0)  # Remove current key
            shuffle(KEYS)
            header['X-ELS-APIKey'] = KEYS[0].strip()
            resp = session.get(url, headers=header, proxies=proxies,
                               params=params, timeout=timeout)
        except IndexError:  # All keys depleted
            break
    _throttling_params[api].append(time())

    # Eventually raise error, if possible with supplied error message
    try:
        error_type = errors[resp.status_code]
        try:
            reason = resp.json()['service-error']['status']['statusText']
        except KeyError:
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
    if not sid.isnumeric():
        if sid.startswith('1-s2.0-') or sid.startswith('2-s2.0-'):
            id_type = 'eid'
        elif '/' in sid or "." in sid:
            id_type = 'doi'
        elif 16 <= len(sid) <= 17:
            id_type = 'pii'
    else:
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
    from pathlib import Path

    from pybliometrics.scopus.utils import CONFIG_FILE, DEFAULT_PATHS
    from pybliometrics.scopus.utils.create_config import create_config

    if not config.has_section('Directories'):
        create_config()
    try:
        parent = Path(config.get('Directories', api))
    except NoOptionError:
        parent = DEFAULT_PATHS[api]
        config.set('Directories', api, str(parent))
        with open(CONFIG_FILE, 'w') as ouf:
            config.write(ouf)
    try:
        folder = parent/view
    except TypeError:
        folder = parent
    folder.mkdir(parents=True, exist_ok=True)
    return folder
