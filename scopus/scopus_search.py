import os
import sys
import xml.etree.ElementTree as ET

from scopus.utils import download, get_content, get_encoded_text, ns

SCOPUS_SEARCH_DIR = os.path.expanduser('~/.scopus/search')

if not os.path.exists(SCOPUS_SEARCH_DIR):
    os.makedirs(SCOPUS_SEARCH_DIR)


class ScopusSearch(object):
    @property
    def EIDS(self):
        """Return list of EIDs retrieved."""
        return self._EIDS

    def __init__(self, query, fields='eid', count=200, start=0,
                 refresh=False, max_entries=1000):
        """Class to search a query, and retrieve a list of EIDs as results.

        Parameters
        ----------
        query : str
            A string of the query.

        fields : str (optional, default='eid')
            The list of fields you want returned.

        count : int (optional, default=200)
            The number of entries to be displayed.

        start : int (optional, default=0)
            The entry number of the first search item to start with.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        Notes
        -----
        XML results are cached in ~/.scopus/search/{query}.

        The EIDs are stored as a property.
        """

        self.query = query

        qfile = os.path.join(SCOPUS_SEARCH_DIR,
                             # We need to remove / in a DOI here so we can save
                             # it as a file.
                             query.replace('/', '_slash_'))

        if os.path.exists(qfile) and not refresh:
            with open(qfile) as f:
                self._EIDS = [eid for eid in
                              f.read().strip().split('\n')
                              if eid]
        else:
            # No cached file exists, or we are refreshing.
            # First, we get a count of how many things to retrieve
            url = 'http://api.elsevier.com/content/search/scopus'
            params = {'query': query, 'field': fields, 'count': 0, 'start': 0}
            xml = download(url=url, params=params).text.encode('utf-8')
            results = ET.fromstring(xml)

            N = results.find('opensearch:totalResults', ns)
            try:
                N = int(N.text)
            except:
                N = 0

            if N > max_entries:
                raise Exception(('N = {}. '
                                 'Set max_entries to a higher number or '
                                 'change your query ({})').format(N, query))

            self._EIDS = []
            while N > 0:
                params = {'query': query, 'fields': fields,
                          'count': count, 'start': start}
                resp = download(url=url, params=params, accept="json")
                results = resp.json()

                if 'entry' in results.get('search-results', []):
                    self._EIDS += [str(r['eid']) for
                                   r in results['search-results']['entry']]
                start += count
                N -= count

            with open(qfile, 'wb') as f:
                for eid in self.EIDS:
                    f.write('{}\n'.format(eid).encode('utf-8'))

    def __str__(self):
        s = """{self.query}
        Resulted in {N} hits.
    {entries}"""
        return s.format(self=self,
                        N=len(self.EIDS),
                        entries='\n    '.join(self.EIDS))

    @property
    def org_summary(self):
        """Summary of search results."""
        from scopus.scopus_api import ScopusAbstract
        s = ''
        for i, eid in enumerate(self.EIDS):
            abstract = ScopusAbstract(eid)
            if abstract.aggregationType == 'Journal':
                s += '{0}. {1}\n'.format(i + 1, abstract)
        return s
