import os
import xml.etree.ElementTree as ET

from scopus.utils import get_content, get_encoded_text

SCOPUS_AFFILIATION_DIR = os.path.expanduser('~/.scopus/affiliation')

if not os.path.exists(SCOPUS_AFFILIATION_DIR):
    os.makedirs(SCOPUS_AFFILIATION_DIR)


class ScopusAffiliation:
    @property
    def affiliation_id(self):
        """The Scopus ID of the affiliation."""
        return self._aff_id

    @property
    def nauthors(self):
        """Number of authors in the affiliation."""
        return self._nauthors

    @property
    def ndocuments(self):
        """Number of documents for the affiliation."""
        return self._ndocuments

    @property
    def url(self):
        """The URL for this affiliation."""
        return self._url

    @property
    def name(self):
        """The name of the affiliation."""
        return self._name

    @property
    def address(self):
        """The address of the affiliation."""
        return self._address

    @property
    def city(self):
        """The city of the affiliation."""
        return self._city

    @property
    def country(self):
        """The country of the affiliation."""
        return self._country

    def __init__(self, aff_id, refresh=False):
        """Class to represent an Affiliation in Scopus.

        Parameters
        ----------
        aff_id : str or int
            The Scopus Affiliation ID.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        Notes
        -----
        The files are cached in ~/.scopus/affiliation/{aff_id}.
        """

        self._affiliation_id = aff_id

        qfile = os.path.join(SCOPUS_AFFILIATION_DIR, str(aff_id))
        url = ('http://api.elsevier.com/content/affiliation/'
               'affiliation_id/{}'.format(aff_id))

        xml = ET.fromstring(get_content(qfile, url=url, refresh=refresh))

        # public url
        self._url = xml.find('coredata/link[@rel="scopus-affiliation"]')
        if self._url is not None:
            self._url = self.url.get('href')
        self.api_url = get_encoded_text(xml, 'coredata/prism:url')
        self._nauthors = get_encoded_text(xml, 'coredata/author-count')
        self._ndocuments = get_encoded_text(xml, 'coredata/document-count')
        self._name = get_encoded_text(xml, 'affiliation-name')
        self._address = get_encoded_text(xml, 'address')
        self._city = get_encoded_text(xml, 'city')
        self._country = get_encoded_text(xml, 'country')

    def __str__(self):
        s = '''{self.name} ({self.nauthors} authors, {self.ndocuments} documents)
    {self.address}
    {self.city}, {self.country}
    {self.url}'''.format(self=self)
        return s
