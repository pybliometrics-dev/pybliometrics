"""Superclass to access all search APIs and dump the results."""

from hashlib import md5
from json import dumps, loads
from os.path import exists, join

from scopus import config
from scopus.exception import ScopusQueryError
from scopus.utils import create_config, download, get_content

BASE_URL = 'https://api.elsevier.com/content/search/'
URL = {'AffiliationSearch': BASE_URL + 'affiliation',
       'AuthorSearch': BASE_URL + 'author',
       'ScopusSearch': BASE_URL + 'scopus'}


class Search:
    def __init__(self, query, api, refresh, count=200, start=0,
                 max_entries=5000, view='STANDARD'):
        """Class intended as superclass to perform a search query.

        Parameters
        ----------
        query : str
            A string of the query.

        api : str
            The name of the Scopus API to be accessed.  Allowed values:
            AffiliationSearch, AuthorSearch, ScopusSearch.

        refresh : bool
            Whether to refresh the cached file if it exists or not.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        start : int (optional, default=0)
            The entry number of the first search item to start with.

        max_entries : int (optional, default=5000)
            Raise error when the number of results is beyond this number.
            The Scopus Search Engine does not allow more than 5000 entries.

        view : str (optional, default=STANDARD)
            The view of the file that should be downloaded.  Will not take
            effect for already cached files.  Allowed values: STANDARD,
            COMPLETE.
            Note: Only the ScopusSearch API additionally uses view COMPLETE.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds max_entries.

        ValueError
            If the api parameter or view parameter is an invalid entry.
        """
        # Checks
        if api not in URL:
            raise ValueError('api parameter must be one of ' +
                             ', '.join(URL.keys()))
        allowed_views = ('STANDARD', 'COMPLETE')
        if view not in allowed_views:
            raise ValueError('view parameter must be one of ' +
                             ', '.join(allowed_views))
        if not config.has_section('Directories'):
            create_config()

        # Read the file contents if file exists and we are not refreshing,
        # otherwise download query anew and cache file
        qfile = join(config.get('Directories', api),
                     md5(query.encode('utf8')).hexdigest())
        if not refresh and exists(qfile):
            with open(qfile, "rb") as f:
                self._json = [loads(line) for line in f.readlines()]
        else:
            # Get a count of how many things to retrieve from first chunk
            params = {'query': query, 'count': count, 'start': 0, 'view': view}
            res = download(url=URL[api], params=params, accept="json").json()
            n = int(res['search-results'].get('opensearch:totalResults', 0))
            if n > max_entries:  # Stop if there are too many results
                text = ('Found {} matches. Set max_entries to a higher '
                        'number or change your query ({})'.format(n, query))
                raise ScopusQueryError(text)
            self._json = res.get('search-results', {}).get('entry', [])
            if n == 0:
                self._json = ""
            # Download the remaining information in chunks
            while n > 0:
                n -= count
                start += count
                params.update({'count': count, 'start': start})
                res = download(url=URL[api], params=params, accept="json").json()
                self._json.extend(res.get('search-results', {}).get('entry', []))
            # Finally write out the file
            with open(qfile, 'wb') as f:
                for item in self._json:
                    f.write('{}\n'.format(dumps(item)).encode('utf-8'))
