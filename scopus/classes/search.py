"""Superclass to access all search APIs and dump the results."""

from hashlib import md5
from json import dumps, loads
from os.path import exists, join
from warnings import warn

from scopus import config
from scopus.exception import ScopusQueryError
from scopus.utils import create_config, download, get_content

BASE_URL = 'https://api.elsevier.com/content/search/'
URL = {'AffiliationSearch': BASE_URL + 'affiliation',
       'AuthorSearch': BASE_URL + 'author',
       'ScopusSearch': BASE_URL + 'scopus'}


class Search:
    def __init__(self, query, api, refresh, count=200, start=0,
                 max_entries=5000, view='STANDARD', cursor=False, **kwds):
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
            DEPRECATED! The entry number of the first search item
            to start with.

        max_entries : int (optional, default=5000)
            Raise error when the number of results is beyond this number.
            To skip this check, set `max_entries` to `None`.

        view : str (optional, default=STANDARD)
            The view of the file that should be downloaded.  Will not take
            effect for already cached files.

        cursor : str (optional, default=False)
            Whether to use the cursor in order to iterate over all search
            results without limit on the number of the results.  In contrast
            to `start` parameter, the `cursor` parameter does not allow users
            to obtain partial results.

        kwds : key-value parings, optional
            Keywords passed on to requests header.  Must contain fields
            and values specified in the respective API specification.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds max_entries.

        ValueError
            If the api parameteris an invalid entry.
        """
        # Checks
        if api not in URL:
            raise ValueError('api parameter must be one of ' +
                             ', '.join(URL.keys()))
        if not config.has_section('Directories'):
            create_config()
        if start != 0:
            text = "Parameter start is deprecated and will be removed "\
                   "in scopus 1.6."
            warn(text, UserWarning)

        # Read the file contents if file exists and we are not refreshing,
        # otherwise download query anew and cache file
        qfile = join(config.get('Directories', api),
                     md5(query.encode('utf8')).hexdigest())
        if not refresh and exists(qfile):
            with open(qfile, "rb") as f:
                self._json = [loads(line) for line in f.readlines()]
        else:
            # Get a count of how many things to retrieve from first chunk
            params = {'query': query, 'count': count, 'view': view}
            if cursor:
                params.update({'cursor': '*'})
            else:
                params.update({'start': 0})
            res = download(url=URL[api], params=params, accept="json", **kwds).json()
            n = int(res['search-results'].get('opensearch:totalResults', 0))
            if not cursor and n > max_entries:  # Stop if there are too many results
                text = ('Found {} matches. Set max_entries to a higher '
                        'number, change your query ({}) or set '
                        'subscription=True'.format(n, query))
                raise ScopusQueryError(text)
            self._json = res.get('search-results', {}).get('entry', [])
            if n == 0:
                self._json = ""
            # Download the remaining information in chunks
            while n > 0:
                n -= count
                params.update({'count': count})
                if cursor:
                    pointer = res['search-results']['cursor'].get('@next')
                    params.update({'cursor': pointer})
                else:
                    start += count
                    params.update({'start': start})
                res = download(url=URL[api], params=params, accept="json", **kwds).json()
                self._json.extend(res.get('search-results', {}).get('entry', []))
            # Finally write out the file
            with open(qfile, 'wb') as f:
                for item in self._json:
                    f.write('{}\n'.format(dumps(item)).encode('utf-8'))
