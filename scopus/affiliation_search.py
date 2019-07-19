from collections import namedtuple

from pybliometrics.scopus.classes import Search


class AffiliationSearch(Search):
    @property
    def affiliations(self):
        """A list of namedtuples storing affiliation information,
        where each namedtuple corresponds to one affiliation.
        The information in each namedtuple is (eid name variant documents city
        country parent).

        All entries are strings or None.  variant combines variants of names
        with a semicolon.
        """
        out = []
        order = 'eid name variant documents city country parent'
        aff = namedtuple('Affiliation', order)
        for item in self._json:
            name = item.get('affiliation-name')
            variants = [d.get('$', "") for d in item.get('name-variant', [])
                        if d.get('$', "") != name]
            new = aff(eid=item['eid'], variant=";".join(variants),
                      documents=item.get('document-count', '0'), name=name,
                      city=item.get('city'), country=item.get('country'),
                      parent=item.get('parent-affiliation-id'))
            out.append(new)
        return out or None

    def __init__(self, query, refresh=False, download=True, count=200, verbose=False):
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

        verbose : bool (optional, default=False)
            Whether to print a downloading progress bar to terminal. Has no effect for download=False.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds 5000.

        Notes
        -----
        Json results are cached in ~/.scopus/affiliation_search/STANDARD/{fname},
        where fname is the md5-hashed version of query.
        """
        view = "STANDARD"  # In case Scopus adds different views in future

        self.query = query
        Search.__init__(self, query=query, api="AffiliationSearch",
                        refresh=refresh, count=count, download=download, verbose=verbose)

    def __str__(self):
        s = """Search {} yielded {} affiliation(s):\n    {}"""
        return s.format(self.query, len(self._json),
                        entries='\n    '.join([str(a) for a in self._json]))
