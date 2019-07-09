from collections import namedtuple

from pybliometrics.scopus.classes import Search


class AuthorSearch(Search):
    @property
    def authors(self):
        """A list of namedtuples storing author information,
        where each namedtuple corresponds to one author.
        The information in each namedtuple is (eid surname initials givenname
        documents affiliation affiliation_id city country areas).

        All entries are strings or None.  Areas combines abbreviated subject
        areas followed by the number of documents in this subject.
        """
        out = []
        order = 'eid surname initials givenname affiliation documents '\
                'affiliation_id city country areas'
        auth = namedtuple('Author', order)
        for item in self._json:
            name = item.get('preferred-name', {})
            aff = item.get('affiliation-current', {})
            fields = item.get('subject-area',
                              [{'@abbrev': '', '@frequency': ''}])
            if isinstance(fields, dict):
                fields = [fields]
            areas = ["{} ({})".format(d.get('@abbrev', ''),
                                      d.get('@frequency', ''))
                     for d in fields]
            new = auth(eid=item['eid'], initials=name.get('initials'),
                       surname=name.get('surname'), areas="; ".join(areas),
                       givenname=name.get('given-name'),
                       documents=item.get('document-count', '0'),
                       affiliation=aff.get('affiliation-name'),
                       affiliation_id=aff.get('affiliation-id'),
                       city=aff.get('affiliation-city'),
                       country=aff.get('affiliation-country'))
            out.append(new)
        return out or None

    def __init__(self, query, refresh=False, count=200, download=True):
        """Class to search a query, and retrieve a list of author IDs as results.

        Parameters
        ----------
        query : str
            A string of the query, e.g. "authlast(Einstein) and
            authfirst(Albert)".

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        download : bool (optional, default=True)
            Whether to download results (if they have not been cached).

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds 5000.

        Notes
        -----
        Json results are cached in ~/.scopus/author_search/STANDARD/{fname},
        where fname is the md5-hashed version of query.
        """
        view = "STANDARD"  # In case Scopus adds different views in future
        self.query = query
        Search.__init__(self, query=query, refresh=refresh, view=view,
                        api='AuthorSearch', count=count, download=download)

    def __str__(self):
        s = """Search {} yielded {} author(s):\n    {}"""
        return s.format(self.query, len(self._json),
                        '\n    '.join([str(a) for a in self._json]))
