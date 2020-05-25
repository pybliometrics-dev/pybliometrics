"""Superclass to access all Scopus search APIs and dump the results."""

from hashlib import md5
from os.path import join

from pybliometrics.scopus.superclasses import Base
from pybliometrics.scopus.utils import SEARCH_URL, get_folder


class Search(Base):
    def __init__(self, query, api, refresh, view='STANDARD', count=200,
                 max_entries=5000, cursor=False, download=True,
                 verbose=False, **kwds):
        """Class intended as superclass to perform a search query.

        Parameters
        ----------
        query : str
            A string of the query.

        api : str
            The name of the Scopus API to be accessed.  Allowed values:
            AffiliationSearch, AuthorSearch, ScopusSearch.

        refresh : bool or int
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        view : str
            The view of the file that should be downloaded.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        max_entries : int (optional, default=5000)
            Raise error when the number of results is beyond this number.
            To skip this check, set `max_entries` to `None`. Has no
            effect if cursor=True.

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
            If the api parameter is an invalid entry.
        """
        params = {'count': count, 'view': view}
        if isinstance(query, dict):
            params.update(query)
            name = "&".join(["=".join(t) for t in zip(query.keys(), query.values())])
        else:
            params['query'] = query
            name = query
        fname = md5(name.encode('utf8')).hexdigest()
        qfile = join(get_folder(api, view), fname)
        if cursor:
            params.update({'cursor': '*'})
        else:
            params.update({'start': 0})
        Base.__init__(self, qfile, refresh, params=params, url=SEARCH_URL[api],
                      download=download, max_entries=max_entries, verbose=verbose)
        # Set query parameters
        self._view = view

    def get_results_size(self):
        """Return the number of results (works even if download=False)."""
        return self._n
