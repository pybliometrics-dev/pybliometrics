import os
import requests
from configparser import NoOptionError

from scopus import exception
from scopus.utils import DEFAULT_PATHS, config

errors = {400: exception.Scopus400Error, 401: exception.Scopus401Error,
          404: exception.Scopus404Error, 429: exception.Scopus429Error,
          500: exception.Scopus500Error}


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
    if not sid.isnumeric():
        if sid.startswith('2-s2.0-'):
            id_type = 'eid'
        elif '/' in sid:
            id_type = 'doi'
        elif 16 <= len(sid) <= 17:
            id_type = 'pii'
    elif sid.isnumeric():
        if len(sid) < 10:
            id_type = 'pubmed_id'
        else:
            id_type = 'scopus_id'
    else:
        raise ValueError('ID type detection failed for \'{}\'.'.format(sid))
    return id_type


def download(url, params=None, accept="xml", **kwds):
    """Helper function to download a file and return its content.

    Parameters
    ----------
    url : string
        The URL to be parsed.

    params : dict (optional)
        Dictionary containing query parameters.  For required keys
        and accepted values see e.g.
        https://api.elsevier.com/documentation/AuthorRetrievalAPI.wadl

    accept : str (optional, default=xml)
        mime type of the file to be downloaded.  Accepted values are json,
        atom+xml, xml.

    kwds : key-value parings, optional
        Keywords passed on to as query parameters.  Must contain fields
        and values specified in the respective API specification.

    Raises
    ------
    ScopusHtmlError
        If the status of the response is not ok.

    ValueError
        If the accept parameter is not one of the accepted values.

    Returns
    -------
    resp : byte-like object
        The content of the file, which needs to be serialized.
    """
    # Value check
    accepted = ("json", "xml", "atom+xml")
    if accept.lower() not in accepted:
        raise ValueError('accept parameter must be one of ' +
                         ', '.join(accepted))
    # Get credentials
    key = config.get('Authentication', 'APIKey')
    header = {'X-ELS-APIKey': key}
    if config.has_option('Authentication', 'InstToken'):
        token = config.get('Authentication', 'InstToken')
        header.update({'X-ELS-APIKey': key, 'X-ELS-Insttoken': token})
    header.update({'Accept': 'application/{}'.format(accept)})
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
    # Raise error if necessary
    try:
        reason = resp.reason.upper() + " for url: " + url
        raise errors[resp.status_code](reason)
    except KeyError:  # Exception not specified in scopus
        resp.raise_for_status()  # Will pass when everything is ok
    return resp


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
        content = download(*args, **kwds).text.encode('utf-8')
        with open(qfile, 'wb') as f:
            f.write(content)
    return content


def get_folder(api):
    """Auxiliary function to get the cache folder belonging to a an API
    and eventually create the folder.
    """
    if not config.has_section('Directories'):
        create_config()
    try:
        folder = config.get('Directories', api)
    except NoOptionError:
        folder = DEFAULT_PATHS[api]
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder
