from collections import namedtuple
from typing import List, NamedTuple, Optional, Tuple, Union

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import check_integrity, check_parameter_value,\
    check_field_consistency, make_int_if_possible, make_search_summary


class AffiliationSearch(Search):
    @property
    def affiliations(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples storing affiliation information,
        where each namedtuple corresponds to one affiliation.
        The information in each namedtuple is `(eid name variant documents city
        country parent)`.

        All entries are `strings`, `int` or `None`.  Field `variant` combines variants
        of names with a `";"`.

        Raises
        ------
        `ValueError`
            If the elements provided in `integrity_fields` do not match the
            actual field names (listed above).
        """
        # Initiate namedtuple with ordered list of fields
        fields = 'eid name variant documents city country parent'
        aff = namedtuple('Affiliation', fields)
        check_field_consistency(self._integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            name = item.get('affiliation-name')
            variants = [d.get('$', "") for d in item.get('name-variant', [])
                        if d.get('$', "") != name]
            parent = make_int_if_possible(item.get('parent-affiliation-id')) or None
            new = aff(eid=item.get('eid'), variant=";".join(variants),
                      documents=int(item['document-count']), name=name,
                      city=item.get('city'), country=item.get('country'),
                      parent=parent)
            out.append(new)
        # Finalize
        check_integrity(out, self._integrity, self._action)
        return out or None

    def __init__(self,
                 query: str,
                 refresh: Union[bool, int] = False,
                 verbose: bool = False,
                 download: bool = True,
                 integrity_fields: Union[List[str], Tuple[str, ...]] = None,
                 integrity_action: str = "raise",
                 **kwds: str
                 ) -> None:
        """Interaction with the Affiliation Search API.

        :param query: A string of the query.  For allowed fields and values see
                      https://dev.elsevier.com/sc_affil_search_tips.html.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param verbose: Whether to print a download progress bar.
        :param download: Whether to download results (if they have not been
                         cached).
        :param integrity_fields: Names of fields whose completeness should
                                 be checked.  `AffiliationSearch` will perform
                                 the action specified in `integrity_action`
                                 if elements in these fields are missing.
                                 This helps avoiding idiosynchratically missing
                                 elements that should always be present
                                 (e.g. EID or name).
        :param integrity_action: What to do in case integrity of provided fields
                                 cannot be verified.  Possible actions:
                                 - `"raise"`: Raise an AttributeError
                                 - `"warn"`: Raise a UserWarning
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/AffiliationSearchAPI.wadl.

        Raises
        ------
        `ScopusQueryError`
            If the number of search results exceeds 5000, which is the API's
            maximum number of results returned.  The error prevents the
            download attempt and avoids making use of your API key.

        `ValueError`
            If any of the parameters `integrity_action` or `refresh` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/STANDARD/{fname}`,
        where  `path` is specified in your configuration file and `fname` is
        the md5-hashed version of `query`.
        """
        # Check
        allowed = ("warn", "raise")
        check_parameter_value(integrity_action, allowed, "integrity_action")

        # Query
        self._action = integrity_action
        self._integrity = integrity_fields or []
        self._query = query
        self._refresh = refresh
        self._view = "STANDARD"
        Search.__init__(self, query=query, api="AffiliationSearch",
                        download=download, verbose=verbose, **kwds)

    def __str__(self):
        """Return a summary string."""
        res = [a['affiliation-name'] for a in self._json]
        return make_search_summary(self, "affiliation", res)
