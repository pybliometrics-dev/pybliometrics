from collections import namedtuple
from functools import reduce
from html import unescape
from typing import Any, Dict, Optional
from warnings import warn


def filter_digits(s):
    """Helper function to remove non-digits characters from a string."""
    return "".join(filter(str.isdigit, s))


def chained_get(container, path, default=None):
    """Helper function to perform a series of .get() methods on a dictionary
    or return the `default`.

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
    # Obtain value via reduce
    try:
        return reduce(lambda c, k: c.get(k, default), path, container)
    except (AttributeError, TypeError):
        return default


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


def check_field_consistency(needles, haystack):
    """Raise ValueError if elements of a list are not present in a string."""
    wrong = set(needles) - set(haystack.split())
    if wrong:
        msg = f"Element(s) '{', '.join(sorted(wrong))}' not allowed in "\
              "parameter integrity_fields"
        raise ValueError(msg)


def deduplicate(lst):
    """Auxiliary function to deduplicate a list while preserving its order."""
    new = reduce(lambda x, y: x + y if y[0] not in x else x,
                 map(lambda x: [x], lst),
                 [])
    return new


def get_id(s, integer=True):
    """Helper function to return the Scopus ID at a fixed position."""
    path = ['coredata', 'dc:identifier']
    try:
        return int(chained_get(s, path, "").split(':')[-1])
    except ValueError:
        return None


def get_freetoread(item, path, default):
    """Helper function to return freetoread information from search results."""
    text = chained_get(item, path, default)
    try:
        text = text[-1]["$"]
    except TypeError:
        pass
    return text


def get_link(dct, idx, path=['coredata', 'link']):
    """Helper function to return the link at position `idx` from coredata."""
    links = chained_get(dct, path, [{}])
    try:
        return links[idx].get('@href')
    except IndexError:
        return None


def html_unescape(s: str):
    """Convert s to Unicode characters if possible."""
    return unescape(s) if s else None


def listify(element):
    """Helper function to turn an element into a list if it isn't a list yet.
    """
    if isinstance(element, list):
        return element
    else:
        return [element]


def make_float_if_possible(val):
    """Attempt a conversion to float type."""
    try:
        return float(val)
    except TypeError:
        return val


def make_int_if_possible(val):
    """Attempt a conversion to int type."""
    try:
        return int(val)
    except TypeError:
        return val


def make_search_summary(self, keyword, results, joiner="\n    "):
    """Create string for str dunder of search classes."""
    date = self.get_cache_file_mdate().split()[0]
    if self._n != 1:
        appendix = "s"
        verb = "have"
    else:
        appendix = ""
        verb = "has"
    s = f"Search '{self._query}' yielded {self._n:,} "\
        f"{keyword}{appendix} as of {date}"
    if results:
        s += ":" + joiner + joiner.join(results)
    elif self._n:
        s += f", which {verb} not been downloaded"
    return s


def parse_affiliation(affs, view):
    """Helper function to parse list of affiliation-related information."""
    order = 'id parent type relationship afdispname preferred_name '\
            'parent_preferred_name country_code country address_part city '\
            'state postal_code org_domain org_URL'
    aff = namedtuple('Affiliation', order, defaults=(None,) * len(order.split()))
    out = []

    if view in ('STANDARD', 'ENHANCED'):
        for item in listify(affs):
            if not item:
                continue
            doc = item.get('ip-doc', {}) or {}
            address = doc.get('address', {}) or {}
            try:
                parent = int(item['@parent'])
            except KeyError:
                parent = None
            new = aff(id=int(item['@affiliation-id']), parent=parent,
                type=doc.get('@type'), relationship=doc.get('@relationship'),
                afdispname=doc.get('@afdispname'),
                preferred_name=doc.get('preferred-name', {}).get('$'),
                parent_preferred_name=doc.get('parent-preferred-name', {}).get('$'),
                country_code=address.get('@country'), country=address.get('country'),
                address_part=address.get("address-part"), city=address.get('city'),
                postal_code=address.get('postal-code'), state=address.get('state'),
                org_domain=doc.get('org-domain'), org_URL=doc.get('org-URL'))
            if any(val for val in new):
                out.append(new)
    elif view == 'LIGHT':
        new = aff(preferred_name=affs.get('affiliation-name'),
                  city=affs.get('affiliation-city'),
                  country=affs.get('affiliation-country'))
        if any(val for val in new):
            out.append(new)

    return out or None


def parse_date_created(dct):
    """Helper function to parse date-created from profile."""
    date = dct['date-created']
    if date:
        return int(date['@year']), int(date['@month']), int(date['@day'])
    else:
        return None, None, None
