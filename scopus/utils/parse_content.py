def chained_get(container, path, default=None):
    """Helper function to perform a series of .get() methods on a dictionary
    and return a default object type in the end.

    Parameters
    ----------
    container : dict
        The dictionary on which the .get() methods should be performed.

    path : list or tuple
        The list of keys that should be searched for.

    default : any (optional, default=None)
        The object type that should be returned if the search yields
        no result.
    """
    for key in path:
        try:
            container = container[key]
        except (AttributeError, KeyError, TypeError):
            return default
    return container


def get_id(s):
    """Helper function to return the Scopus ID at a fixed position."""
    return s['coredata']['dc:identifier'].split(':')[-1]


def get_link(dct, idx):
    """Helper function to return the link at position `idx` from coredata."""
    return dct['coredata'].get('link', [])[idx].get('@href')


def listify(element):
    """Helper function to turn an element into a list if it isn't a list yet.
    """
    if isinstance(element, list):
        return element
    else:
        return [element]

def parse_date_created(dct):
    """Helper function to parse date-created from profile."""
    date = dct['date-created']
    if date:
        return (int(date['@year']), int(date['@month']), int(date['@day']))
    else:
        return (None, None, None)
