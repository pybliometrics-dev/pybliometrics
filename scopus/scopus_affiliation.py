import requests
import os
import xml.etree.ElementTree as ET
from . import get_encoded_text, MY_API_KEY

SCOPUS_AFFILIATION_DIR = os.path.expanduser('~/.scopus/affiliation')

if not os.path.exists(SCOPUS_AFFILIATION_DIR):
    os.makedirs(SCOPUS_AFFILIATION_DIR)


class ScopusAffiliation:
    """A class to represent an Affiliation in Scopus."""

    @property
    def affiliation_id(self):
        """The affiliation id."""
        return self._affiliation_id

    @property
    def nauthors(self):
        """Number of authors in the affiliation"""
        return self._nauthors

    @property
    def ndocuments(self):
        """Number of documents for the affiliation."""
        return self._ndocuments

    @property
    def url(self):
        """The URL for this affiliation"""
        return self._url

    @property
    def name(self):
        """The NAME of the affiliation"""
        return self._name

    @property
    def address(self):
        """The address of the affiliation"""
        return self._address

    @property
    def city(self):
        """The city of the affiliation"""
        return self._city

    @property
    def country(self):
        """The country of the affiliation"""
        return self._country

    def __init__(self, affiliation_id, refresh=False):
        """affiliation_id is a number like 60030926, can be an int or string.

        refresh is a boolean. If True, download the Scopus xml again. If False,
        try to use a cached result, and download only if it doesn't exist.
        """

        self._affiliation_id = affiliation_id
        self.href = ('http://api.elsevier.com/content/'
                     'affiliation/affiliation_id/' +
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
        self._url = self.results.find('coredata/'
                                     'link[@rel="scopus-affiliation"]')
        if self._url is not None:
            self._url = self.url.get('href')
        self.api_url = get_encoded_text(self.results, 'coredata/prism:url')
        self._nauthors = get_encoded_text(self.results,
                                          'coredata/author-count')
        self._ndocuments = get_encoded_text(self.results,
                                           'coredata/document-count')
        self._name = get_encoded_text(self.results, 'affiliation-name')
        self._address = get_encoded_text(self.results, 'address')
        self._city = get_encoded_text(self.results, 'city')
        self._country = get_encoded_text(self.results, 'country')

    def __str__(self):
        s = '''{self.name} ({self.nauthors} authors, {self.ndocuments} documents)
    {self.address}
    {self.city}, {self.country}
    {self.url}'''.format(self=self)
        return s
