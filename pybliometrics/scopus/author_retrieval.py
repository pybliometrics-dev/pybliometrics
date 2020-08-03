from collections import namedtuple
from warnings import warn

from json import loads

from .author_search import AuthorSearch
from .scopus_search import ScopusSearch
from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import chained_get, get_content, get_link,\
    listify, parse_affiliation, parse_date_created


class AuthorRetrieval(Retrieval):
    @property
    def affiliation_current(self):
        """A list of namedtuples representing the authors's current
        affiliation(s), in the form (id parent type relationship afdispname
        preferred_name parent_preferred_name country_code country address_part
        city state postal_code org_domain org_URL).
        Note: Affiliation information might be missing or mal-assigned even
        when it lookes correct in the web view.  In this case please request
        a correction.
        """
        path = ["author-profile", "affiliation-current", "affiliation"]
        return parse_affiliation(chained_get(self._json, path))

    @property
    def affiliation_history(self):
        """A list of namedtuples representing the authors's historical
        affiliation(s), in the form (id parent type relationship afdispname
        preferred_name parent_preferred_name country_code country address_part
        city state postal_code org_domain org_URL).
        Note: Affiliation information might be missing or mal-assigned even
        when it lookes correct in the web view.  In this case please request
        a correction.
        """
        path = ["author-profile", "affiliation-history", "affiliation"]
        return parse_affiliation(chained_get(self._json, path))

    @property
    def citation_count(self):
        """Total number of citing items."""
        return self._json['coredata'].get('citation-count', '0')

    @property
    def cited_by_count(self):
        """Total number of citing authors."""
        return self._json['coredata'].get('cited-by-count', '0')

    @property
    def coauthor_count(self):
        """Total number of coauthors."""
        return self._json.get('coauthor-count', '0')

    @property
    def classificationgroup(self):
        """List with (subject group ID, number of documents)-tuples."""
        path = ['author-profile', 'classificationgroup', 'classifications',
                'classification']
        out = [(item['$'], item['@frequency']) for item in
               listify(chained_get(self._json, path, []))]
        return out or None

    @property
    def coauthor_link(self):
        """URL to Scopus API search page for coauthors."""
        return get_link(self._json, 3)

    @property
    def date_created(self):
        """Date the Scopus record was created."""
        return parse_date_created(self._json['author-profile'])

    @property
    def document_count(self):
        """Number of documents authored (excludes book chapters and notes)."""
        return self._json['coredata'].get('document-count', '0')

    @property
    def eid(self):
        """The EID of the author.  If it differs from the one provided,
        pybliometrics will throw a warning informing the user about
        author profile merges.
        """
        return self._json['coredata']['eid']

    @property
    def given_name(self):
        """Author's preferred given name."""
        path = ['author-profile', 'preferred-name', 'given-name']
        return chained_get(self._json, path)

    @property
    def h_index(self):
        """The author's h-index."""
        return self._json.get('h-index', '0')

    @property
    def historical_identifier(self):
        """Scopus IDs of previous profiles now compromising this profile."""
        hist = chained_get(self._json, ["coredata", 'historical-identifier'], [])
        return [d['$'].split(":")[-1] for d in hist] or None

    @property
    def identifier(self):
        """The author's ID.  Might differ from the one provided."""
        ident = self._json['coredata']['dc:identifier'].split(":")[-1]
        if ident != self._id:
            text = f"Profile with ID {self._id} has been merged and the new "\
                   f"ID is {ident}.  Please update your records manually.  "\
                   "Files have been cached with the old ID."
            warn(text, UserWarning)
        return ident

    @property
    def indexed_name(self):
        """Author's name as indexed by Scopus."""
        path = ['author-profile', 'preferred-name', 'indexed-name']
        return chained_get(self._json, path)

    @property
    def initials(self):
        """Author's preferred initials."""
        path = ['author-profile', 'preferred-name', 'initials']
        return chained_get(self._json, path)

    @property
    def name_variants(self):
        """List of named tuples containing variants of the author name with
        number of documents published with that variant.
        """
        fields = 'indexed_name initials surname given_name doc_count'
        variant = namedtuple('Variant', fields)
        path = ['author-profile', 'name-variant']
        out = [variant(indexed_name=var['indexed-name'], surname=var['surname'],
                       doc_count=var.get('@doc-count'), initials=var['initials'],
                       given_name=var.get('given-name'))
               for var in listify(chained_get(self._json, path, []))]
        return out or None

    @property
    def orcid(self):
        """The author's ORCID."""
        return self._json['coredata'].get('orcid')

    @property
    def publication_range(self):
        """Tuple containing years of first and last publication."""
        r = self._json['author-profile']['publication-range']
        return (r['@start'], r['@end'])
        return self._json['coredata'].get('orcid')

    @property
    def scopus_author_link(self):
        """Link to the Scopus web view of the author."""
        return get_link(self._json, 1)

    @property
    def search_link(self):
        """URL to the API page listing documents of the author."""
        return get_link(self._json, 2)

    @property
    def self_link(self):
        """Link to the author's API page."""
        return get_link(self._json, 0)

    @property
    def status(self):
        """The status of the author profile."""
        return chained_get(self._json, ["author-profile", "status"])

    @property
    def subject_areas(self):
        """List of named tuples of subject areas in the form
        (area, abbreviation, code) of author's publication.
        """
        path = ['subject-areas', 'subject-area']
        area = namedtuple('Subjectarea', 'area abbreviation code')
        areas = [area(area=item['$'], code=item['@code'],
                      abbreviation=item['@abbrev'])
                 for item in chained_get(self._json, path, [])]
        return areas or None

    @property
    def surname(self):
        """Author's preferred surname."""
        path = ['author-profile', 'preferred-name', 'surname']
        return chained_get(self._json, path)

    @property
    def url(self):
        """URL to the author's API page."""
        return self._json['coredata']['prism:url']

    def __init__(self, author_id, refresh=False):
        """Interaction with the Author Retrieval API.

        Parameters
        ----------
        author_id : str or int
            The ID of the author to search for.  Optionally expressed
            as an Elsevier EID (i.e., in the form 9-s2.0-nnnnnnnn).

        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/AuthorRetrieval.html

        Notes
        -----
        The directory for cached results is `{path}/ENHANCED/{author_id}`,
        where `path` is specified in `~/.scopus/config.ini` and `author_id`
        is stripped of an eventually leading `'9-s2.0-'`.
        """
        # Load json
        view = "ENHANCED"  # In case Scopus adds different views in future
        self._id = str(int(str(author_id).split('-')[-1]))
        Retrieval.__init__(self, identifier=self._id, api='AuthorRetrieval',
                           refresh=refresh, view=view)
        self._json = self._json['author-retrieval-response']
        # Checks
        try:
            self._json = self._json[0]
        except KeyError:  # Incomplete forward
            alias_json = listify(self._json['alias']['prism:url'])
            alias = ', '.join([d['$'].split(':')[-1] for d in alias_json])
            text = f'Author profile with ID {author_id} has been merged and '\
                   f'the main profile is now one of {alias}.  Please update '\
                   'your records manually.  Functionality of this object is '\
                   'reduced.'
            warn(text, UserWarning)

    def __str__(self):
        """Return a summary string."""
        date = self.get_cache_file_mdate().split()[0]
        main_aff = self.affiliation_current[0]
        s = f"{self.indexed_name} from {main_aff.preferred_name} in "\
            f"{main_aff.country},\npublished {int(self.document_count):,} "\
            f"document(s) since {self.publication_range[0]} "\
            f"\nwhich were cited by {int(self.cited_by_count):,} author(s) in "\
            f"{int(self.citation_count):,} document(s) as of {date}"
        return s

    def get_coauthors(self):
        """Retrieves basic information about co-authors as a list of
        namedtuples in the form
        (surname, given_name, id, areas, affiliation_id, name, city, country),
        where areas is a list of subject area codes joined by "; ".
        Note: These information will not be cached and are slow for large
        coauthor groups.
        """
        SIZE = 25
        # Get number of authors to search for
        url = self.coauthor_link
        res = get_content(url=url)
        data = loads(res.text)['search-results']
        N = int(data.get('opensearch:totalResults', 0))
        # Store information in namedtuples
        fields = 'surname given_name id areas affiliation_id name city country'
        coauth = namedtuple('Coauthor', fields)
        coauthors = []
        # Iterate over search results in chunks of 25 results
        count = SIZE
        start = 0
        while start < N:
            params = {'start': start, 'count': count}
            res = get_content(url=url, params=params, accept='json')
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
                    id=entry['dc:identifier'].split(':')[-1],
                    areas='; '.join(areas), name=aff.get('affiliation-name'),
                    affiliation_id=aff.get('affiliation-id'),
                    city=aff.get('affiliation-city'),
                    country=aff.get('affiliation-country'))
                coauthors.append(new)
            start += SIZE
        return coauthors or None

    def get_documents(self, subtypes=None, **kwds):
        """Return list of the author's publications using a ScopusSearch()
        query, where publications may fit specified set of document subtypes.

        Parameters
        ----------
        subtypes : list of str (optional, default=None)
            The type of documents that should be returned.

        **kwds : dict-like
            Parameters to be passed on to ScopusSearch().

        Returns
        -------
        results : list of namedtuple
            The same type of results returned from any ScopusSearch().
        """
        s = ScopusSearch(f'AU-ID({self.identifier})', **kwds)
        if subtypes:
            return [p for p in s.results if p.subtype in subtypes]
        else:
            return s.results

    def get_document_eids(self, *args, **kwds):
        """Return list of EIDs of the author's publications using
        a ScopusSearch() query.
        """
        s = ScopusSearch(f'AU-ID({self.identifier})', *args, **kwds)
        return s.get_eids()

    def estimate_uniqueness(self, query=None, *args, **kwds):
        """Estimate how unqiue a profile is by get the number of
        matches of an AuthorSearch for this person.

        Parameters
        ----------
        query : str (optional, default=None)
            The query string to perform to search for authors.  If empty,
            the query is of form "AUTHLAST() AND AUTHFIRST()" with the
            corresponding information included.  Provided queries may include
            "SUBJAREA()" OR "AF-ID() AND SUBJAREA()".  For details see
            https://dev.elsevier.com/tips/AuthorSearchTips.htm.

        args, kwds : key-value pairings
            Parameters to be passed on to AuthorSearch().

        Returns
        -------
        n : int
            The number of matches of the query.
        """
        if not query:
            query = f"AUTHLAST({self.surname}) AND AUTHFIRST({self.given_name})"
        s = AuthorSearch(query, **kwds)
        return s.get_results_size()
