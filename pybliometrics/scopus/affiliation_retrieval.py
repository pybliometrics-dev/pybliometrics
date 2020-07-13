from collections import namedtuple

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import chained_get, get_id, get_link,\
    parse_date_created


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
        path = ['name-variants', 'name-variant']
        return [variant(name=var['$'], doc_count=var.get('@doc-count'))
                for var in chained_get(self._json, path, [])]

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
        """The state (country's administrative sububunit)
        of the affiliation.
        """
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
        """Interaction with the Content Affiliation Retrieval API.

        Parameters
        ----------
        aff_id : str or int
            The Scopus Affiliation ID.  Optionally expressed
            as an Elsevier EID (i.e., in the form 10-s2.0-nnnnnnnn).

        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/ContentAffiliationRetrieval.html.

        Notes
        -----
        The directory for cached results is `{path}/STANDARD/{aff_id}`,
        where `path` is specified in `~/.scopus/config.ini`.
        """
        # Load json
        aff_id = str(int(str(aff_id).split('-')[-1]))
        Retrieval.__init__(self, identifier=aff_id, view="STANDARD",
                           refresh=refresh, api='ContentAffiliationRetrieval')
        self._json = self._json['affiliation-retrieval-response']

    def __str__(self):
        """Return a summary string."""
        date = self.get_cache_file_mdate().split()[0]
        s = f"{self.affiliation_name} in {self.city} in {self.country},\nhas "\
            f"{int(self.author_count):,} connected authors and "\
            f"{int(self.document_count):,} connected documents as of {date}"
        return s
