"""Superclass to access all search APIs and dump the results."""

from json import dumps, loads
from os.path import exists

from scopus.utils import download, get_content


class Search:
    def __init__(self, query, filepath, url, refresh, count=200, start=0,
                 max_entries=5000, view='STANDARD'):
        """Class intended as superclass to perform a search query.

        Parameters
        ----------
        query : str
            A string of the query.

        filepath : str
            The complete filepath and -name of the cached file.

        url : str
            The API access point.

        refresh : bool
            Whether to refresh the cached file if it exists or not.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        start : int (optional, default=0)
            The entry number of the first search item to start with.

        max_entries : int (optional, default=5000)
            Raise error when the number of results is beyond this number.
            The Scopus Search Engine does not allow more than 5000 entries.

        view : str (optional, default=STANDARD)
            The view of the file that should be downloaded.  Will not take
            effect for already cached files.  Allowed values: STANDARD,
            COMPLETE.
            Note: Only the Scopus search API additionally uses view COMPLETE.

        Raises
        ------
        Exception
            If the number of search results exceeds max_entries.

        ValueError
            If the view parameters contains invalid entries.
        """
        allowed_views = ('STANDARD', 'COMPLETE')
        if view not in allowed_views:
            raise ValueError('view parameter must be one of ' +
                             ', '.join(allowed_views))
        # Read the file contents if it exists and we are not refreshing
        if not refresh and exists(filepath):
            self._json = []
            with open(filepath) as f:
                for r in f.readlines():
                    self._json.append(loads(r))
        # Download file if cached file doesn't exists or we are refreshing
        else:
            # First, get a count of how many things to retrieve
            params = {'query': query, 'count': 0, 'start': 0, 'view': view}
            res = get_content(filepath, url=url, refresh=refresh, params=params,
                              accept='json')
            data = loads(res.decode('utf-8'))['search-results']
            N = int(data.get('opensearch:totalResults', 0))
            if N > max_entries:
                raise Exception(('Found {} matches. '
                                 'Set max_entries to a higher number or '
                                 'change your query ({})').format(N, query))

            # Then download the information in chunks
            self._json = []
            while N > 0:
                params.update({'count': count, 'start': start})
                res = download(url=url, params=params, accept="json")
                results = res.json()

                if 'entry' in results.get('search-results', []):
                    for r in results['search-results']['entry']:
                        self._json.append({f: r[f] for f in r.keys()})
                start += count
                N -= count

            # Finally write out the file
            with open(filepath, 'wb') as f:
                for item in self._json:
                    f.write('{}\n'.format(dumps(item)).encode('utf-8'))
