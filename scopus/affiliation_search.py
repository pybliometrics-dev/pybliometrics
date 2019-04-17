from collections import namedtuple
from warnings import warn

from scopus.classes import Search


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

    def __init__(self, query, count=200, start=0, max_entries=5000,
                 refresh=False, download=True):
        """Class to perform a search for an affiliation.

        Parameters
        ----------
        query : str
            A string of the query, e.g. "af-id(60021784)".

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        start : int (optional, default=0)
            DEPRECATED! The entry number of the first search item
            to start with.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        max_entries : int (optional, default=5000)
            DEPRECATED!  Raise error when the number of results is
            beyond this number.  The Affiliation Search API does not
            allow more than 5000 entries.

        download : bool (optional, default=True)
            Whether to download results (if they have not been cached).

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds max_entries.

        Notes
        -----
        Json results are cached in ~/.scopus/affiliation_search/{fname},
        where fname is the md5-hashed version of query.
        """
        if max_entries != 5000:
            text = "Parameter max_entries is deprecated and will be removed "\
                   "in scopus 1.6."
            warn(text, UserWarning)
        if start != 0:
            text = "Parameter start is deprecated and will be removed "\
                   "in scopus 1.6."
            warn(text, UserWarning)
        self.query = query
        Search.__init__(self, query=query, api="AffiliationSearch",
                        refresh=refresh, count=count, start=start,
                        max_entries=max_entries, download_results=download)

    def __str__(self):
        s = """Search {} yielded {} affiliation(s):\n    {}"""
        return s.format(self.query, len(self._json),
                        entries='\n    '.join([str(a) for a in self._json]))
