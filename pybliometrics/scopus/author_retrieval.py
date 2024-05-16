from collections import namedtuple
from warnings import warn
from typing import List, NamedTuple, Optional, Tuple, Union

from json import loads

from .author_search import AuthorSearch
from .scopus_search import ScopusSearch
from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import chained_get, check_parameter_value,\
    filter_digits, get_content, get_link, html_unescape, listify, make_int_if_possible,\
    parse_affiliation, parse_date_created, VIEWS


class AuthorRetrieval(Retrieval):
    @property
    def affiliation_current(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing the authors's current
        affiliation(s), in the form `(id parent type relationship afdispname
        preferred_name parent_preferred_name country_code country address_part
        city state postal_code org_domain org_URL)`.
        Note: Affiliation information might be missing or mal-assigned even
        when it lookes correct in the web view.  In this case please request
        a correction.
        """
        if self._view in ('STANDARD', 'ENHANCED'):
            affs = chained_get(self._profile, ["affiliation-current", "affiliation"])
        elif self._view == 'LIGHT':
            affs = self._json.get('affiliation-current')
        else:
            return None
        return parse_affiliation(affs or {}, self._view)

    @property
    def affiliation_history(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing the authors's historical
        affiliation(s), in the form `(id parent type relationship afdispname
        preferred_name parent_preferred_name country_code country address_part
        city state postal_code org_domain org_URL)`.
        Note: Affiliation information might be missing or mal-assigned even
        when it lookes correct in the web view.  In this case please request
        a correction.

        Note: Unlike on their website, Scopus doesn't provide the periods
        of affiliation.
        """
        affs = chained_get(self._profile, ["affiliation-history", "affiliation"])
        return parse_affiliation(affs or {}, self._view)

    @property
    def alias(self) -> Optional[List[str]]:
        """List of possible new Scopus Author Profile IDs in case the profile
        has been merged.
        """
        return self._alias

    @property
    def citation_count(self) -> int:
        """Total number of citing items."""
        return make_int_if_possible(chained_get(self._json, ['coredata', 'citation-count']))

    @property
    def cited_by_count(self) -> int:
        """Total number of citing authors."""
        return make_int_if_possible(chained_get(self._json, ['coredata', 'cited-by-count']))

    @property
    def classificationgroup(self) -> Optional[List[Tuple[int, int]]]:
        """List with tuples with form`(subject group ID, number of documents)`."""
        path = ['classificationgroup', 'classifications', 'classification']
        out = [(int(filter_digits(item['$'])), int(filter_digits(item['@frequency'])))
               for item in listify(chained_get(self._profile, path, []))]
        return out or None

    @property
    def coauthor_count(self) -> Optional[int]:
        """Total number of coauthors."""
        return make_int_if_possible(chained_get(self._json, ['coauthor-count']))

    @property
    def coauthor_link(self) -> Optional[str]:
        """URL to Scopus API search page for coauthors."""
        return get_link(self._json, 3)

    @property
    def date_created(self) -> Optional[Tuple[int, int, int]]:
        """Date the Scopus record was created."""
        try:
            return parse_date_created(self._profile)
        except KeyError:
            return None

    @property
    def document_count(self) -> int:
        """Number of documents authored (excludes book chapters and notes)."""
        return make_int_if_possible(chained_get(self._json, ['coredata', 'document-count']))
    
    @property
    def document_entitlement_status(self) -> Optional[str]:
        """Returns the document entitlement status, i.e. tells if the requestor 
        is entitled to the requested resource.
        Note: Only works with `ENTITLED` view.
        """
        return chained_get(self._json, ['document-entitlement', 'status'])

    @property
    def eid(self) -> Optional[str]:
        """The EID of the author.  If it differs from the one provided,
        pybliometrics will throw a warning informing the user about
        author profile merges.
        """
        return chained_get(self._json, ['coredata', 'eid'])

    @property
    def given_name(self) -> Optional[str]:
        """Author's preferred given name."""
        return html_unescape(chained_get(self._profile, ['preferred-name', 'given-name']))

    @property
    def h_index(self) -> Optional[str]:
        """The author's h-index."""
        return make_int_if_possible(chained_get(self._json, ['h-index']))

    @property
    def historical_identifier(self) -> Optional[List[int]]:
        """Scopus IDs of previous profiles now compromising this profile."""
        hist = chained_get(self._json, ["coredata", 'historical-identifier'], [])
        return [int(d['$'].split(":")[-1]) for d in hist] or None

    @property
    def identifier(self) -> int:
        """The author's ID.  Might differ from the one provided."""
        ident = chained_get(self._json, ['coredata', 'dc:identifier'])
        if not ident:
            return ident
        ident = ident.split(":")[-1]
        if ident != self._id:
            text = f"Profile with ID {self._id} has been merged and the new "\
                   f"ID is {ident}.  Please update your records manually.  "\
                   "Files have been cached with the old ID."
            warn(text, UserWarning)
        return int(ident)

    @property
    def indexed_name(self) -> Optional[str]:
        """Author's name as indexed by Scopus."""
        if self._view in ('STANDARD', 'ENHANCED'):
            indexed_name = html_unescape(chained_get(self._profile, ['preferred-name', 'indexed-name']))
        elif self._view == 'LIGHT':
            # Try to get indexed name from name-variants
            name_variants = chained_get(self._json, ['name-variants', 'name-variant'])
            if name_variants:
                indexed_name = chained_get(name_variants[0], ['name-variant', 'indexed-name'])
            else:
                # In case of no name-variants get name from preferred-name
                preferred_name = self._json.get('preferred-name')
                indexed_name = ' '.join([preferred_name.get('initials', ''), preferred_name.get('surname', '')])
        else:
            indexed_name = None
        
        return indexed_name

    @property
    def initials(self) -> Optional[str]:
        """Author's preferred initials."""
        return html_unescape(chained_get(self._profile, ['preferred-name', 'initials']))

    @property
    def name_variants(self) -> Optional[List[NamedTuple]]:
        """List of named tuples containing variants of the author name with
        number of documents published with that variant.
        """
        fields = 'indexed_name initials surname given_name doc_count'
        variant = namedtuple('Variant', fields)
        out = [variant(indexed_name=html_unescape(var['indexed-name']), surname=html_unescape(var['surname']),
                       doc_count=make_int_if_possible(var.get('@doc-count')),
                       initials=html_unescape(var['initials']),
                       given_name=html_unescape(var.get('given-name')))
               for var in listify(self._profile.get('name-variant', []))]
        return out or None

    @property
    def orcid(self) -> Optional[str]:
        """The author's ORCID."""
        return chained_get(self._json, ['coredata', 'orcid'])

    @property
    def publication_range(self) -> Optional[Tuple[int, int]]:
        """Tuple containing years of first and last publication."""        
        if self._view in ('STANDARD', 'ENHANCED', 'LIGHT'):
            if self._view in ('STANDARD', 'ENHANCED'):
                r = self._profile.get('publication-range')
                start = '@start'
                end = '@end'
            elif self._view == 'LIGHT':
                r = self._json.get('publication-range')
                start = 'start'
                end = 'end'
            
            try:
                return int(r.get(start)), int(r.get(end))
            except TypeError:
                return None
            
        return None

    @property
    def scopus_author_link(self) -> Optional[str]:
        """Link to the Scopus web view of the author."""
        return get_link(self._json, 1)

    @property
    def search_link(self) -> Optional[str]:
        """URL to the API page listing documents of the author."""
        return get_link(self._json, 2)

    @property
    def self_link(self) -> Optional[str]:
        """Link to the author's API page."""
        return get_link(self._json, 0)

    @property
    def status(self) -> Optional[str]:
        """The status of the author profile."""
        return self._profile.get("status")

    @property
    def subject_areas(self) -> Optional[List[NamedTuple]]:
        """List of named tuples of subject areas in the form
        `(area, abbreviation, code)` of author's publication.
        """
        path = ['subject-areas', 'subject-area']
        area = namedtuple('Subjectarea', 'area abbreviation code')
        areas = [area(area=item['$'], code=int(item['@code']),
                      abbreviation=item['@abbrev'])
                 for item in chained_get(self._json, path, [])]
        return areas or None

    @property
    def surname(self) -> Optional[str]:
        """Author's preferred surname."""
        return html_unescape(chained_get(self._profile, ['preferred-name', 'surname']))

    @property
    def url(self) -> Optional[str]:
        """URL to the author's API page."""
        return chained_get(self._json, ['coredata', 'prism:url'])

    def __init__(self,
                 author_id: Union[int, str],
                 refresh: Union[bool, int] = False,
                 view: str = "ENHANCED",
                 **kwds: str
                 ) -> None:
        """Interaction with the Author Retrieval API.

        :param author_id: The ID or the EID of the author.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: The view of the file that should be downloaded.  Allowed
                     values: `METRICS`, `LIGHT`, `STANDARD`, `ENHANCED`, `ENTITLED`, where `STANDARD`
                     includes all information of `LIGHT` view and `ENHANCED`
                     includes all information of any view.  For details see
                     https://dev.elsevier.com/sc_author_retrieval_views.html.
                     Note: Neither the `BASIC` nor the `DOCUMENTS` view are active,
                     although documented. `ENTITLED` only contains the `document_entitlement_status`.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/AuthorRetrievalAPI.wadl.

        Raises
        ------
        ValueError
            If any of the parameters `refresh` or `view` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/ENHANCED/{author_id}`,
        where `path` is specified in your configuration file, and `author_id`
        is stripped of an eventually leading `'9-s2.0-'`.
        """
        # Checks
        check_parameter_value(view, VIEWS['AuthorRetrieval'], "view")

        # Load json
        self._id = str(author_id).split('-')[-1]
        self._view = view
        self._refresh = refresh
        Retrieval.__init__(self, identifier=self._id,
                           api='AuthorRetrieval', **kwds)

        if self._view in ('METRICS', 'LIGHT', 'STANDARD', 'ENHANCED'):
            # Parse json
            self._json = self._json['author-retrieval-response']
            try:
                self._json = self._json[0]
            except KeyError:  # Incomplete forward
                alias_json = listify(self._json['alias']['prism:url'])
                self._alias = [d['$'].split(':')[-1] for d in alias_json]
                alias_str = ', '.join(self._alias)
                text = f'Author profile with ID {author_id} has been merged and '\
                    f'the main profile is now one of {alias_str}.  Please update '\
                    'your records manually.  Functionality of this object is '\
                    'reduced.'
                warn(text, UserWarning)
            else:
                self._alias = None
        elif self._view == 'ENTITLED':
            self._alias = None
        self._profile = self._json.get("author-profile", {})

    def __str__(self):
        """Return a summary string."""
        if self._view in ('STANDARD', 'ENHANCED', 'LIGHT'):
            date = self.get_cache_file_mdate().split()[0]
            main_aff = self.affiliation_current[0]
            s = f"{self.indexed_name} from {main_aff.preferred_name} in "\
                f"{main_aff.country},\npublished {int(self.document_count):,} "\
                f"document(s) since {self.publication_range[0]} "\
                f"\nwhich were cited by {int(self.cited_by_count):,} author(s) in "\
                f"{int(self.citation_count):,} document(s) as of {date}"
        elif self._view == 'METRICS':
            s = f'Author with ID {self._id}\n'\
                f'published {int(self.document_count):,} document(s)\n'\
                f'which were cited by {int(self.cited_by_count):,} author(s) '\
                f'in {int(self.citation_count):,} document(s)'
        return s

    def get_coauthors(self) -> Optional[List[NamedTuple]]:
        """Retrieves basic information about co-authors as a list of
        namedtuples in the form
        `(surname, given_name, id, areas, affiliation_id, name, city, country)`,
        where areas is a list of subject area codes joined by `"; "`.
        Note: Method retrieves information via individual queries which will
        not be cached.  The Scopus API returns 160 coauthors at most.
        """
        SIZE = 25
        # Get number of authors to search for
        url = self.coauthor_link
        if not url:
            return None
        res = get_content(url, api="AuthorSearch")
        data = loads(res.text)['search-results']
        N = int(data.get('opensearch:totalResults', 0))
        # Store information in namedtuples
        fields = 'surname given_name id areas affiliation_id name city country'
        coauth = namedtuple('Coauthor', fields)
        coauthors = []
        # Iterate over search results in chunks of `SIZE` results
        count = SIZE
        start = 0
        while start < N:
            params = {'start': start, 'count': count, 'accept': 'json'}
            res = get_content(url, api="AuthorSearch", params=params)
            data = loads(res.text)['search-results'].get('entry', [])
            # Extract information for each coauthor
            for entry in data:
                aff = entry.get('affiliation-current', {})
                try:
                    areas = [a['$'] for a in entry.get('subject-area', [])]
                except TypeError:  # Only one subject area given
                    areas = [entry['subject-area']['$']]
                new = coauth(surname=entry['preferred-name']['surname'],
                    given_name=entry['preferred-name'].get('given-name'),
                    id=int(entry['dc:identifier'].split(':')[-1]),
                    areas='; '.join(areas), name=aff.get('affiliation-name'),
                    affiliation_id=aff.get('affiliation-id'),
                    city=aff.get('affiliation-city'),
                    country=aff.get('affiliation-country'))
                coauthors.append(new)
            start += SIZE
        return coauthors or None

    def get_documents(self,
                      subtypes: List[str] = None,
                      *args: str, **kwds: str
                      ) -> Optional[List[NamedTuple]]:
        """Return list of the author's publications using a `ScopusSearch()`
        query, where publications may fit a specified set of document subtypes.

        :param subtypes: The type of documents that should be returned.
        :param args: Parameters to be passed on to `ScopusSearch()`.
        :param kwds: Parameters to be passed on to `ScopusSearch()`.

        Note: To update these results, use `refresh`; the class' `refresh`
        parameter is not used here.
        """
        s = ScopusSearch(f'AU-ID({self.identifier})', **kwds)
        if subtypes:
            return [p for p in s.results if p.subtype in subtypes]
        else:
            return s.results

    def get_document_eids(self,
                          *args: str, **kwds: str
                          ) -> Optional[List[str]]:
        """Return list of EIDs of the author's publications using
        a ScopusSearch() query.

        :param args: Parameters to be passed on to `ScopusSearch()`.
        :param kwds: Parameters to be passed on to `ScopusSearch()`.

        Note: To update these results, use `refresh`; the class' `refresh`
        parameter is not used here.
        """
        s = ScopusSearch(f'AU-ID({self.identifier})', *args, **kwds)
        return s.get_eids()

    def estimate_uniqueness(self,
                            query: str = None,
                            *args: str,
                            **kwds: str
                            ) -> int:
        """Return the number of Scopus author profiles similar to this profile
        via calls with `AuthorSearch()`.

        :param query: The query string to perform to search for authors.  If
                      `None`, the query is of form `"AUTHLAST() AND AUTHFIRST()"`
                      with the corresponding information included.  Provided
                      queries may include `"SUBJAREA()" OR "AF-ID() AND
                      SUBJAREA()"`.  For details see
                      https://dev.elsevier.com/tips/AuthorSearchTips.htm.
        :param args: Parameters to be passed on to `AuthorSearch()`.
        :param kwds: Parameters to be passed on to `AuthorSearch()`.
        """
        if not query:
            query = f"AUTHLAST({self.surname}) AND AUTHFIRST({self.given_name})"
        s = AuthorSearch(query, *args, **kwds)
        return s.get_results_size()
