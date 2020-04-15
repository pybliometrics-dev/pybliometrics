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
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

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

        ValueError
            If `refresh` is neither boolean nor numeric.
        """
        # Compare age of file to test whether we refresh
        refresh, exists, mod_ts = _check_file_age(fname, refresh)

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
                self._n = n
                cursor_false = "cursor" in params and not params["cursor"]
                if cursor_false and n > max_entries:
                    # Stop if there are too many results
                    text = (f'Found {n} matches. Set max_entries to a higher '
                            f'number, change your query ({query}) or set '
                            'subscription=True')
                    raise ScopusQueryError(text)
                if download:
                    self._json = _parse(res, n, url, params, verbose,
                                        *args, **kwds)
                    with open(fname, 'wb') as f:
                        for item in self._json:
                            f.write(f'{dumps(item)}\n'.encode('utf-8'))
                else:
                    # Assures that properties will not result in an error
                    self._json = []
            else:
                content = get_content(url, params, *args, **kwds).text.encode('utf-8')
                self._json = loads(content)
                with open(fname, 'wb') as f:
                    f.write(content)
            self._mdate = time()

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


def _check_file_age(fname, refresh):
    """Check whether a file needs to be refreshed based on its age."""
    exists = None
    try:
        mod_ts = getmtime(fname)
        exists = True
        if not isinstance(refresh, bool):
            diff = time() - mod_ts
            days = int(diff / 86400) + 1
            try:
                allowed_age = int(refresh)
            except ValueError:
                msg = "Parameter refresh needs to be numeric or boolean."
                raise ValueError(msg)
            refresh = allowed_age < days
    except FileNotFoundError:
        exists = False
        refresh = True
        mod_ts = None
    return refresh, exists, mod_ts


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
        print(f'Downloading results for query "{params["query"]}":')
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
