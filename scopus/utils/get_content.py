import os
import requests


def download(url, params=None, accept="xml"):
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

    Raises
    ------
    HTTPError
        If the status of the response is not ok.

    ValueError
        If the accept parameter is not one of the accepted values.

    Returns
    -------
    resp : byte-like object
        The content of the file, which needs to be serialized.
    """
    accepted = ("json", "xml", "atom+xml")
    if accept.lower() not in accepted:
        raise ValueError('accept parameter must be one of ' +
                         ', '.join(accepted))
    key = load_api_key()
    header = {'Accept': 'application/{}'.format(accept), 'X-ELS-APIKey': key}
    resp = requests.get(url, headers=header, params=params)
    resp.raise_for_status()  # Raise status code if necessary
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


def load_api_key():
    """Helper function to return MY_API_KEY if it is correctly specified.

    Returns
    -------
    MY_API_KEY : str
        The user's API key for interaction with Scopus database.
    """
    SCOPUS_API_FILE = os.path.expanduser("~/.scopus/my_scopus.py")
    try:
        with open(SCOPUS_API_FILE) as f:
            exec(f.read(), globals())
            return globals()["MY_API_KEY"]
    except:
        raise Exception('No API key found. Please create {} it and define '
                        'variable MY_API_KEY in it.'.format(SCOPUS_API_FILE))
