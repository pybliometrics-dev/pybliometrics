import hashlib
import os
import sys
from collections import namedtuple
from json import dumps, loads

from scopus.utils import download, get_content

AUTHOR_SEARCH_DIR = os.path.expanduser('~/.scopus/author_search')

if not os.path.exists(AUTHOR_SEARCH_DIR):
    os.makedirs(AUTHOR_SEARCH_DIR)


FIELDS = ['eid', 'preferred-name', 'affiliation-current']


class AuthorSearch(object):
    @property
    def authors(self):
        """A list of namedtuples storing author information,
        where each namedtuple corresponds to one author.
        The information in each namedtuple is (eid surname initials givenname
        affiliation affiliation_id city country).
        All entries are strings or None.
        """
        out = []
        order = 'eid surname initials givenname affiliation '\
                'affiliation_id city country'
        auth = namedtuple('Author', order)
        for item in self._json:
            name = item.get('preferred-name', {})
            aff = item.get('affiliation-current', {})
            new = auth(eid=item['eid'],
                       surname=name.get('surname'),
                       initials=name.get('initials'),
                       givenname=name.get('given-name'),
                       affiliation=aff.get('affiliation-name'),
                       affiliation_id=aff.get('affiliation-id'),
                       city=aff.get('affiliation-city'),
                       country=aff.get('affiliation-country'))
            out.append(new)
        return self._json

    def __init__(self, query, fields=FIELDS, count=200, start=0,
                 max_entries=5000, refresh=False):
        """Class to search a query, and retrieve a list of author IDs as results.

        Parameters
        ----------
        query : str
            A string of the query, e.g. "authlast(Einstein) and
            authfirst(Albert)".

        fields : str (optional, default=['eid', 'preferred-name',
            'affiliation-current'])
            The fields you want returned.  Allowed fields are specified in
            https://dev.elsevier.com/guides/AuthorSearchViews.htm.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        start : int (optional, default=0)
            The entry number of the first search item to start with.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        max_entries : int (optional, default=5000)
            Raise error when the number of results is beyond this number.
            The Scopus Search Engine does not allow more than 5000 entries.

        Raises
        ------
        Exception
            If the number of search results exceeds max_entries.

        Notes
        -----
        Json results are cached in ~/.scopus/author_search/{fname}, where
        fname is the hashed version of query.

        The Authors are stored as a property named Authors.
        """

        self.query = query
        qfile = os.path.join(AUTHOR_SEARCH_DIR,
                             hashlib.md5(query.encode('utf8')).hexdigest())

        if os.path.exists(qfile) and not refresh:
            self._json = []
            with open(qfile) as f:
                for r in f.readlines():
                    self._json.append(loads(r))
        else:
            # No cached file exists, or we are refreshing.
            # First, we get a count of how many things to retrieve
            url = 'https://api.elsevier.com/content/search/author'
            params = {'query': query, 'count': 0, 'start': 0}
            res = get_content(qfile, url=url, refresh=refresh, params=params,
                              accept='json')
            data = loads(res.decode('utf-8'))['search-results']

            N = int(data.get('opensearch:totalResults', 0))

            if N > max_entries:
                raise Exception(('N = {}. '
                                 'Set max_entries to a higher number or '
                                 'change your query ({})').format(N, query))

            self._json = []
            while N > 0:
                params = {'query': query, 'count': count, 'start': start}
                resp = download(url=url, params=params, accept="json")
                results = resp.json()

                if 'entry' in results.get('search-results', []):
                    for r in results['search-results']['entry']:
                        self._json.append({f: r[f] for f in fields if f in r})
                start += count
                N -= count

            with open(qfile, 'wb') as f:
                for author in self._json:
                    f.write('{}\n'.format(dumps(author)).encode('utf-8'))

    def __str__(self):
        s = """{query}
        Resulted in {N} hits.
    {entries}"""
        return s.format(query=self.query, N=len(self._json),
                        entries='\n    '.join([str(a) for a in self._json]))
