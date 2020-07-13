from collections import namedtuple
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
        if None not in elements:
            continue
        msg = "Parsed information doesn't pass integrity check because of "\
              f"incomplete information in field '{field}'"
        if action == "raise":
            raise AttributeError(msg)
        elif action == "warn":
            warn(msg)


def check_integrity_params(action, allowed=("warn", "raise")):
    """Verify that the passed integrity action parameters valid ones."""
    if action not in allowed:
        msg = 'integrity_action parameter must be one of ' + ', '.join(allowed)
        raise ValueError(msg)


def check_field_consistency(needles, haystack):
    """Raise ValueError if elements of a list are not present in a string."""
    wrong = set(needles) - set(haystack.split())
    if wrong:
        msg = f"Element(s) '{', '.join(sorted(wrong))}' not allowed in "\
              "parameter integrity_fields"
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


def make_search_summary(self, keyword, results, joiner="\n    "):
    """Create string for str dunder of search classes."""
    date = self.get_cache_file_mdate().split()[0]
    if self._n != 1:
        appendix = "s"
        verb = "have"
    else:
        appendix = ""
        verb = "has"
    s = f"Search '{self.query}' yielded {self._n:,} "\
        f"{keyword}{appendix} as of {date}"
    if results:
        s += ":" + joiner + joiner.join(results)
    elif self._n:
        s += f", which {verb} not been downloaded"
    return s


def parse_affiliation(affs):
    """Helper function to parse list of affiliation-related information."""
    order = 'id parent type relationship afdispname preferred_name '\
            'parent_preferred_name country_code country address_part city '\
            'state postal_code org_domain org_URL'
    aff = namedtuple('Affiliation', order)
    out = []
    for item in listify(affs):
        if not item:
            continue
        doc = item.get('ip-doc', {}) or {}
        address = doc.get('address', {}) or {}
        new = aff(id=item.get('@affiliation-id'), parent=item.get('@parent'),
            type=doc.get('@type'), relationship=doc.get('@relationship'),
            afdispname=doc.get('@afdispname'),
            preferred_name=doc.get('preferred-name', {}).get('$'),
            parent_preferred_name=doc.get('parent-preferred-name', {}).get('$'),
            country_code=address.get('@country'), country=address.get('country'),
            address_part=address.get("address-part"), city=address.get('city'),
            postal_code=address.get('postal-code'), state=address.get('state'),
            org_domain=doc.get('org-domain'), org_URL=doc.get('org-URL'))
        out.append(new)
    return out or None


def parse_date_created(dct):
    """Helper function to parse date-created from profile."""
    date = dct['date-created']
    if date:
        return (int(date['@year']), int(date['@month']), int(date['@day']))
    else:
        return (None, None, None)
