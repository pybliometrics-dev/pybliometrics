"""Superclass to access all Scopus search APIs and dump the results."""

from hashlib import md5
from json import dumps, loads
from os.path import exists, join
from warnings import warn

from pybliometrics.scopus.exception import ScopusQueryError
from pybliometrics.scopus.utils import SEARCH_URL, cache_file, get_content,\
    get_folder, print_progress


class Search:
    def __init__(self, query, api, refresh, view='STANDARD', count=200,
                 max_entries=5000, cursor=False, download=True, verbose=False, **kwds):
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

        view : str
            The view of the file that should be downloaded.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        max_entries : int (optional, default=5000)
            Raise error when the number of results is beyond this number.
            To skip this check, set `max_entries` to `None`.


        cursor : str (optional, default=False)
            Whether to use the cursor in order to iterate over all search
            results without limit on the number of the results.  In contrast
            to `start` parameter, the `cursor` parameter does not allow users
            to obtain partial results.

        download : bool (optional, default=True)
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
        # Read the file contents if file exists and we are not refreshing,
        # otherwise download query anew and cache file
        fname = md5(query.encode('utf8')).hexdigest()
        qfile = join(get_folder(api, view), fname)
        if not refresh and exists(qfile):
            with open(qfile, "rb") as f:
                self._json = [loads(line) for line in f.readlines()]
            self._n = len(self._json)
        else:
            # Set query parameters
            params = {'query': query, 'count': count, 'view': view}
            if cursor:
                params.update({'cursor': '*'})
            else:
                params.update({'start': 0})
            # Download results
            res = cache_file(url=SEARCH_URL[api], params=params, **kwds).json()
            n = int(res['search-results'].get('opensearch:totalResults', 0))
            self._n = n
            if not cursor and n > max_entries:  # Stop if there are too many results
                text = ('Found {} matches. Set max_entries to a higher '
                        'number, change your query ({}) or set '
                        'subscription=True'.format(n, query))
                raise ScopusQueryError(text)
            if download:
                self._json = _parse(res, params, n, api, verbose, **kwds)
                # Finally write out the file
                with open(qfile, 'wb') as f:
                    for item in self._json:
                        f.write('{}\n'.format(dumps(item)).encode('utf-8'))
            else:
                # Assures that properties will not result in an error
                self._json = []
        self._view = view

    def get_results_size(self):
        """Return the number of results (works even if download=False)."""
        return self._n


def _parse(res, params, n, api, verbose, **kwds):
    """Auxiliary function to download results and parse json."""
    cursor = "cursor" in params
    if not cursor:
        start = params["start"]
    if n == 0:
        return ""
    _json = res.get('search-results', {}).get('entry', [])
    if verbose:
        chunk = 1
        chunks = int(n/params['count']) + (n % params['count'] > 0) + 1 #roundup + 1 for the final iteration
        print('Downloading results for query "{}":'.format(params['query']))
        print_progress(chunk, chunks)
    # Download the remaining information in chunks
    while n > 0:
        n -= params["count"]
        if cursor:
            pointer = res['search-results']['cursor'].get('@next')
            params.update({'cursor': pointer})
        else:
            start += params["count"]
            params.update({'start': start})
        res = cache_file(url=SEARCH_URL[api], params=params, **kwds).json()
        _json.extend(res.get('search-results', {}).get('entry', []))
        if verbose:
            chunk += 1
            print_progress(chunk, chunks)
    return _json
