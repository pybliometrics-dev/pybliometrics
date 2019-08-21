from warnings import warn


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


def check_integrity(tuples, fields, action):
    """Check integrity of specific fields in a list of tuples and perfom
    provided action.
    """
    for field in fields:
        elements = [getattr(e, field) for e in tuples]
        if None in elements:
            msg = "Parsed information doesn't pass integrity check "\
                  "because of incomplete field '{}'".format(field)
            if action == "raise":
                raise AttributeError(msg)
            elif action == "warn":
                warn(msg)


def check_field_consistency(needles, haystack):
    """Raise ValueError if elements of a list are not present in a string."""
    wrong = set(needles) - set(haystack.split())
    if wrong:
        msg = "Element(s) '{}' not allowed in parameter "\
              "integrity_fields".format("', '".join(sorted(wrong)))
        raise ValueError(msg)


def get_id(s):
    """Helper function to return the Scopus ID at a fixed position."""
    path = ['coredata', 'dc:identifier']
    return chained_get(s, path, "").split(':')[-1] or None


def get_link(dct, idx, path=['coredata', 'link']):
    """Helper function to return the link at position `idx` from coredata."""
    links = chained_get(dct, path, [{}])
    try:
        return links[idx].get('@href')
    except IndexError:
        return None


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
