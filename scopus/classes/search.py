"""Superclass to access all search APIs and dump the results."""

from hashlib import md5
from json import dumps, loads
from os.path import exists, join
from warnings import warn

from scopus.exception import ScopusQueryError
from scopus.utils import SEARCH_URL, download, get_content, get_folder


class Search:
    def __init__(self, query, api, refresh, count=200, max_entries=5000,
                 view='STANDARD', cursor=False, download_results=True, **kwds):
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

        download_results : bool (optional, default=True)
            Whether to download results (if they have not been cached) or not.

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
        if api not in SEARCH_URL:
            raise ValueError('api parameter must be one of ' +
                             ', '.join(SEARCH_URL.keys()))

        # Read the file contents if file exists and we are not refreshing,
        # otherwise download query anew and cache file
        qfile = join(get_folder(api), md5(query.encode('utf8')).hexdigest())
        if not refresh and exists(qfile):
            with open(qfile, "rb") as f:
                self._json = [loads(line) for line in f.readlines()]
            self._n = n = len(self._json)
        else:
            # Set query parameters
            params = {'query': query, 'count': count, 'view': view}
            if cursor:
                params.update({'cursor': '*'})
            else:
                params.update({'start': 0})
            # Download results
            res = download(url=SEARCH_URL[api], params=params, accept="json", **kwds).json()
            n = int(res['search-results'].get('opensearch:totalResults', 0))
            self._n = n
            if not cursor and n > max_entries:  # Stop if there are too many results
                text = ('Found {} matches. Set max_entries to a higher '
                        'number, change your query ({}) or set '
                        'subscription=True'.format(n, query))
                raise ScopusQueryError(text)
            if download_results:
                self._json = _parse(res, params, n, api, **kwds)
                # Finally write out the file
                with open(qfile, 'wb') as f:
                    for item in self._json:
                        f.write('{}\n'.format(dumps(item)).encode('utf-8'))

    def get_results_size(self):
        """Return the number of results (works even if download=False)."""
        return self._n


def _parse(res, params, n, api, **kwds):
    """Auxiliary function to download results and parse json."""
    cursor = "cursor" in params
    if not cursor:
        start = params["start"]
    if n == 0:
        return ""
    _json = res.get('search-results', {}).get('entry', [])
    # Download the remaining information in chunks
    while n > 0:
        n -= params["count"]
        if cursor:
            pointer = res['search-results']['cursor'].get('@next')
            params.update({'cursor': pointer})
        else:
            start += params["count"]
            params.update({'start': start})
        res = download(url=SEARCH_URL[api], params=params, accept="json", **kwds).json()
        _json.extend(res.get('search-results', {}).get('entry', []))
    return _json
