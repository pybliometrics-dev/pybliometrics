from collections import namedtuple

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import check_integrity,\
    check_integrity_params, check_field_consistency, make_search_summary


class AffiliationSearch(Search):
    @property
    def affiliations(self):
        """A list of namedtuples storing affiliation information,
        where each namedtuple corresponds to one affiliation.
        The information in each namedtuple is (eid name variant documents city
        country parent).

        All entries are strings or None.  variant combines variants of names
        with a semicolon.

        Raises
        ------
        ValueError
            If the elements provided in integrity_fields do not match the
            actual field names (listed above).
        """
        # Initiate namedtuple with ordered list of fields
        fields = 'eid name variant documents city country parent'
        aff = namedtuple('Affiliation', fields)
        check_field_consistency(self.integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            name = item.get('affiliation-name')
            variants = [d.get('$', "") for d in item.get('name-variant', [])
                        if d.get('$', "") != name]
            new = aff(eid=item.get('eid'), variant=";".join(variants),
                      documents=item.get('document-count', '0'), name=name,
                      city=item.get('city'), country=item.get('country'),
                      parent=item.get('parent-affiliation-id'))
            out.append(new)
        # Finalize
        check_integrity(out, self.integrity, self.action)
        return out or None

    def __init__(self, query, refresh=False, download=True, count=200,
                 integrity_fields=None, integrity_action="raise",
                 verbose=False):
        """Interaction with the Affiliation Search API.

        Parameters
        ----------
        query : str
            A string of the query, e.g. "af-id(60021784)".

        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        download : bool (optional, default=True)
            Whether to download results (if they have not been cached).

        integrity_fields : None or iterable (default=None)
            Iterable of field names whose completeness should be checked.
            ScopusSearch will perform the action specified in
            `integrity_action` if elements in these fields are missing.  This
            helps avoiding idiosynchratically missing elements that should
            always be present, such as the EID or the name.

        integrity_action : str (optional, default="raise")
            What to do in case integrity of provided fields cannot be
            verified.  Possible actions:
            - "raise": Raise an AttributeError
            - "warn": Raise a UserWarning

        verbose : bool (optional, default=False)
            Whether to print a downloading progress bar to terminal. Has no
            effect for download=False.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds 5000.

        ValueError
            If the integrity_action parameter is not one of the allowed ones.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/AffiliationSearch.html.

        Notes
        -----
        The directory for cached results is `{path}/STANDARD/{fname}`,
        where  `path` is specified in `~/.scopus/config.ini` and fname is
        the md5-hashed version of `query`.
        """
        # Checks
        check_integrity_params(integrity_action)

        # Query
        self.query = query
        Search.__init__(self, query=query, api="AffiliationSearch",
                        refresh=refresh, count=count, download=download,
                        verbose=verbose, view="STANDARD")
        self.integrity = integrity_fields or []
        self.action = integrity_action

    def __str__(self):
        """Return a summary string."""
        res = [a['affiliation-name'] for a in self._json]
        return make_search_summary(self, "affiliation", res)
