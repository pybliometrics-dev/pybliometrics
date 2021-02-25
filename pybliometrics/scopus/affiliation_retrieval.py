from collections import namedtuple

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import chained_get, check_parameter_value,\
    get_id, get_link, parse_date_created


class AffiliationRetrieval(Retrieval):
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
        try:
            return parse_date_created(self._profile)
        except KeyError:
            return None

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
        """Internet domain of the affiliation.  Requires the STANDARD view."""
        return self._profile.get('org-domain')

    @property
    def org_type(self):
        """Type of the affiliation.  Requires the STANDARD view and only
        present if profile is org profile.
        """
        return self._profile.get('org-type')

    @property
    def org_URL(self):
        """Website of the affiliation.  Requires the STANDARD view."""
        return self._profile.get('org-URL')

    @property
    def postal_code(self):
        """The postal code of the affiliation.  Requires the STANDARD view."""
        return chained_get(self._profile, ['address', 'postal-code'])

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
        of the affiliation.   Requires the STANDARD view.
        """
        return chained_get(self._profile, ['address', 'state'])

    @property
    def sort_name(self):
        """The name of the affiliation used for sorting.  Requires the
        STANDARD view.
        """
        return self._profile.get('sort-name')

    @property
    def url(self):
        """URL to the affiliation's API page."""
        return self._json['coredata'].get('prism:url')

    def __init__(self, aff_id, refresh=False, view="STANDARD"):
        """Interaction with the Affiliation Retrieval API.

        Parameters
        ----------
        aff_id : str or int
            The Scopus Affiliation ID.  Optionally expressed
            as an Elsevier EID (i.e., in the form 10-s2.0-nnnnnnnn).

        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        view : str (optional, default=STANDARD)
            The view of the file that should be downloaded.  Allowed values:
            LIGHT, STANDARD, where STANDARD includes all information of the
            LIGHT view.  For details see
            https://dev.elsevier.com/sc_affil_retrieval_views.html.
            Note: Neither the BASIC view nor DOCUMENTS or AUTHORS views are
            active, although documented.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/AffiliationRetrieval.html.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{aff_id}`,
        where `path` is specified in `~/.scopus/config.ini`.
        """
        # Checks
        check_parameter_value(view, ('LIGHT', 'STANDARD'), "view")

        # Load json
        aff_id = str(int(str(aff_id).split('-')[-1]))
        Retrieval.__init__(self, identifier=aff_id, view=view,
                           refresh=refresh, api='AffiliationRetrieval')
        self._json = self._json['affiliation-retrieval-response']
        self._profile = self._json.get("institution-profile", {})

    def __str__(self):
        """Return a summary string."""
        date = self.get_cache_file_mdate().split()[0]
        s = f"{self.affiliation_name} in {self.city} in {self.country},\nhas "\
            f"{int(self.author_count):,} associated author(s) and "\
            f"{int(self.document_count):,} associated document(s) as of {date}"
        return s


def ContentAffiliationRetrieval(*args, **kwargs):
    from warnings import warn
    text = "Class ContentAffiliationRetrieval() has been renamed to "\
           "AffiliationRetrieval().  This class will be removed in "\
           "pybliometrics 3.0."
    warn(text, Warning, stacklevel=2)
    return AffiliationRetrieval(*args, **kwargs)
