from collections import namedtuple

from scopus.classes import Retrieval
from scopus.utils import chained_get, get_id, get_link, parse_date_created


class ContentAffiliationRetrieval(Retrieval):
    @property
    def address(self):
        """The address of the affiliation."""
        return self._json.get('address')

    @property
    def affiliation_name(self):
        """The name of the affiliation."""
        return self._json.get('affiliation-name')

    @property
    def author_count(self):
        """Number of authors associated with the affiliation."""
        return self._json['coredata'].get('author-count')

    @property
    def city(self):
        """The city of the affiliation."""
        return self._json.get('city')

    @property
    def country(self):
        """The country of the affiliation."""
        return self._json.get('country')

    @property
    def date_created(self):
        """Date the Scopus record was created."""
        return parse_date_created(self._json['institution-profile'])

    @property
    def document_count(self):
        """Number of documents for the affiliation."""
        return self._json['coredata'].get('document-count')

    @property
    def eid(self):
        """The EID of the affiliation."""
        return self._json['coredata']['eid']

    @property
    def identifier(self):
        """The Scopus ID of the affiliation."""
        return get_id(self._json)

    @property
    def name_variants(self):
        """A list of namedtuples representing variants of the affiliation name
        with number of documents referring to this variant.
        """
        out = []
        variant = namedtuple('Variant', 'name doc_count')
        for var in chained_get(self._json, ['name-variants', 'name-variant'], []):
            new = variant(name=var['$'], doc_count=var.get('@doc-count'))
            out.append(new)
        return out

    @property
    def org_domain(self):
        """Internet domain of the affiliation."""
        return self._json['institution-profile'].get('org-domain')

    @property
    def org_type(self):
        """Type of the affiliation (only present if profile is org profile)."""
        return self._json['institution-profile'].get('org-type')

    @property
    def org_URL(self):
        """Website of the affiliation."""
        return self._json['institution-profile'].get('org-URL')

    @property
    def postal_code(self):
        """The postal code of the affiliation."""
        path = ['institution-profile', 'address', 'postal-code']
        return chained_get(self._json, path)

    @property
    def scopus_affiliation_link(self):
        """Link to the Scopus web view of the affiliation."""
        return get_link(self._json, 2)

    @property
    def self_link(self):
        """Link to the affiliation's API page."""
        return get_link(self._json, 0)

    @property
    def search_link(self):
        """URL to the API page listing documents of the affiliation."""
        return get_link(self._json, 1)

    @property
    def state(self):
        """The state (country's administrative sububunit) of the affiliation."""
        path = ['institution-profile', 'address', 'state']
        return chained_get(self._json, path)

    @property
    def sort_name(self):
        """The name of the affiliation used for sorting."""
        return self._json['institution-profile'].get('sort-name')

    @property
    def url(self):
        """URL to the affiliation's API page."""
        return self._json['coredata'].get('prism:url')

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
        The files are cached in ~/.scopus/affiliation_retrieval/{aff_id}.
        """
        # Load json
        aff_id = str(int(str(aff_id).split('-')[-1]))
        Retrieval.__init__(self, identifier=aff_id,
                           api='ContentAffiliationRetrieval', refresh=refresh)
        self._json = self._json['affiliation-retrieval-response']

    def __str__(self):
        s = '''{self.affiliation_name} ({self.author_count} authors, {self.document_count} documents)
    {self.address}
    {self.city}, {self.country}
    {self.url}'''.format(self=self)
        return s
