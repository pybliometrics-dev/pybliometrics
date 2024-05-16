from collections import namedtuple
from typing import List, NamedTuple, Optional, Tuple, Union

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import chained_get, check_parameter_value,\
    get_id, get_link, parse_date_created, make_int_if_possible, VIEWS


class AffiliationRetrieval(Retrieval):
    @property
    def address(self) -> Optional[str]:
        """The address of the affiliation."""
        return self._json.get('address')

    @property
    def affiliation_name(self) -> str:
        """The name of the affiliation."""
        return self._json.get('affiliation-name')

    @property
    def author_count(self) -> int:
        """Number of authors associated with the affiliation."""
        return make_int_if_possible(chained_get(self._json, ['coredata', 'author-count']))

    @property
    def city(self) -> Optional[str]:
        """The city of the affiliation."""
        return self._json.get('city')

    @property
    def country(self) -> Optional[str]:
        """The country of the affiliation."""
        return self._json.get('country')

    @property
    def date_created(self) -> Optional[Tuple[int, int, int]]:
        """Date the Scopus record was created."""
        try:
            return parse_date_created(self._profile)
        except KeyError:
            return None

    @property
    def document_count(self) -> int:
        """Number of documents for the affiliation."""
        return make_int_if_possible(chained_get(self._json, ['coredata', 'document-count']))
    
    @property
    def document_entitlement_status(self) -> Optional[str]:
        """Returns the document entitlement status, i.e. tells if the requestor 
        is entitled to the requested resource.
        Note: Only works with `ENTITLED` view.
        """
        return chained_get(self._json, ['document-entitlement', 'status'])

    @property
    def eid(self) -> str:
        """The EID of the affiliation."""
        return chained_get(self._json, ['coredata', 'eid'])

    @property
    def identifier(self) -> int:
        """The Scopus ID of the affiliation."""
        return get_id(self._json)

    @property
    def name_variants(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing variants of the `affiliation_name`
        with number of documents referring to this variant.
        """
        variant = namedtuple('Variant', 'name doc_count')
        path = ['name-variants', 'name-variant']
        variants = [variant(name=var['$'], doc_count=int(var['@doc-count']))
                    for var in chained_get(self._json, path, [])]
        return variants or None

    @property
    def org_domain(self) -> Optional[str]:
        """Internet domain of the affiliation.  Requires the STANDARD view."""
        return self._profile.get('org-domain')

    @property
    def org_type(self) -> Optional[str]:
        """Type of the affiliation.  Requires the STANDARD view and only
        present if `profile` is `org profile`.
        """
        return self._profile.get('org-type')

    @property
    def org_URL(self) -> Optional[str]:
        """Website of the affiliation.  Requires the STANDARD view."""
        return self._profile.get('org-URL')

    @property
    def postal_code(self) -> Optional[str]:
        """The postal code of the affiliation.  Requires the STANDARD view."""
        return chained_get(self._profile, ['address', 'postal-code'])

    @property
    def scopus_affiliation_link(self) -> str:
        """Link to the Scopus web view of the affiliation."""
        return get_link(self._json, 2)

    @property
    def self_link(self) -> str:
        """Link to the affiliation's API page."""
        return get_link(self._json, 0)

    @property
    def search_link(self) -> str:
        """URL to the API page listing documents of the affiliation."""
        return get_link(self._json, 1)

    @property
    def state(self) -> Optional[str]:
        """The state (country's administrative sububunit)
        of the affiliation.   Requires the STANDARD view.
        """
        return chained_get(self._profile, ['address', 'state'])

    @property
    def status(self) -> Optional[str]:
        return self._profile.get("status")

    @property
    def sort_name(self) -> Optional[str]:
        """The name of the affiliation used for sorting.  Requires the
        STANDARD view.
        """
        return self._profile.get('sort-name')

    @property
    def url(self) -> str:
        """URL to the affiliation's API page."""
        return chained_get(self._json, ['coredata', 'prism:url'])

    def __init__(self,
                 aff_id: Union[int, str],
                 refresh: Union[bool, int] = False,
                 view: str = "STANDARD",
                 **kwds: str
                 ) -> None:
        """Interaction with the Affiliation Retrieval API.

        :param aff_id: Scopus ID or EID of the affiliation profile.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: The view of the file that should be downloaded.  Allowed
                     values: `LIGHT`, `STANDARD`, `ENTITLED`, where `STANDARD` includes all
                     information of the `LIGHT` view.  For details see
                     https://dev.elsevier.com/sc_affil_retrieval_views.html.
                     Note: Neither the `BASIC` view nor `DOCUMENTS` or `AUTHORS`
                     views are active, although documented. `ENTITLED` only contains the `document_entitlement_status`.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/AffiliationRetrievalAPI.wadl.

        Raises
        ------
        ValueError
            If any of the parameters `refresh` or `view` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{aff_id}`,
        where `path` is specified in your configuration file.
        """
        # Checks
        check_parameter_value(view, VIEWS['AffiliationRetrieval'], "view")

        # Load json
        self._view = view
        self._refresh = refresh
        aff_id = str(int(str(aff_id).split('-')[-1]))
        Retrieval.__init__(self, aff_id, api='AffiliationRetrieval', **kwds)
        if self._view in ('LIGHT', 'STANDARD'):
            self._json = self._json['affiliation-retrieval-response']
        self._profile = self._json.get("institution-profile", {})

    def __str__(self):
        """Return a summary string."""
        date = self.get_cache_file_mdate().split()[0]
        s = f"{self.affiliation_name} in {self.city} in {self.country},\nhas "\
            f"{int(self.author_count):,} associated author(s) and "\
            f"{int(self.document_count):,} associated document(s) as of {date}"
        return s
