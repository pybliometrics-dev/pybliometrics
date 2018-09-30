# Namespaces for Scopus XML
ns = {'dtd': 'http://www.elsevier.com/xml/svapi/abstract/dtd',
      'dn': 'http://www.elsevier.com/xml/svapi/abstract/dtd',
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
        return "".join(container.find(xpath, ns).itertext())
    except AttributeError:
        return None
