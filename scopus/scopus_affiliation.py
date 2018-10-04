import os
import xml.etree.ElementTree as ET
import warnings

from scopus import config
from scopus.utils import get_content, get_encoded_text

SCOPUS_AFFILIATION_DIR = os.path.expanduser('~/.scopus/affiliation')

if not os.path.exists(SCOPUS_AFFILIATION_DIR):
    os.makedirs(SCOPUS_AFFILIATION_DIR)


class ScopusAffiliation:
    @property
    def affiliation_id(self):
        """The Scopus ID of the affiliation."""
        return get_encoded_text(self.xml, 'coredata/dc:identifier').split(":")[-1]

    @property
    def date_created(self):
        """Date the Scopus record was created."""
        date_created = self.xml.find('institution-profile/date-created')
        if date_created is not None:
            date_created = (int(date_created.attrib['year']),
                            int(date_created.attrib['month']),
                            int(date_created.attrib['day']))
        else:
            date_created = (None, None, None)
        return date_created

    @property
    def nauthors(self):
        """Number of authors in the affiliation."""
        return get_encoded_text(self.xml, 'coredata/author-count')

    @property
    def ndocuments(self):
        """Number of documents for the affiliation."""
        return get_encoded_text(self.xml, 'coredata/document-count')

    @property
    def url(self):
        """URL to the affiliation's profile page."""
        url = self.xml.find('coredata/link[@rel="scopus-affiliation"]')
        if url is not None:
            url = url.get('href')
        return url

    @property
    def api_url(self):
        """URL to the affiliation's API page."""
        return get_encoded_text(self.xml, 'coredata/prism:url')

    @property
    def org_type(self):
        """Type of the affiliation (only present if profile is org profile)."""
        return get_encoded_text(self.xml, 'institution-profile/org-type')

    @property
    def org_domain(self):
        """Internet domain of the affiliation."""
        return get_encoded_text(self.xml, 'institution-profile/org-domain')

    @property
    def org_url(self):
        """Website of the affiliation."""
        return get_encoded_text(self.xml, 'institution-profile/org-URL')

    @property
    def name(self):
        """The name of the affiliation."""
        return get_encoded_text(self.xml, 'affiliation-name')

    @property
    def address(self):
        """The address of the affiliation."""
        return get_encoded_text(self.xml, 'address')

    @property
    def city(self):
        """The city of the affiliation."""
        return get_encoded_text(self.xml, 'city')

    @property
    def state(self):
        """The state (country's administrative sububunit) of the affiliation."""
        return get_encoded_text(self.xml, 'state')

    @property
    def country(self):
        """The country of the affiliation."""
        return get_encoded_text(self.xml, 'country')

    def __init__(self, aff_id, refresh=False):
        """Class to represent an Affiliation in Scopus.

        Parameters
        ----------
        aff_id : str or int
            The Scopus Affiliation ID.  Optionally expressed
            as an Elsevier EID (i.e., in the form 10-s2.0-nnnnnnnn).

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        Notes
        -----
        The files are cached in ~/.scopus/affiliation/{aff_id}.
        """
        if config.getboolean('Warnings', 'Affiliation'):
            text = config.get('Warnings', 'Text').format('ContentAffiliationRetrieval')
            warnings.warn(text, DeprecationWarning)
            config.set('Warnings', 'Affiliation', '0')
        aff_id = str(int(str(aff_id).split('-')[-1]))

        qfile = os.path.join(SCOPUS_AFFILIATION_DIR, aff_id)
        url = ('https://api.elsevier.com/content/affiliation/'
               'affiliation_id/{}'.format(aff_id))

        self.xml = ET.fromstring(get_content(qfile, url=url, refresh=refresh))

    def __str__(self):
        s = '''{self.name} ({self.nauthors} authors, {self.ndocuments} documents)
    {self.address}
    {self.city}, {self.country}
    {self.url}'''.format(self=self)
        return s
