import os
import requests
from configparser import NoOptionError

from pybliometrics.scopus import exception
from pybliometrics.scopus.utils import DEFAULT_PATHS, config
from pybliometrics.scopus.utils.create_config import create_config

errors = {400: exception.Scopus400Error, 401: exception.Scopus401Error,
          404: exception.Scopus404Error, 429: exception.Scopus429Error,
          500: exception.Scopus500Error}


def cache_file(url, params={}, **kwds):
    """Helper function to download a file and return its content.

    Parameters
    ----------
    url : string
        The URL to be parsed.

    params : dict (optional)
        Dictionary containing query parameters.  For required keys
        and accepted values see e.g.
        https://api.elsevier.com/documentation/AuthorRetrievalAPI.wadl

    kwds : key-value parings, optional
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
    # Get credentials
    key = config.get('Authentication', 'APIKey')
    header = {'X-ELS-APIKey': key, 'Accept': 'application/json'}
    if config.has_option('Authentication', 'InstToken'):
        token = config.get('Authentication', 'InstToken')
        header.update({'X-ELS-APIKey': key, 'X-ELS-Insttoken': token})
    # Perform request
    params.update(**kwds)
    # If config.ini has a section as follows:
    #
    # [Proxy]
    # https = protocol://server:port
    #
    # it uses a proxy as defined
    # see requests documentation for details
    if config.has_section("Proxy"):
        proxyDict = dict(config.items("Proxy"))
        resp = requests.get(url, headers=header, proxies=proxyDict, params=params)
    else:
        resp = requests.get(url, headers=header, params=params)
    # Handle error messages
    if resp.ok:
        return resp
    else:
        # Try raising ScopusError with supplied error message
        # if no message given, do without supplied error message
        # at least raise requests error
        if resp.status_code in errors:
            try:
                reason = resp.json()['service-error']['status']['statusText']
            except:
                reason = ""
            raise errors[resp.status_code](reason)
        else:
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
    PII usually has 17 chars, but in Scopus there are valid cases with only
    16 for old converted articles.

    Scopus ID contains only digits, but it can have leading zeros.  If ID
    with leading zeros is treated as a number, SyntaxError can occur, or the
    ID will be rendered invalid and the type will be misinterpreted.
    """
    sid = str(sid)
    try:
        isnumeric = sid.isnumeric()
    except AttributeError:  # Python2
        isnumeric = unicode(sid, 'utf-8').isnumeric()
    if not isnumeric:
        if sid.startswith('2-s2.0-'):
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
        raise ValueError('ID type detection failed for \'{}\'.'.format(sid))


def get_content(qfile, refresh, *args, **kwds):
    """Helper function to read file content as xml.  The file is cached
    in a subfolder of ~/.scopus/.

    Parameters
    ----------
    qfile : string
        The name of the file to be created.

    refresh : bool
        Whether the file content should be refreshed if it exists.

    *args, **kwds :
        Arguments and keywords to be passed on to download().

    Returns
    -------
    content : str
        The content of the file.
    """
    if not refresh and os.path.exists(qfile):
        with open(qfile, 'rb') as f:
            content = f.read()
    else:
        content = cache_file(*args, **kwds).text.encode('utf-8')
        with open(qfile, 'wb') as f:
            f.write(content)
    return content


def get_folder(api, view):
    """Auxiliary function to get the cache folder belonging to a an API
    and eventually create the folder.
    """
    if not config.has_section('Directories'):
        create_config()
    try:
        folder = config.get('Directories', api)
    except NoOptionError:
        folder = DEFAULT_PATHS[api]
    folder = os.path.join(folder, view or '')
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder
