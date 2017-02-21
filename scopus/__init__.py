import os
import requests

SCOPUS_API_FILE = os.path.expanduser("~/.scopus/my_scopus.py")
if os.path.exists(SCOPUS_API_FILE):
    with open(SCOPUS_API_FILE) as f:
        exec(f.read())
else:
    raise Exception('{} not found. Please create it and create variable'
                    'MY_API_KEY in it.'.format(SCOPUS_API_FILE))


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

    Parameters
    ----------
    container : xml.etree.ElementTree.Element
        The element to be searched in.

    xpath : str
        The path to be looked for.

    Returns
    -------
    result : str

    """
    try:
        return container.find(xpath, ns).text
    except AttributeError:
        return None
