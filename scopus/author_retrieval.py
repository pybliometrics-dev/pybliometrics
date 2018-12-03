from collections import namedtuple
from warnings import warn

from .scopus_search import ScopusSearch
from scopus.classes import Retrieval


class AuthorRetrieval(Retrieval):
    @property
    def affiliation_current(self):
        """The ID of the current affiliation according to Scopus."""
        return self._json.get('affiliation-current', {}).get('@id')

    @property
    def affiliation_history(self):
        """Unordered list of IDs of all affiliations the author was
        affiliated with acccording to Scopus.
        """
        affs = self._json.get('affiliation-history', {}).get('affiliation')
        try:
            return [d['@id'] for d in affs]
        except TypeError:  # No affiliation history
            return None

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
        clg = self._json['author-profile'].get('classificationgroup', {}).get('classifications', {})
        out = []
        items = clg.get('classification', [])
        if not isinstance(items, list):
            items = [items]
        for item in items:
            out.append((item['$'], item['@frequency']))
        return out

    @property
    def coauthor_link(self):
        """URL to Scopus API search page for coauthors."""
        return self._json['coredata'].get('link', [])[3].get('@href')

    @property
    def date_created(self):
        """Date the Scopus record was created."""
        date = self._json['author-profile']['date-created']
        if date is not None:
            return (int(date['@year']), int(date['@month']), int(date['@day']))
        else:
            return (None, None, None)

    @property
    def document_count(self):
        """Number of documents authored (excludes book chapters and notes)."""
        return self._json['coredata'].get('document-count', '0')

    @property
    def eid(self):
        """The EID of the author.  Might differ from the one provided."""
        return self._json['coredata']['eid']

    @property
    def given_name(self):
        """Author's preferred given name."""
        profile = self._json['author-profile']
        return profile.get('preferred-name', {}).get('given-name')

    @property
    def h_index(self):
        """The author's h-index"""
        return self._json.get('h-index', '0')

    @property
    def identifier(self):
        """The author's ID.  Might differ from the one provided."""
        ident = self._json['coredata']['dc:identifier'].split(":")[-1]
        if ident != self._id:
            text = "Profile with ID {} has been merged and the new ID is "\
                   "{}.  Please update your records manually.  Files have "\
                   "been cached with the old ID.".format(self._id, ident)
            warn(text, UserWarning)
        return ident

    @property
    def indexed_name(self):
        """Author's name as indexed by Scopus."""
        return self._json['author-profile'].get('preferred-name', {}).get('indexed-name')

    @property
    def initials(self):
        """Author's preferred initials."""
        return self._json['author-profile'].get('preferred-name', {}).get('initials')

    @property
    def journal_history(self):
        """List of named tuples of authored publications in the form
        (sourcetitle, abbreviation, type, issn).  issn is only given
        for journals.  abbreviation and issn may be None.
        """
        hist = []
        jour = namedtuple('Journal', 'sourcetitle abbreviation type issn')
        jour_hist = self._json['author-profile'].get('journal-history', {})
        pub_hist = jour_hist.get('journal', [])
        if not isinstance(pub_hist, list):
            pub_hist = [pub_hist]
        for pub in pub_hist:
            new = jour(sourcetitle=pub['sourcetitle'],
                       abbreviation=pub.get('sourcetitle-abbrev'),
                       type=pub['@type'], issn=pub.get('issn'))
            hist.append(new)
        return hist

    @property
    def orcid(self):
        """The author's ORCID."""
        return self._json['coredata'].get('orcid')

    @property
    def name_variants(self):
        """List of named tuples containing variants of the author name with
        number of documents published with that variant.
        """
        out = []
        fields = 'indexed_name initials surname given_name doc_count'
        variant = namedtuple('Variant', fields)
        items = self._json['author-profile'].get('name-variant', [])
        if not isinstance(items, list):
            items = [items]
        for var in items:
            new = variant(indexed_name=var['indexed-name'],
                          initials=var['initials'], surname=var['surname'],
                          given_name=var.get('given-name'),
                          doc_count=var.get('@doc-count'))
            out.append(new)
        return out

    @property
    def surname(self):
        """Author's preferred surname."""
        return self._json['author-profile'].get('preferred-name', {}).get('surname')

    @property
    def scopus_author_link(self):
        """Link to the Scopus web view of the author."""
        return self._json['coredata'].get('link', [])[1].get('@href')

    @property
    def self_link(self):
        """Link to the author's API page."""
        return self._json['coredata'].get('link', [])[0].get('@href')

    @property
    def search_link(self):
        """URL to the API page listing documents of the author."""
        return self._json['coredata'].get('link', [])[2].get('@href')

    @property
    def publication_range(self):
        """Tuple containing years of first and last publication."""
        r = self._json['author-profile']['publication-range']
        return (r['@start'], r['@end'])

    @property
    def subject_areas(self):
        """List of named tuples of subject areas in the form
        (area, abbreviation, code) of author's publication.
        """
        try:
            items = self._json['subject-areas']['subject-area']
        except (KeyError, TypeError):
            return None
        area = namedtuple('Subjectarea', 'area abbreviation code')
        areas = [area(area=item['$'], code=item['@code'],
                      abbreviation=item['@abbrev'])
                 for item in items]
        return areas or None

    @property
    def url(self):
        """URL to the author's API page."""
        return self._json['coredata']['prism:url']

    def __init__(self, author_id, refresh=False):
        """Class to represent a Scopus Author query by the scopus-id.

        Parameters
        ----------
        author_id : str or int
            The ID of the author to search for.  Optionally expressed
            as an Elsevier EID (i.e., in the form 9-s2.0-nnnnnnnn).

        refresh : bool (optional, default=False)
            Whether to refresh the cached file (if it exists) or not.

        Notes
        -----
        The files are cached in ~/.scopus/author_retrieval/{author_id} (without
        eventually leading '9-s2.0-').
        """
        # Load json
        self._id = str(int(str(author_id).split('-')[-1]))
        Retrieval.__init__(self, self._id, 'AuthorRetrieval', refresh)
        self._json = self._json['author-retrieval-response']
        # Checks
        try:
            self._json = self._json[0]
        except KeyError:  # Incomplete forward
            alias_json = self._json['alias']['prism:url']
            if not isinstance(alias_json, list):
                alias_json = [alias_json]
            alias = ', '.join([d['$'].split(':')[-1] for d in alias_json])
            text = 'Author profile with ID {} has been merged and the main '\
                   'profile is now one of {}.  Please update your records '\
                   'manually.  Functionality of this object is '\
                   'reduced.'.format(author_id, alias)
            warn(text, UserWarning)

    def __str__(self):
        """Return a summary string."""
        s = '''{self.indexed_name} from {self.affiliation_current},
    published {self.document_count} documents since {since}
    in {journals} distinct journals
    which were cited by {self.cited_by_count} authors in {self.citation_count} documents
    '''.format(self=self, since=self.publication_range[0],
               journals=len(self.journal_history))
        return s

    def get_coauthors(self):
        """Retrieves basic information about co-authors as a list of
        namedtuples in the form
        (surname, given_name, id, areas, affiliation_id, name, city, country),
        where areas is a list of subject area codes joined by "; ".
        Note: These information will not be cached and are slow for large
        coauthor groups.
        """
        # Get number of authors to search for
        res = download(url=self.coauthor_link, accept='json')
        data = loads(res.text)['search-results']
        N = int(data.get('opensearch:totalResults', 0))
        # Store information in namedtuples
        fields = 'surname given_name id areas affiliation_id name city country'
        coauth = namedtuple('Coauthor', fields)
        coauthors = []
        # Iterate over search results in chunks of 25 results
        count = 0
        while count < N:
            params = {'start': count, 'count': 25}
            res = download(url=self.coauthor_link, params=params, accept='json')
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
                             areas='; '.join(areas),
                             affiliation_id=aff.get('affiliation-id'),
                             name=aff.get('affiliation-name'),
                             city=aff.get('affiliation-city'),
                             country=aff.get('affiliation-country'))
                coauthors.append(new)
            count += 25
        return coauthors

    def get_documents(self, subtypes=None, refresh=False):
        """Return list of author's publications using ScopusSearch, which
        fit a specified set of document subtypes.
        """
        search = ScopusSearch('au-id({})'.format(self.identifier), refresh)
        if subtypes:
            return [p for p in search.results if p.subtype in subtypes]
        else:
            return search.results

    def get_document_eids(self, *args, **kwds):
        """Return list of EIDs of author's publications using ScopusSearch."""
        search = ScopusSearch('au-id({})'.format(self.identifier),
                              *args, **kwds)
        return search.get_eids()
