from typing import Literal, Optional, Type
from random import shuffle
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import JSONDecodeError
from time import sleep, time
from urllib3.util import Retry

from pybliometrics import __version__
from pybliometrics import exception
from pybliometrics.utils.startup import get_config, get_insttokens, get_keys, _throttling_params

# Define user agent string for HTTP requests
user_agent = 'pybliometrics-v' + __version__

errors = {400: exception.Scopus400Error, 401: exception.Scopus401Error,
          403: exception.Scopus403Error, 404: exception.Scopus404Error,
          407: exception.Scopus407Error, 413: exception.Scopus413Error, 
          414: exception.Scopus414Error, 429: exception.Scopus429Error}


def get_session() -> Type[Session]:
    """Auxiliary function to create a session"""
    config = get_config()

    _retries = config.getint("Requests", "Retries", fallback=5)
    retry = Retry(total=_retries, backoff_factor=0.1,
                  status_forcelist=[500, 501, 502, 503, 504, 524])
    adapter = HTTPAdapter(max_retries=retry)
    session = Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def prepare_headers_and_tokens(params):
    """Prepare headers and tokens for the request."""
    keys = get_keys()
    insttokens = list(zip(keys, get_insttokens()))
    keys = keys[len(insttokens):]

    token_key, insttoken = None, None
    if "insttoken" in params:
        token_key = params.pop("apikey")
        insttoken = params.pop("insttoken")
    elif "apikey" in params:
        key = params.pop("apikey")
    elif insttokens:
        token_key, insttoken = insttokens.pop(0)
    else:
        key = keys.pop(0)

    header = {
        'Accept': 'application/json',
        'User-Agent': user_agent,
        'X-ELS-APIKey': token_key or key
    }

    if insttoken:
        header['X-ELS-Insttoken'] = insttoken

    return header, insttokens, keys


def handle_throttling(api):
    """Handle throttling based on API limits."""
    if len(_throttling_params[api]) == _throttling_params[api].maxlen:
        try:
            sleep(1 - (time() - _throttling_params[api][0]))
        except (IndexError, ValueError):
            pass


def handle_response(resp):
    """Handle the response and raise appropriate errors."""
    try:
        error_type = errors[resp.status_code]
        try:
            reason = resp.json()['service-error']['status']['statusText']
        except KeyError:
            try:
                reason = resp.json()['message']
            except KeyError:
                try:
                    reason = resp.json()['error-response']['error-message']
                except KeyError:
                    reason = ""
        raise error_type(reason)
    except (JSONDecodeError, KeyError):
        resp.raise_for_status()


def get_content(url: str,
                api: str,
                params: Optional[dict],
                method: Literal['GET', 'PUT'] = 'GET',
                **kwds):
    """Helper function to download a file and return its content."""
    config = get_config()

    session = get_session()

    params = params or {}
    params.update(**kwds)
    proxies = dict(config._sections.get("Proxy", {}))
    timeout = config.getint("Requests", "Timeout", fallback=20)

    header, insttokens, keys = prepare_headers_and_tokens(params)
    handle_throttling(api)

    # Use insttoken if available
    if 'X-ELS-Insttoken' in header:
        if method == 'GET':
            resp = session.get(url, headers=header, params=params, timeout=timeout)
        else:
            resp = session.put(url, headers=header, json=params, timeout=timeout)
    else:
        if method == 'GET':
            resp = session.get(url, headers=header, params=params, timeout=timeout, proxies=proxies)
        else:
            resp = session.put(url, headers=header, json=params, timeout=timeout, proxies=proxies)


    # Retry logic for 429 or 401
    while resp.status_code in (429, 401):
        try:
            token_key, token = insttokens.pop(0) # Get and remove current key
            header['X-ELS-APIKey'] = token_key
            header['X-ELS-Insttoken'] = token
            shuffle(insttokens)
            if method == 'GET':
                resp = session.get(url, headers=header, params=params, timeout=timeout)
            else:
                resp = session.put(url, headers=header, json=params, timeout=timeout)
        except IndexError:  # All tokens depleted
            break

    while resp.status_code in (429, 401):
        try:
            key = keys.pop(0)  # Remove current key
            header['X-ELS-APIKey'] = key
            shuffle(keys)
            if method == 'GET':
                resp = session.get(url, headers=header, proxies=proxies, params=params, timeout=timeout)
            else:
                resp = session.put(url, headers=header, json=params, timeout=timeout, proxies=proxies)
        except IndexError:  # All keys depleted
            break

    if 'X-ELS-Insttoken' in header:
        del header['X-ELS-Insttoken']

    _throttling_params[api].append(time())

    handle_response(resp)
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
