'''Module to retrieve xml data from the Scopus API.'''

import requests
import os
import xml.etree.ElementTree as ET

from . import MY_API_KEY

ns = {'opensearch': 'http://a9.com/-/spec/opensearch/1.1/'}

SCOPUS_SEARCH_DIR = os.path.expanduser('~/.scopus/search')

if not os.path.exists(SCOPUS_SEARCH_DIR):
    os.makedirs(SCOPUS_SEARCH_DIR)


class ScopusSearch(object):
    '''Class to search a query, and retrieve a list of EIDs as results.'''
    def __init__(self,
                 query,
                 fields='eid',
                 count=200,
                 start=0,
                 refresh=False,
                 max_entries=500):
        '''
        query is a string of the query.
        fields is the list of fields you want returned.

        Results are cached in SCOPUS_SEARCH_DIR/{query}.
        '''

        self.query = query

        qfile = os.path.join(SCOPUS_SEARCH_DIR,
                             # We need to remove / in a DOI here so we can save
                             # it as a file.
                             query.replace('/', '_slash_'))

        if os.path.exists(qfile) and not refresh:
            with open(qfile) as f:
                self.EIDS = [eid for eid in
                             f.read().strip().split('\n')
                             if eid]
        else:
            url = 'http://api.elsevier.com/content/search/scopus'
            # No cached file exists, or we are refreshing.
            # First, we get a count of how many things to retrieve
            resp = requests.get(url,
                                headers={'Accept': 'application/xml',
                                         'X-ELS-APIKey': MY_API_KEY},
                                params={'query': query,
                                        'field': fields,
                                        'count': 0,
                                        'start': 0})
            results = ET.fromstring(resp.text.encode('utf-8'))

            N = results.find('opensearch:totalResults', ns)
            try:
                N = int(N.text)
            except:
                N = 0

            if N > max_entries:
                raise Exception(('N = {}. '
                                 'Set max_entries to a higher number or '
                                 'change your query').format(N))

            self.EIDS = []
            while N > 0:
                resp = requests.get(url,
                                    headers={'Accept': 'application/json',
                                             'X-ELS-APIKey': MY_API_KEY},
                                    params={'query': query,
                                            'fields': fields,
                                            'count': count,
                                            'start': start})

                results = resp.json()

                if 'entry' in results['search-results']:
                    self.EIDS += [str(r['eid']) for
                                  r in results['search-results']['entry']]
                start += count
                N -= count

            with open(qfile, 'w') as f:
                for eid in self.EIDS:
                    f.write('{}\n'.format(eid))

    def __str__(self):
        s = '''{self.query}
        Resulted in {N} hits.
    {entries}'''
        return s.format(self=self,
                        N=len(self.EIDS),
                        entries='\n    '.join(self.EIDS))

    @property
    def org_summary(self):
        from scopus.scopus_api import ScopusAbstract
        s = ''
        for i, eid in enumerate(self.EIDS):
            abstract = ScopusAbstract(eid)
            if abstract.aggregationType == 'Journal':
                s += '{0}. {1}\n'.format(i + 1, abstract)
        return s
