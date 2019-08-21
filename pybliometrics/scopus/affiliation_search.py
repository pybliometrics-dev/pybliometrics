from collections import namedtuple

from pybliometrics.scopus.classes import Search
from pybliometrics.scopus.utils import check_integrity, check_field_consistency


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
        """Class to perform a search for an affiliation.

        Parameters
        ----------
        query : str
            A string of the query, e.g. "af-id(60021784)".

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

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
            Whether to print a downloading progress bar to terminal. Has no effect for download=False.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds 5000.

        ValueError
            If the integrity_action parameter is not one of the allowed ones.

        Notes
        -----
        Json results are cached in ~/.scopus/affiliation_search/STANDARD/{fname},
        where fname is the md5-hashed version of query.
        """
        # Checks
        allowed_actions = ("warn", "raise")
        if integrity_action not in allowed_actions:
            msg = 'integrity_action parameter must be one of ' +\
                  ', '.join(allowed_actions)
            raise ValueError(msg)

        # Parameters
        view = "STANDARD"  # In case Scopus adds different views in future

        # Query
        self.query = query
        Search.__init__(self, query=query, api="AffiliationSearch",
                        refresh=refresh, count=count, download=download,
                        verbose=verbose)
        self.integrity = integrity_fields or []
        self.action = integrity_action

    def __str__(self):
        s = """Search {} yielded {} affiliation(s):\n    {}"""
        return s.format(self.query, len(self._json),
                        entries='\n    '.join([str(a) for a in self._json]))
