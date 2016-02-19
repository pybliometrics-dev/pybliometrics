import os

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


def get_encoded_text(container, xpath):
    '''Return text for element at xpath in the container xml if it is there. Note:
in Python2, I had to encode this. In Python3, this seems to be unnecessary.

    '''
    if container is None:
        return None
    result = container.find(xpath, ns)
    if hasattr(result, 'text') and result.text:
        return result.text
    else:
        return None
