import os
from collections import namedtuple
from json import loads

from scopus.utils import download, get_content

AUTHOR_RETRIEVAL_DIR = os.path.expanduser('~/.scopus/author_retrieval')

if not os.path.exists(AUTHOR_RETRIEVAL_DIR):
    os.makedirs(AUTHOR_RETRIEVAL_DIR)


class AuthorRetrieval(object):
    @property
    def affiliation_current(self):
        """The ID of the current affiliation according to Scopus."""
        return self.data['affiliation-current']['@id']

    @property
    def affiliation_history(self):
        """Unordered list of IDs of all affiliations the author was
        affiliated with acccording to Scopus.
        """
        return [d['@id'] for d in
                self.data['affiliation-history']['affiliation']]

    @property
    def citation_count(self):
        """Total number of citing items."""
        return self.data['coredata'].get('citation-count', '0')

    @property
    def cited_by_count(self):
        """Total number of citing authors."""
        return self.data['coredata'].get('cited-by-count', '0')

    @property
    def coauthor_count(self):
        """Total number of coauthors."""
        return self.data.get('coauthor-count', '0')

    @property
    def classificationgroup(self):
        """List with (subject group ID, number of documents)-tuples."""
        clg = self.data['author-profile']['classificationgroup'].get('classifications', {})
        out = []
        for item in clg.get('classification', []):
            out.append((item['$'], item['@frequency']))
        return out
    
    @property
    def coauthor_link(self):
        """URL to Scopus API search page for coauthors."""
        return self.data['coredata'].get('link', [])[3].get('@href')

    @property
    def date_created(self):
        """Date the Scopus record was created."""
        date = self.data['author-profile']['date-created']
        if date is not None:
            return (int(date['@year']), int(date['@month']), int(date['@day']))
        else:
            return (None, None, None)

    @property
    def document_count(self):
        """Number of documents authored (excludes book chapters and notes)."""
        return self.data['coredata'].get('document-count', '0')

    @property
    def eid(self):
        """The EID of the author."""
        return self.data['coredata']['eid']

    @property
    def given_name(self):
        """Author's preferred given name."""
        return self.data['author-profile'].get('preferred-name', {}).get('given-name')

    @property
    def h_index(self):
        """The author's h-index"""
        return self.data.get('h-index', '0')

    @property
    def identifier(self):
        """The author's ID."""
        return self.data['coredata']['dc:identifier'].split(":")[-1]

    @property
    def indexed_name(self):
        """Author's name as indexed by Scopus."""
        return self.data['author-profile'].get('preferred-name', {}).get('indexed-name')

    @property
    def initials(self):
        """Author's preferred initials."""
        return self.data['author-profile'].get('preferred-name', {}).get('initials')

    @property
    def journal_history(self):
        """List of named tuples of authored publications in the form
        (sourcetitle, abbreviation, type, issn).  issn is only given
        for journals.  abbreviation and issn may be None.
        """
        pub_hist = self.data['author-profile']['journal-history'].get('journal', [])
        hist = []
        jour = namedtuple('Journal', 'sourcetitle abbreviation type issn')
        for pub in pub_hist:
            new = jour(sourcetitle=pub['sourcetitle'],
                       abbreviation=pub.get('sourcetitle-abbrev'),
                       type=pub['@type'], issn=pub.get('issn'))
            hist.append(new)
        return hist

    @property
    def orcid(self):
        """The author's ORCID."""
        return self.data['coredata'].get('orcid')

    @property
    def name_variants(self):
        """List of named tuples containing variants of the author name with
        number of documents published with that variant.
        """
        out = []
        fields = 'indexed_name initials surname given_name doc_count'
        variant = namedtuple('Variant', fields)
        for var in self.data['author-profile'].get('name-variant', []):
            new = variant(indexed_name=var['indexed-name'],
                          initials=var['initials'], surname=var['surname'],
                          given_name=var['given-name'],
                          doc_count=var['@doc-count'])
            out.append(new)
        return out

    @property
    def surname(self):
        """Author's preferred surname."""
        return self.data['author-profile'].get('preferred-name', {}).get('surname')

    @property
    def scopus_author_link(self):
        """Link to the Scopus web view of the author."""
        return self.data['coredata'].get('link', [])[1].get('@href')

    @property
    def self_link(self):
        """Link to the author's API page."""
        return self.data['coredata'].get('link', [])[0].get('@href')

    @property
    def search_link(self):
        """URL to the API page listing documents of the author."""
        return self.data['coredata'].get('link', [])[2].get('@href')

    @property
    def publication_range(self):
        """Tuple containing years of first and last publication."""
        r = self.data['author-profile']['publication-range']
        return (r['@start'], r['@end'])

    @property
    def subject_areas(self):
        """List of named tuples of subject areas in the form
        (area, abbreviation, code) of author's publication.
        """
        areas = []
        area = namedtuple('Subjectarea', 'area abbreviation code')
        for item in self.data['subject-areas'].get('subject-area', []):
            new = area(area=item['$'], code=item['@code'],
                       abbreviation=item['@abbrev'])
            areas.append(new)
        return areas

    @property
    def url(self):
        """URL to the author's API page."""
        return self.data['coredata']['prism:url']

    def __init__(self, author_id, refresh=False, refresh_aff=False, level=1):
        """Class to represent a Scopus Author query by the scopus-id.

        Parameters
        ----------
        author_id : str or int
            The ID of the author to search for.  Optionally expressed
            as an Elsevier EID (i.e., in the form 9-s2.0-nnnnnnnn).

        refresh : bool (optional, default=False)
            Whether to refresh the cached file (if it exists) or not.

        refresh_aff : bool (optional, default=False)
            Whether to refresh the cached corresponding affiliation views
            (if they exist) or not.

        level : int (optional, default=1)
            Number of * to print in property __str__.

        Notes
        -----
        The files are cached in ~/.scopus/author/{author_id} (without
        eventually leading '9-s2.0-').
        """
        author_id = str(int(str(author_id).split('-')[-1]))
        self.level = level

        qfile = os.path.join(AUTHOR_RETRIEVAL_DIR, author_id)
        url = ('https://api.elsevier.com/content/author/'
               'author_id/{}').format(author_id)
        params = {'author_id': author_id, 'view': 'ENHANCED'}
        res = get_content(qfile, url=url, refresh=refresh, accept='json',
                          params=params)
        self.data = loads(res.decode('utf-8'))['author-retrieval-response'][0]

    def get_coauthors(self):
        """Retrieves basic information about co-authors as a list of
        namedtuples in the form
        (surname, given_name, scopus_id, affiliation, areas), where
        areas is a list of subject area codes joined by "; ".
        Note: These information will not be cached and are slow for large
        coauthor groups.
        """
        # Get number of authors to search for
        res = download(url=self.coauthor_link, accept='json')
        data = loads(res.text)['search-results']
        N = int(data.get('opensearch:totalResults', 0))
        # Store information in namedtuples
        fields = 'surname given_name id affiliation areas'
        coauth = namedtuple('Coauthor', fields)
        coauthors = []
        # Iterate over search results in chunks of 25 results
        count = 0
        while count < N:
            params = {'start': count, 'count': 25}
            res = download(url=self.coauthor_link, params=params, accept='json')
            data = loads(res.text)['author-retrieval-response']
            # Extract information for each coauthor
            for entry in data:
                surname = entry['author-profile']['preferred-name']['surname']
                given = entry['author-profile']['preferred-name']['given-name']
                scopus_id = entry['coredata']['dc:identifier'].split(':')[-1]
                aff = entry['affiliation-current']['@id']
                areas = [a['@code'] for a in
                         entry['subject-areas']['subject-area']]
                new = coauth(surname=surname, given_name=given, id=scopus_id,
                             affiliation=aff, areas='; '.join(areas))
                coauthors.append(new)
            count += 25
        return coauthors

    def get_document_eids(self, *args, **kwds):
        """Return list of EIDs of author's publications using ScopusSearch."""
        search = ScopusSearch('au-id({})'.format(self.author_id),
                              *args, **kwds)
        return search.EIDS

    def __str__(self):
        """Return a summary string."""
        s = '''{self.indexed_name} from {self.affiliation_current},
    published {self.document_count} documents since {since}
    in {journals} distinct journals
    which were cited by {self.cited_by_count} authors in {self.citation_count} documents
    '''.format(self=self, since=self.publication_range[0],
               journals=len(self.journal_history))
        return s
