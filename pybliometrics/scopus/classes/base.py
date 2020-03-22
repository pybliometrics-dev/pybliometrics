"""Base class object for superclasses."""

from json import dumps, loads
from os.path import getmtime
from time import time

from pybliometrics.scopus.exception import ScopusQueryError
from pybliometrics.scopus.utils import get_content


class Base:
    def __init__(self, fname, refresh, params, url, download=None,
                 max_entries=None, verbose=False, *args, **kwds):
        """Class intended as base class for superclasses.

        Parameters
        ----------
        fname : str
            The filename (including path) of the cache object.

        refresh : bool or int
            Whether to refresh the cached file if it exists or not. If int
            is passed, value will be interpreted as allowed age measured
            in number of days. When the number of days since the cached
            file was last modified exceeds the allowed age, the file will
            be refreshed.

        params : dict
            Dictionary used as header during the API request.

        url : str
            The URL to be accessed.

        download : bool (optional, default=None)
            Whether to download the query or not.  Has no effect for
            retrieval requests.

        max_entries : int (optional, default=None)
            Raise error when the number of results is beyond this number.
            Has no effect for retrieval requests.

        verbose : bool (optional, default=False)
            Whether to print a progress bar for multip-page requests.

        *args, **kwds
            Arguments and key-value pairings to be passed on
            to `get_content()`.

        Raises
        ------
        ScopusQueryError
            If `refresh` is neither boolean nor numeric.
        """
        # Compare age of file
        now = time()
        exists = None
        try:
            mod_ts = getmtime(fname)
            exists = True
            if not isinstance(refresh, bool):
                diff = now - mod_ts
                days = int(diff / 86400) + 1
                try:
                    allowed_age = int(refresh)
                except ValueError:
                    raise ValueError("refresh parameter needs to be numeric.")
                refresh = allowed_age < days
        except FileNotFoundError:
            exists = False
            refresh = True

        # Read or dowload eventually with caching
        search_request = "query" in params
        if exists and not refresh:
            self._mdate = mod_ts
            if search_request:
                with open(fname, 'rb') as f:
                    self._json = [loads(line) for line in f.readlines()]
                self._n = len(self._json)
            else:
                with open(fname, 'rb') as f:
                    self._json = loads(f.read().decode('utf-8'))
        else:
            if search_request:
                # Download results
                res = get_content(url, params, *args, **kwds).json()
                n = int(res['search-results'].get('opensearch:totalResults', 0))
                print(n)
                self._n = n
                if "cursor" in params and not params["cursor"] and n > max_entries:
                    # Stop if there are too many results
                    text = ('Found {} matches. Set max_entries to a higher '
                            'number, change your query ({}) or set '
                            'subscription=True'.format(n, query))
                    raise ScopusQueryError(text)
                if download:
                    self._json = _parse(res, n, url, params, verbose,
                                        *args, **kwds)
                    with open(fname, 'wb') as f:
                        for item in self._json:
                            f.write('{}\n'.format(dumps(item)).encode('utf-8'))
                else:
                    # Assures that properties will not result in an error
                    self._json = []
            else:
                content = get_content(url, params, *args, **kwds).text.encode('utf-8')
                self._json = loads(content)
                with open(fname, 'wb') as f:
                    f.write(content)
            self._mdate = now

    def get_cache_file_age(self):
        """Return the age of the cached file in days."""
        diff = time() - self._mdate
        return int(diff / 86400)

    def get_cache_file_mdate(self):
        """Return the modification date of the cached file as
        datetime object.
        """
        from datetime import datetime
        return datetime.fromtimestamp(self._mdate)


def _parse(res, n, url, params, verbose, *args, **kwds):
    """Auxiliary function to download results and parse json."""
    cursor = "cursor" in params
    if not cursor:
        start = params["start"]
    if n == 0:
        return ""
    _json = res.get('search-results', {}).get('entry', [])
    if verbose:
        chunk = 1
        # Roundup + 1 for the final iteration
        chunks = int(n/params['count']) + (n % params['count'] > 0) + 1
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
        res = get_content(url, params, *args, **kwds).json()
        _json.extend(res.get('search-results', {}).get('entry', []))
        if verbose:
            chunk += 1
            print_progress(chunk, chunks)
    return _json
