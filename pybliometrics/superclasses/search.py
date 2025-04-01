"""Superclass to access all Scopus search APIs and dump the results."""

from hashlib import md5
from pathlib import Path
from typing import Union

from pybliometrics.superclasses import Base
from pybliometrics.utils import get_config, COUNTS, URLS


class Search(Base):
    def __init__(self,
                 query: Union[str, dict],
                 cursor: bool = False,
                 download: bool = True,
                 verbose: bool = False,
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
        :param kwds: Keywords passed on to requests header.  Must contain
                     fields and values specified in the respective API specification.

        Raises
        ------
        ValueError
            If the api parameter is an invalid entry.
        """
        api = self.__class__.__name__
        # Construct query parameters
        count = COUNTS[api][self._view]
        params = {'count': count, 'view': self._view, **kwds}
        if isinstance(query, dict):
            params.update(query)
            name = "&".join(["=".join(t) for t in zip(query.keys(), query.values())])
        else:
            params['query'] = query
            name = query
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
        Base.__init__(self, params=params, url=URLS[api], download=download, verbose=verbose)

    def get_results_size(self) -> int:
        """Return the number of results (works even if download=False)."""
        return self._n
