"""Superclass to access all Scopus search APIs and dump the results."""

from hashlib import md5
from pathlib import Path

from pybliometrics.scopus.superclasses import Base
from pybliometrics.scopus.utils import get_config, URLS


class Search(Base):
    def __init__(self,
                 query: str,
                 api: str,
                 size: int = 200,
                 cursor: bool = False,
                 download: bool = True,
                 verbose: bool = False,
                 **kwds: str
                 ) -> None:
        """Class intended as superclass to perform a search query.

        :param query : A string of the query.
        :param api: The name of the Scopus API to be accessed.  Allowed values:
                    AffiliationSearch, AuthorSearch, ScopusSearch,
                    SerialSearch, SubjectClass.
        :param size: The number of entries to be displayed at once.  A smaller
                     number means more queries with each query having
                     fewer results.
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
        # Construct query parameters
        params = {'size': size, 'view': self._view, **kwds}
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
        Base.__init__(self, params=params, url=URLS[api], download=download,
                      api=api, verbose=verbose)

    def get_results_size(self) -> int:
        """Return the number of results (works even if download=False)."""
        return self._n
