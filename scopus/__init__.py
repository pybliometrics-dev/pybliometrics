import os
import requests
import sys

SCOPUS_API_FILE = os.path.expanduser("~/.scopus/my_scopus.py")
if os.path.exists(SCOPUS_API_FILE):
    with open(SCOPUS_API_FILE) as f:
        exec(f.read())
else:
    raise Exception('{} not found. Please create it and put your API key in it.'.format(SCOPUS_API_FILE))


# Namespaces for Scopus XML
ns = {'dtd': 'http://www.elsevier.com/xml/svapi/abstract/dtd',
      'ait': "http://www.elsevier.com/xml/ani/ait",
      'cto': "http://www.elsevier.com/xml/cto/dtd",
      'xocs': "http://www.elsevier.com/xml/xocs/dtd",
      'ce': 'http://www.elsevier.com/xml/ani/common',
      'prism': 'http://prismstandard.org/namespaces/basic/2.0/',
      'xsi': "http://www.w3.org/2001/XMLSchema-instance",
      'dc': 'http://purl.org/dc/elements/1.1/',
      'atom': 'http://www.w3.org/2005/Atom',
      'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'}


def get_content(qfile, url, refresh, header, params=None, ):
    """Helper function to read file content, download and save if necessary.

    Parameters
    ----------
    qfile : string
        The name of the file to be created.

    url : string
        The URL to be parsed.

    refresh : bool
        Whether the file content should be refreshed if it exists.

    header : string
        Dictionary containing header parameters.  For required keys
        and accepted values see e.g.
        https://api.elsevier.com/documentation/AuthorRetrievalAPI.wadl

    params : dict (optional)
        Dictionary containing query parameters.  For required keys
        and accepted values see e.g.
        https://api.elsevier.com/documentation/AuthorRetrievalAPI.wadl

    Raises
    ------
    HTTPError
        If the status of the response is not ok.

    Returns
    -------
    content : str
        The content of the file.
    """
    if os.path.exists(qfile) and not refresh:
        with open(qfile, 'rb') as f:
            content = f.read()
    else:
        resp = requests.get(url, headers=header, params=params)
        resp.raise_for_status()  # Raise status code if necessary
        content = resp.text.encode('utf-8')
        with open(qfile, 'wb') as f:
            f.write(content)
    return content


def get_encoded_text(container, xpath):
    """Return text for element at xpath in the container xml if it is there.

    Note: in Python2, I had to encode this. In Python3, this seems to be
unnecessary.

    """
    if container is None:
        return None
    result = container.find(xpath, ns)
    if hasattr(result, 'text') and result.text:
        if sys.version_info[0] == 3:
            return result.text
        else:
            return result.text.encode('utf-8')
    else:
        return None
