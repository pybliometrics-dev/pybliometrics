"""Superclass to access all Scopus search APIs and dump the results."""

from hashlib import md5
from operator import index
from pathlib import Path

from pybliometrics.superclasses import Base
from pybliometrics.utils import get_config, COUNTS, URLS


class Search(Base):
    def __init__(self,
                 query: str | dict,
                 cursor: bool = False,
                 download: bool = True,
                 verbose: bool = False,
                 max_pages: int | None = None,
                 **kwds: str
                 ) -> None:
        """Class intended as superclass to perform a search query.

        :param query : A string of the query.
        :param cursor: Whether to use the cursor in order to iterate over all
                       search results without limit on the number of the results.
                       In contrast to `start` parameter, the `cursor` parameter
                       does not allow users to obtain partial results.
        :param download: Whether to download results (if they have not been
                         cached) or not.
        :param verbose: Whether to print a download progress bar.
        :param max_pages: Maximum number of result pages to download.
        :param kwds: Keywords passed on to requests header.  Must contain
                     fields and values specified in the respective API specification.

        Raises
        ------
        ValueError
            If the api parameter is an invalid entry or `max_pages` is not a
            positive integer.
        """
        if max_pages is not None:
            try:
                max_pages = index(max_pages)
            except TypeError:
                raise ValueError("Parameter 'max_pages' must be a positive integer.")
            if max_pages < 1:
                raise ValueError("Parameter 'max_pages' must be a positive integer.")

        api = self.__class__.__name__
        # Construct query parameters
        count = COUNTS[api][self._view]
        params = {'count': count, 'view': self._view, **kwds}
        if isinstance(query, dict):
            params.update(query)
            name = "&".join(["=".join(t) for t in query.items()])
        else:
            params['query'] = query
            name = query
        # Cache key must reflect all user-supplied parameters affecting results
        extra = {**kwds}
        if max_pages is not None:
            extra['max_pages'] = max_pages
        if extra:
            name += "&" + "&".join(f"{k}={v}" for k, v in sorted(extra.items()))
        if cursor:
            params.update({'cursor': '*'})
        else:
            if "start" not in params:
                params['start'] = 0

        # Construct cache file path
        stem = md5(name.encode('utf8')).hexdigest()
        # Get cache file path
        config = get_config()
        parent = Path(config.get('Directories', api))
        self._cache_file_path = parent/self._view/stem

        # Init
        Base.__init__(self, params=params, url=URLS[api], download=download,
                      verbose=verbose, max_pages=max_pages)

    def get_results_size(self) -> int:
        """Return the number of results (works even if download=False).
        If `max_pages` is set and `download=True`, returns the number of
        downloaded results rather than the total number of matches.
        """
        return self._n
