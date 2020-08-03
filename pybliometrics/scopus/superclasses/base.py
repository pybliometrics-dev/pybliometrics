"""Base class object for superclasses."""

from json import dumps, loads
from os.path import getmtime
from time import localtime, strftime, time

from pybliometrics.scopus.exception import ScopusQueryError
from pybliometrics.scopus.utils import get_content, print_progress


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
            resp = get_content(url, params, *args, **kwds)
            header = resp.headers
            if search_request:
                # Get number of results
                res = resp.json()
                n = int(res['search-results'].get('opensearch:totalResults', 0))
                self._n = n
                self._json = []
                # Results size check
                cursor_false = "cursor" in params and not params["cursor"]
                if cursor_false and n > max_entries:
                    # Stop if there are too many results
                    text = (f'Found {n} matches. Set max_entries to a higher '
                            f'number, change your query ({query}) or set '
                            'subscription=True')
                    raise ScopusQueryError(text)
                # Download results page-wise
                if download:
                    data = "".encode('utf-8')
                    if n:
                        data, header = _parse(res, n, url, params, verbose,
                                              *args, **kwds)
                        self._json = data
                else:
                    data = None
            else:
                data = resp.text.encode('utf-8')
                self._json = loads(data)
            # Set private variables
            self._mdate = time()
            self._header = header
            # Finally write data
            _write_json(fname, data)

    def get_cache_file_age(self):
        """Return the age of the cached file in days."""
        diff = time() - self._mdate
        return int(diff / 86400)

    def get_cache_file_mdate(self):
        """Return the modification date of the cached file."""
        return strftime('%Y-%m-%d %H:%M:%S', localtime(self._mdate))

    def get_key_remaining_quota(self):
        """Return number of remaining requests for the current key and the
        current API (relative on last actual request).
        """
        try:
            return self._header['X-RateLimit-Remaining']
        except AttributeError:
            return None

    def get_key_reset_time(self):
        """Return time when current key is reset (relative on last
        actual request).
        """
        try:
            date = int(self._header['X-RateLimit-Reset'])/1000
            return strftime('%Y-%m-%d %H:%M:%S', localtime(date))
        except AttributeError:
            return None


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
        resp = get_content(url, params, *args, **kwds)
        res = resp.json()
        _json.extend(res.get('search-results', {}).get('entry', []))
        if verbose:
            chunk += 1
            print_progress(chunk, chunks)
    return _json, resp.headers


def _write_json(fname, data):
    """Auxiliary function to write json to a file."""
    if data is None:
        return None
    with open(fname, 'wb') as f:
        if isinstance(data, list):
            for item in data:
                f.write(f'{dumps(item)}\n'.encode('utf-8'))
        else:
            f.write(data)
