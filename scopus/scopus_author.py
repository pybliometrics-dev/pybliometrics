import os
import sys
import textwrap
import time
import xml.etree.ElementTree as ET
from collections import Counter, namedtuple
from operator import itemgetter

from .scopus_api import ScopusAbstract
from .scopus_search import ScopusSearch
from .scopus_affiliation import ScopusAffiliation
from scopus.utils import download, get_content, get_encoded_text, ns

SCOPUS_AUTHOR_DIR = os.path.expanduser('~/.scopus/author')

if not os.path.exists(SCOPUS_AUTHOR_DIR):
    os.makedirs(SCOPUS_AUTHOR_DIR)


class ScopusAuthor(object):
    @property
    def author_id(self):
        """The scopus id for the author."""
        return self._author_id

    @property
    def orcid(self):
        """The author's ORCID."""
        return self._orcid

    @property
    def hindex(self):
        """The author hindex"""
        return self._hindex

    @property
    def ndocuments(self):
        """Number of documents authored (excludes book chapters and notes)."""
        return self._ndocuments

    @property
    def ncited_by(self):
        """Total number of citing authors."""
        return self._ncited_by

    @property
    def citation_count(self):
        """Total number of citing items."""
        return self._citation_count

    @property
    def ncoauthors(self):
        """Total number of coauthors."""
        return self._ncoauthors

    @property
    def current_affiliation(self):
        """Current affiliation according to scopus."""
        return self._current_affiliation

    @property
    def affiliation_history(self):
        """List of ScopusAffiliation objects."""
        return self._affiliation_history

    @property
    def date_created(self):
        """Date the Scopus record was created."""
        return self._date_created

    @property
    def firstname(self):
        """Author first name."""
        return self._firstname

    @property
    def lastname(self):
        """Author last name."""
        return self._lastname

    @property
    def name(self):
        """Author name."""
        return self._name

    @property
    def scopus_url(self):
        """URL to the author's profile page."""
        return self._scopus_url

    @property
    def citedby_url(self):
        """URL to Scopus page of citing papers."""
        return self._citedby_url

    @property
    def coauthor_url(self):
        """URL to Scopus coauthor page."""
        return self._coauthor_url

    @property
    def subject_areas(self):
        """List of tuples of author subject areas in the form
        (area, frequency, abbreviation, code), where frequency is the
        number of publications in this subject area.
        """
        freqs = self._subject_freq
        return [(a.text, freqs[int(a.get("code"))], a.get("abbrev"), a.get("code"))
                for a in self._area_elements]

    @property
    def publication_history(self):
        """List of tuples of authored publications in the form
        (title, abbreviation, type, issn), where issn is only given
        for journals.  abbreviation and issn may be None.
        """
        hist = []
        for pub in self._pub_hist:
            try:
                issn = pub.find("issn").text
            except AttributeError:
                issn = None
            try:
                abbr = pub.find("sourcetitle-abbrev").text
            except AttributeError:
                abbr = None
            hist.append((pub.find("sourcetitle").text, abbr, pub.get("type"), issn))
        return hist

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

        qfile = os.path.join(SCOPUS_AUTHOR_DIR, author_id)
        url = ('https://api.elsevier.com/content/author/'
               'author_id/{}').format(author_id)
        params = {'author_id': author_id, 'view': 'ENHANCED'}
        xml = ET.fromstring(get_content(qfile, url=url, refresh=refresh,
                                        params=params))
        self.xml = xml
        self._orcid = get_encoded_text(xml, 'coredata/orcid')
        hindex = get_encoded_text(xml, 'h-index')
        self._hindex = int(hindex) if hindex is not None else 0

        ndocuments = get_encoded_text(xml, 'coredata/document-count')
        self._ndocuments = int(ndocuments) if ndocuments is not None else 0

        _author_id = get_encoded_text(xml, 'coredata/dc:identifier')
        self._author_id = _author_id.split(":")[-1]

        citation_count = get_encoded_text(xml, 'coredata/citation-count')
        self._citation_count = int(citation_count) if citation_count is not None else 0

        ncited_by = get_encoded_text(xml, 'coredata/cited-by-count')
        self._ncited_by = int(ncited_by) if ncited_by is not None else 0

        ncoauthors = get_encoded_text(xml, 'coauthor-count')
        self._ncoauthors = int(ncoauthors) if ncoauthors is not None else 0

        self._current_affiliation = get_encoded_text(xml,
            'author-profile/affiliation-current/affiliation/ip-doc/afdispname')

        # affiliation history (sort out faulty historic affiliations)
        aff_ids = [el.attrib.get('affiliation-id') for el in
                   xml.findall('author-profile/affiliation-history/affiliation')
                   if el is not None and len(list(el.find("ip-doc").iter())) > 1]
        affs = [ScopusAffiliation(aff_id, refresh=refresh_aff) for aff_id in aff_ids]
        self._affiliation_history = affs

        date_created = xml.find('author-profile/date-created', ns)
        if date_created is not None:
            self._date_created = (int(date_created.attrib['year']),
                                  int(date_created.attrib['month']),
                                  int(date_created.attrib['day']))
        else:
            self._date_created = (None, None, None)
        # Research areas
        self._area_elements = xml.findall('subject-areas/subject-area')
        # {code: name}
        d = {int(ae.attrib['code']): ae.text for ae in self._area_elements}

        freqs = xml.findall('author-profile/classificationgroup/'
                            'classifications[@type="ASJC"]/classification')
        # {code: frequency}
        c = {int(cls.text): int(cls.attrib['frequency'])
             for cls in freqs}
        self._subject_freq = c

        categories = [(d[code], c[code]) for code in d]
        categories.sort(reverse=True, key=itemgetter(1))
        self.categories = categories

        self._firstname = (get_encoded_text(xml,
            'author-profile/preferred-name/given-name') or '')

        self._lastname = (get_encoded_text(xml,
           'author-profile/preferred-name/surname') or '')

        self._name = ((get_encoded_text(xml,
                       'author-profile/preferred-name/given-name') or '') +
                      ' ' +
                      (get_encoded_text(xml,
                       'author-profile/preferred-name/surname') or ''))

        # Real website for the author
        self._scopus_url = xml.find('coredata/link[@rel="scopus-author"]')
        if self._scopus_url is not None:
            self._scopus_url = self._scopus_url.get('href')

        # API URL for coauthors
        self._coauthor_url = xml.find('coredata/link[@rel="coauthor-search"]')
        if self._coauthor_url is not None:
            self._coauthor_url = self._coauthor_url.get('href')

        # Publication history
        pub_hist_elements = self.xml.findall('author-profile/journal-history/')
        self._pub_hist = pub_hist_elements

    def get_coauthors(self):
        """Return list of coauthors, their scopus-id and research areas."""
        url = self.xml.find('coredata/link[@rel="coauthor-search"]').get('href')
        xml = download(url=url).text.encode('utf-8')
        xml = ET.fromstring(xml)
        coauthors = []
        N = int(get_encoded_text(xml, 'opensearch:totalResults') or 0)

        AUTHOR = namedtuple('Author',
                            ['name', 'scopus_id', 'affiliation', 'categories'])

        count = 0
        while count < N:
            params = {'start': count, 'count': 25}
            xml = download(url=url, params=params).text.encode('utf-8')
            xml = ET.fromstring(xml)

            for entry in xml.findall('atom:entry', ns):

                given_name = get_encoded_text(entry,
                    'atom:preferred-name/atom:given-name')
                surname = get_encoded_text(entry,
                    'atom:preferred-name/atom:surname')
                coauthor_name = u'{0} {1}'.format(given_name, surname)

                scopus_id = get_encoded_text(entry,
                    'dc:identifier').replace('AUTHOR_ID:', '')

                affiliation = get_encoded_text(entry,
                    'atom:affiliation-current/atom:affiliation-name')

                # get categories for this author
                s = u', '.join(['{0} ({1})'.format(subject.text,
                                                  subject.attrib['frequency'])
                               for subject in
                               entry.findall('atom:subject-area', ns)])

                coauthors += [AUTHOR(coauthor_name, scopus_id, affiliation, s)]
            count += 25

        return coauthors

    def get_document_eids(self, *args, **kwds):
        """Return list of EIDs for the author using ScopusSearch."""
        search = ScopusSearch('au-id({})'.format(self.author_id),
                              *args, **kwds)
        return search.EIDS

    def get_abstracts(self, refresh=True):
        """Return a list of ScopusAbstract objects using ScopusSearch."""
        return [ScopusAbstract(eid, refresh=refresh)
                for eid in self.get_document_eids(refresh=refresh)]

    def get_journal_abstracts(self, refresh=True):
        """Return a list of ScopusAbstract objects using ScopusSearch,
           but only if belonging to a Journal."""
        return [abstract for abstract in self.get_abstracts(refresh=refresh) if
                abstract.aggregationType == 'Journal']

    def get_document_summary(self, N=None, cite_sort=True, refresh=True):
        """Return a summary string of documents.

        Parameters
        ----------
        N : int or None (optional, default=None)
            Maximum number of documents to include in the summary.
            If None, return all documents.

        cite_sort : bool (optional, default=True)
            Whether to sort xml by number of citations, in decreasing order,
            or not.

        refresh : bool (optional, default=True)
            Whether to refresh the cached abstract file (if it exists) or not.

        Returns
        -------
        s : str
            Text summarizing an author's documents.
        """
        abstracts = self.get_abstracts(refresh=refresh)

        if cite_sort:
            counts = [(a, int(a.citedby_count)) for a in abstracts]
            counts.sort(reverse=True, key=itemgetter(1))
            abstracts = [a[0] for a in counts]

        if N is None:
            N = len(abstracts)

        s = [u'{0} of {1} documents'.format(N, len(abstracts))]

        for i in range(N):
            s += ['{0:2d}. {1}\n'.format(i + 1, str(abstracts[i]))]

        return '\n'.join(s)

    def __str__(self):
        """Return a summary string."""
        s = ['{} {} (updated on {})'.format(
             '*' * self.level, self._name, time.asctime())]

        url = self.xml.find('coredata/link[@rel="scopus-author"]')
        if url is not None:
            url = url.get('href', 'None')
        else:
            url = ''

        s += ['']

        orcid = get_encoded_text(self.xml, 'coredata/orcid')
        if orcid is not None:
            s += ['http://orcid.org/' + orcid]

        s += ['{} documents cited {} times by {} people ({} coauthors)'.format(
              self._ndocuments, self._citation_count, self._ncited_by,
              self._ncoauthors)]
        s += ['#first author papers {0}'.format(self.n_first_author_papers())]
        s += ['#last author papers {0}'.format(self.n_last_author_papers())]
        s += ['h-index: {}'.format(self._hindex) +
              '        AIF(2014) = ' +
              '{0:1.2f}'.format(self.author_impact_factor(2015)[2])]

        s += ['Scopus ID created on {}'.format(self.date_created)]

        # Current Affiliation. Note this is what Scopus thinks is current.
        s += ['\nCurrent affiliation according to Scopus:']
        s += ['  ' + (self._current_affiliation or '')]

        # subject areas
        s += ['\nSubject areas']

        s += [textwrap.fill(', '.join(['{0} ({1})'.format(el[0], el[1])
                                       for el in self.categories]),
                            initial_indent='  ',
                            subsequent_indent='  ')]

        # journals published in
        temp_s = [el.find('sourcetitle-abbrev').text for el in self._pub_hist]
        s += ['\nPublishes in:\n' +
              textwrap.fill(', '.join(temp_s), initial_indent='  ',
                            subsequent_indent='  ')]

        # affiliation history
        s += ['\nAffiliation history:']
        for aff in self.affiliation_history:
            s += [str(aff)]

        # print a bibliography
        s += [self.get_document_summary()]

        return '\n'.join(s)

    def author_impact_factor(self, year=2014, refresh=True):
        """Get author_impact_factor for the .

        Parameters
        ----------
        year : int (optional, default=2014)
            The year based for which the impact factor is to be calculated.

        refresh : bool (optional, default=True)
            Whether to refresh the cached search file (if it exists) or not.

        Returns
        -------
        (ncites, npapers, aif) : tuple of integers
            The citations count, publication count, and author impact factor.
        """
        scopus_abstracts = self.get_journal_abstracts(refresh=refresh)

        cites = [int(ab.citedby_count) for ab in scopus_abstracts]
        years = [int(ab.coverDate.split('-')[0]) for ab in scopus_abstracts]

        data = zip(years, cites, scopus_abstracts)
        data = sorted(data, key=itemgetter(1), reverse=True)

        # now get aif papers for year-1 and year-2
        aif_data = [tup for tup in data if tup[0] in (year - 1, year - 2)]
        Ncites = sum([tup[1] for tup in aif_data])
        if len(aif_data) > 0:
            return (Ncites, len(aif_data), Ncites / float(len(aif_data)))
        else:
            return (Ncites, len(aif_data), 0)

    def n_first_author_papers(self, refresh=True):
        """Return number of papers with author as the first author."""
        first_authors = [1 for ab in self.get_journal_abstracts(refresh=refresh)
                         if ab.authors[0].scopusid == self.author_id]
        return sum(first_authors)

    def n_last_author_papers(self, refresh=True):
        """Return number of papers with author as the last author."""
        first_authors = [1 for ab in self.get_journal_abstracts(refresh=refresh)
                         if ab.authors[-1].scopusid == self.author_id]
        return sum(first_authors)

    def n_journal_articles(self, refresh=True):
        """Return the number of journal articles."""
        return len(self.get_journal_abstracts(refresh=refresh))

    def n_yearly_publications(self, refresh=True):
        """Number of journal publications in a given year."""
        pub_years = [int(ab.coverDate.split('-')[0])
                     for ab in self.get_journal_abstracts(refresh=refresh)]
        return Counter(pub_years)
