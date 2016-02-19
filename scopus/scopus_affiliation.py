import requests
import os
import xml.etree.ElementTree as ET
from . import ns, get_encoded_text, MY_API_KEY

SCOPUS_AFFILIATION_DIR = os.path.expanduser('~/.scopus/affiliation')

if not os.path.exists(SCOPUS_AFFILIATION_DIR):
    os.makedirs(SCOPUS_AFFILIATION_DIR)


class ScopusAffiliation:
    '''
    self.name
    nauthors
    ndocuments
    address
    city
    country
    '''

    def __init__(self, affiliation_id, refresh=False):
        '''affiliation_id is a number like 60030926'''
        self.affiliation_id = affiliation_id
        self.href = ('http://api.elsevier.com/content/affiliation/affiliation_id/' +
                     str(affiliation_id))

        qfile = os.path.join(SCOPUS_AFFILIATION_DIR, str(affiliation_id))
        if os.path.exists(qfile) and not refresh:
            with open(qfile) as f:
                self.xml = f.read()
                self.results = ET.fromstring(self.xml)
        else:
            resp = requests.get(self.href,
                                headers={'Accept': 'application/xml',
                                         'X-ELS-APIKey': MY_API_KEY})
            self.xml = resp.text.encode('utf-8')
            results = ET.fromstring(resp.text.encode('utf-8'))

            self.results = results
            with open(qfile, 'w') as f:
                f.write(resp.text)

        # public url
        self.url = self.results.find('coredata/'
                                     'link[@rel="scopus-affiliation"]')
        if self.url is not None:
            self.url = self.url.get('href')
        self.api_url = get_encoded_text(self.results, 'coredata/prism:url')
        self.nauthors = get_encoded_text(self.results, 'coredata/author-count')
        self.ndocuments = get_encoded_text(self.results,
                                           'coredata/document-count')
        self.name = get_encoded_text(self.results, 'affiliation-name')
        self.address = get_encoded_text(self.results, 'address')
        self.city = get_encoded_text(self.results, 'city')
        self.country = get_encoded_text(self.results, 'country')

    def __str__(self):
        s = '''{self.name}
    {self.address}
    {self.city}, {self.country}
    {self.url}'''.format(self=self)
        return s
