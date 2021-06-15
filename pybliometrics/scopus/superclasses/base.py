"""Base class object for superclasses."""

from json import dumps, loads
from time import localtime, strftime, time

from pybliometrics.scopus.exception import ScopusQueryError
from pybliometrics.scopus.utils import get_content
from tqdm import tqdm


class Base:
    def __init__(self, fname, refresh, params, url, api, download=None,
                 max_entries=None, verbose=False, *args, **kwds):
        """Class intended as base class for superclasses.

        Parameters
        ----------
        fname : PosixPath or WindowsPath
            The filename as Path() object.

        refresh : bool or int
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        params : dict
            Dictionary used as header during the API request.

        url : str
            The URL to be accessed.

        api : str
            The Scopus API to be accessed.

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
        refresh, mod_ts = _check_file_age(fname, refresh)

        # Read or dowload, possibly with caching
        search_request = "query" in params
        if fname.exists() and not refresh:
            self._mdate = mod_ts
            if search_request:
                self._json = [loads(line) for line in
                              fname.read_text().split("\n") if line]
                self._n = len(self._json)
            else:
                self._json = loads(fname.read_text())
        else:
            resp = get_content(url, api, params, *args, **kwds)
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
                    data = ""
                    if n:
                        data, header = _parse(res, n, url, api, params,
                                              verbose, *args, **kwds)
                        self._json = data
                else:
                    data = None
            else:
                data = loads(resp.text)
                self._json = data
            # Set private variables
            self._mdate = time()
            self._header = header
            # Finally write data
            data = data or ""
            if not search_request:
                data = [data]
            text = [dumps(item, separators=(',', ':')) for item in data]
            fname.write_text("\n".join(text))

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
    try:
        mod_ts = fname.stat().st_mtime
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
        refresh = True
        mod_ts = None
    return refresh, mod_ts


def _parse(res, n, url, api, params, verbose, *args, **kwds):
    """Auxiliary function to download results and parse json."""
    cursor = "cursor" in params
    if not cursor:
        start = params["start"]
    _json = res.get('search-results', {}).get('entry', [])
    if verbose:
        # Roundup + 1 for the final iteration
        print(f'Downloading results for query "{params["query"]}":')
        n_chunks = int(n/params['count']) + (n % params['count'] > 0) + 1
        pbar = tqdm(total=n_chunks)
        pbar.update(1)
    # Download the remaining information in chunks
    while n > 0:
        n -= params["count"]
        if cursor:
            pointer = res['search-results']['cursor'].get('@next')
            params.update({'cursor': pointer})
        else:
            start += params["count"]
            params.update({'start': start})
        resp = get_content(url, api, params, *args, **kwds)
        res = resp.json()
        _json.extend(res.get('search-results', {}).get('entry', []))
        if verbose:
            pbar.update(1)
    if verbose:
        pbar.close()
    return _json, resp.headers
