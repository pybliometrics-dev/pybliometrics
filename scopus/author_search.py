from collections import namedtuple
from warnings import warn

from scopus.classes import Search


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
            areas = ["{} ({})".format(d.get('@abbrev', ''), d.get('@frequency', ''))
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

    def __init__(self, query, count=200, start=0, max_entries=5000,
                 refresh=False, download=True):
        """Class to search a query, and retrieve a list of author IDs as results.

        Parameters
        ----------
        query : str
            A string of the query, e.g. "authlast(Einstein) and
            authfirst(Albert)".

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
        Json results are cached in ~/.scopus/author_search/{fname},
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
        Search.__init__(self, query=query, api='AuthorSearch', refresh=refresh,
                        count=count, start=start, max_entries=max_entries,
                        download_results=download)

    def __str__(self):
        s = """Search {} yielded {} author(s):\n    {}"""
        return s.format(self.query, len(self._json),
                        '\n    '.join([str(a) for a in self._json]))
