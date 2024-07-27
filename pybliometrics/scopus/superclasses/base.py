"""Base class object for superclasses."""

from json import dumps, loads
from math import ceil
from time import localtime, strftime, time
from typing import Dict, Optional

from tqdm import tqdm

from pybliometrics.scopus.exception import ScopusQueryError
from pybliometrics.scopus.utils import get_content, parse_content, SEARCH_MAX_ENTRIES


class Base:
    def __init__(self,
                 params: Dict,
                 url: str,
                 api: str,
                 download: bool = True,
                 verbose: bool = False,
                 *args: str, **kwds: str
                 ) -> None:
        """Class intended as base class for superclasses.

        :param params: Dictionary used as header during the API request.
        :param url: The URL to be accessed.
        :param api: The Scopus API to be accessed.
        :param download: Whether to download the query or not.  Has no effect
                         for retrieval requests.
        :param verbose: Whether to print a download progress bar.
        :param args: Keywords passed on `get_content()`
        :param kwds: Keywords passed on `get_content()`

        Raises
        ------
        ValueError
            If `self._refresh` is neither boolean nor numeric.
        """
        # Checks
        try:
            _ = int(self._refresh)
        except ValueError:
            msg = "Parameter refresh needs to be numeric or boolean."
            raise ValueError(msg)

        # Compare age of file to test whether we refresh
        self._refresh, mod_ts = _check_file_age(self)

        # Read or download, possibly with caching
        fname = self._cache_file_path

        # Check if search request
        search_request = "query" in params
        # Check if ref retrieval for abstract
        ab_ref_retrieval = (api == 'AbstractRetrieval') and (params['view'] == 'REF')

        if fname.exists() and not self._refresh:
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

            if ab_ref_retrieval:
                kwds['startref'] = '1'
                data = _get_all_refs(url, params, verbose, resp, *args, **kwds)
                self._json = data
                data = [data]
            elif search_request:
                # Get number of results
                res = resp.json()
                n = int(res['search-results'].get('opensearch:totalResults', 0))
                self._n = n
                # Results size check
                cursor_exists = "cursor" in params
                if not cursor_exists and n > SEARCH_MAX_ENTRIES:
                    # Stop if there are too many results
                    text = f'Found {n:,} matches.  The query fails to return '\
                           f'more than {SEARCH_MAX_ENTRIES} entries.  Change '\
                           'your query such that it returns fewer entries.'
                    raise ScopusQueryError(text)
                self._json = []
                # Download results page-wise
                if download:
                    data = res.get('search-results', {}).get('entry', [])
                    if not n:
                        data = ""
                    if not cursor_exists:
                        start = params["start"]
                    # Download the remaining information in chunks
                    if verbose:
                        print(f'Downloading results for query "{params["query"]}":')
                    n_chunks = ceil(n/params['size'])
                    for i in tqdm(range(1, n_chunks), disable=not verbose,
                                  initial=1, total=n_chunks):
                        if cursor_exists:
                            cursor = res['search-results']['cursor']['@next']
                            params.update({'cursor': cursor})
                        else:
                            start += params["size"]
                            params.update({'start': start})
                        resp = get_content(url, api, params, *args, **kwds)
                        res = resp.json()
                        data.extend(res.get('search-results', {}).get('entry', []))
                    header = resp.headers  # Use header of final call
                    self._json = data
                else:
                    data = None
            else:
                data = loads(resp.text)
                self._json = data
                data = [data]
            # Set private variables
            self._mdate = time()
            self._header = header
            # Finally write data unless download=False
            if download:
                text = [dumps(item, separators=(',', ':')) for item in data]
                fname.write_text("\n".join(text))

    def get_cache_file_age(self) -> int:
        """Return the age of the cached file in days."""
        diff = time() - self._mdate
        return int(diff / 86400)

    def get_cache_file_mdate(self) -> str:
        """Return the modification date of the cached file."""
        return strftime('%Y-%m-%d %H:%M:%S', localtime(self._mdate))

    def get_key_remaining_quota(self) -> Optional[str]:
        """Return number of remaining requests for the current key and the
        current API (relative on last actual request).
        """
        try:
            return self._header['X-RateLimit-Remaining']
        except AttributeError:
            return None

    def get_key_reset_time(self) -> Optional[str]:
        """Return time when current key is reset (relative on last
        actual request).
        """
        try:
            date = int(self._header['X-RateLimit-Reset'])
            return strftime('%Y-%m-%d %H:%M:%S', localtime(date))
        except AttributeError:
            return None


def _check_file_age(self):
    """Whether a file needs to be refreshed based on its age."""
    refresh = self._refresh
    try:
        mod_ts = self._cache_file_path.stat().st_mtime
        if not isinstance(refresh, bool):
            diff = time() - mod_ts
            days = int(diff / 86400) + 1
            allowed_age = int(self._refresh)
            refresh = allowed_age < days
    except FileNotFoundError:
        refresh = True
        mod_ts = None
    return refresh, mod_ts


def _get_all_refs(url: str, params: dict, verbose: bool, resp: dict, *args, **kwds) -> dict:
    """Get all references for `AbstractRetrieval` with view `REF`."""
    # startref starts at 1 (0 does not work)
    # Max refs per query are 40
    # Use of refcount leads to errors
    res = resp.json()
    path_total_references = ['abstracts-retrieval-response', 'references', '@total-references']
    try:
        n = int(parse_content.chained_get(res, path_total_references))
    except TypeError:
        return res

    data  = res #data is used to gather all responses. res is a tmp variable

    path_reference = ['abstracts-retrieval-response', 'references', 'reference']
    ref_len = len(parse_content.chained_get(data, path_reference))
    n_chunks = ceil(n/ref_len)

    for i in tqdm(range(1, n_chunks), disable=not verbose,
                  initial=1, total=n_chunks):
        # Increment startref
        kwds['startref'] = str(int(kwds['startref']) + ref_len)
        # Get
        resp = get_content(url, 'AbstractRetrieval', params, *args, **kwds)
        res = resp.json()
        res = parse_content.chained_get(res, path_reference)
        # Append
        data['abstracts-retrieval-response']['references']['reference'].extend(res)
        if verbose:
            print(f'Extracted:\n\tFrom: {kwds["startref"]}\n\tTo:{len(parse_content.chained_get(data, ["abstracts-retrieval-response", "references", "reference"]))}')

    if verbose:
        print(f'Total data: {len(parse_content.chained_get(data, ["abstracts-retrieval-response", "references", "reference"]))}')

    return data
