import requests
import os
import xml.etree.ElementTree as ET
import textwrap
import time
from operator import itemgetter

from .scopus_api import ScopusAbstract
from .scopus_search import ScopusSearch
from .scopus_affiliation import ScopusAffiliation

from . import ns, get_encoded_text, MY_API_KEY

SCOPUS_AUTHOR_DIR = os.path.expanduser('~/.scopus/author')

if not os.path.exists(SCOPUS_AUTHOR_DIR):
    os.makedirs(SCOPUS_AUTHOR_DIR)


class ScopusAuthor(object):
    '''Class to represent a Scopus Author query by the scopus-id.

    Attributes:
    orcid
    hindex
    ndocuments
    ncitations
    ncited_by
    ncoauthors
    current_affiliation
    affiliation_history
    date_created
    categories - list of scopus categories
    name - Constructed first last name
    scopus_url - Public website to author in Scopus
    citedby_url - api link to who is citing
    coauthor_url - api link to coauthors

    Functions:
    get_coauthors
    get_document_eids
    get_document_summary
    get_abstracts
    '''

    def __init__(self,
                 author_id,
                 refresh=False,
                 level=1):
        '''author_id is the scopus id

        if refresh download new results, otherwise read from cache
        scopus-authors/{author_id} if possible.

        level = number of * to print in __str__.

        '''

        if isinstance(author_id, int):
            author_id = str(author_id)

        self.author_id = author_id
        self.level = level

        qfile = os.path.join(SCOPUS_AUTHOR_DIR, author_id)
        if os.path.exists(qfile) and not refresh:
            with open(qfile) as f:
                self.xml = f.read()
                self.results = ET.fromstring(self.xml)
        else:
            url = ('http://api.elsevier.com/content'
                   '/author/author_id/{0}').format(author_id)
            # No cached file exists, or we are refreshing.
            # First, we get a count of how many things to retrieve
            resp = requests.get(url,
                                headers={'Accept': 'application/xml',
                                         'X-ELS-APIKey': MY_API_KEY},
                                params={'author_id': author_id,
                                        'view': 'ENHANCED'})
            self.xml = resp.text.encode('utf-8')
            results = ET.fromstring(resp.text.encode('utf-8'))

            self.results = results
            with open(qfile, 'w') as f:
                f.write(resp.text)

        self.orcid = get_encoded_text(self.results, 'coredata/orcid')
        hindex = get_encoded_text(self.results,
                                  'h-index')
        self.hindex = int(hindex) if hindex is not None else 0

        ndocuments = get_encoded_text(self.results,
                                      'coredata/document-count')
        self.ndocuments = int(ndocuments) if ndocuments is not None else 0

        ncitations = get_encoded_text(self.results,
                                      'coredata/citation-count')
        self.ncitations = int(ncitations) if ncitations is not None else 0

        ncited_by = get_encoded_text(self.results,
                                     'coredata/cited-by-count')
        self.ncited_by = int(ncited_by) if ncited_by is not None else 0

        ncoauthors = get_encoded_text(self.results,
                                      'coauthor-count')
        self.ncoauthors = int(ncoauthors) if ncoauthors is not None else 0

        self.current_affiliation = get_encoded_text(self.results,
                                                    'author-profile/'
                                                    'affiliation-current/'
                                                    'affiliation/'
                                                    'ip-doc/'
                                                    'afdispname')

        # affiliation history
        affiliations = [ScopusAffiliation(aff_id, refresh=refresh)
                        for aff_id
                        in
                        [el.attrib.get('id')
                         for el in
                         self.results.findall('affiliation-history/'
                                              'affiliation')
                         if el is not None]]
        self.affiliation_history = affiliations

        date_created = self.results.find('author-profile/'
                                         'date-created', ns)
        if date_created is not None:
            self.date_created = (int(date_created.attrib['year']),
                                 int(date_created.attrib['month']),
                                 int(date_created.attrib['day']))
        else:
            self.date_created = (None, None, None)
        # Research areas
        area_elements = self.results.findall('subject-areas/subject-area')
        # {code: name}
        d = {int(ae.attrib['code']): ae.text for ae in area_elements}

        classifications = self.results.findall('author-profile/'
                                               'classificationgroup/'
                                               'classifications/'
                                               'classification')
        # {code: frequency}
        c = {int(cls.text): int(cls.attrib['frequency'])
             for cls in classifications}

        categories = [(d[code], c[code]) for code in d]
        categories.sort(reverse=True, key=itemgetter(1))
        self.categories = categories

        self.name = ((get_encoded_text(self.results,
                                       'author-profile/'
                                       'preferred-name/'
                                       'given-name') or '') +
                     ' ' +
                     (get_encoded_text(self.results,
                                       'author-profile/'
                                       'preferred-name/'
                                       'surname') or ''))

        # Real website for the author
        self.scopus_url = self.results.find('coredata/' +
                                            'link[@rel="scopus-author"]')
        if self.scopus_url is not None:
            self.scopus_url = self.scopus_url.get('href')

        # API url for who cites them.
        self.citedby_url = self.results.find('coredata/'
                                             'link[@rel="scopus-citedby"]')
        if self.citedby_url is not None:
            self.citedby_url = self.citedby_url.get('href')

        # API url for coauthors
        self.coauthor_url = self.results.find('coredata/'
                                              'link[@rel="coauthor-search"]')
        if self.coauthor_url is not None:
            self.coauthor_url = self.coauthor_url.get('href')

    def get_coauthors(self):
        '''Return list of coauthors, their scopus-id and research areas.'''
        url = self.results.find('coredata/'
                                'link[@rel="coauthor-search"]').get('href')
        resp = requests.get(url,
                            headers={'Accept': 'application/xml',
                                     'X-ELS-APIKey': MY_API_KEY})
        xml = resp.text.encode('utf-8')
        results = ET.fromstring(xml)
        coauthors = []

        N = int(get_encoded_text(results, 'opensearch:totalResults'))
        from collections import namedtuple
        AUTHOR = namedtuple('Author', ['name', 'scopus_id',
                                       'affiliation', 'categories'])

        count = 0
        while count < N:
            resp = requests.get(url,
                                headers={'Accept': 'application/xml',
                                         'X-ELS-APIKey': MY_API_KEY},
                                params={'start': count,
                                        'count': 25})
            xml = resp.text.encode('utf-8')
            results = ET.fromstring(xml)

            for entry in results.findall('atom:entry', ns):

                given_name = get_encoded_text(entry,
                                              'atom:preferred-name/'
                                              'atom:given-name')
                surname = get_encoded_text(entry,
                                           'atom:preferred-name/atom:surname')

                coauthor_name = '{0} {1}'.format(given_name, surname)

                scopus_id = get_encoded_text(entry,
                                             'dc:identifier').replace('AUTHOR_ID:',
                                                                      '')

                affiliation = get_encoded_text(entry,
                                               'atom:affiliation-current/'
                                               'atom:affiliation-name')

                # get categories for this author
                s = ', '.join(['{0} ({1})'.format(subject.text,
                                                  subject.attrib['frequency'])
                               for subject in
                               entry.findall('atom:subject-area', ns)])

                coauthors += [AUTHOR(coauthor_name, scopus_id, affiliation, s)]
            count += 25

        return coauthors

    def get_document_eids(self):
        '''Return list of EIDs for the author.'''
        search = ScopusSearch('au-id({0})'.format(self.author_id))
        return search.EIDS

    def get_abstracts(self):
        '''Return a list of ScopusAbstract objects'''
        return [ScopusAbstract(eid) for eid in self.get_document_eids()]

    def get_document_summary(self, N=None, cite_sort=True):
        '''
        Return a summary string of documents.

        N = maximum number to return. if None, return all documents.
        cite_sort is a boolean to sort results by number of citations,
            in decreasing order.
        '''
        abstracts = [ScopusAbstract(eid) for eid in self.get_document_eids()]

        if cite_sort:
            counts = [(a, int(a.citedby_count)) for a in abstracts]
            counts.sort(reverse=True, key=itemgetter(1))
            abstracts = [a[0] for a in counts]

        if N is None:
            N = len(abstracts)

        s = ['{0} of {1} documents'.format(N, len(abstracts))]

        for i in range(N):
            s += ['{0:2d}. {1}\n'.format(i + 1, str(abstracts[i]))]

        return '\n'.join(s)

    def __str__(self):
        '''Return a summary string.'''
        s = ['*' * self.level + ' ' +
             (get_encoded_text(self.results,
                                'author-profile/preferred-name/given-name') or '') +
             ' ' +
             (get_encoded_text(self.results,
                              'author-profile/preferred-name/surname') or '') +
             ' (updated on ' + time.asctime() + ')']

        url = self.results.find('coredata/'
                                'link[@rel="scopus-author"]')
        if url is not None:
            url = url.get('href',
                          'None')
        else:
            url = ''

        s += ['']

        orcid = get_encoded_text(self.results, 'coredata/orcid')
        if orcid is not None:
            s += ['http://orcid.org/' + orcid]

        s += [str(get_encoded_text(self.results,
                                   'coredata/document-count')) +
              ' documents cited ' +
              str(get_encoded_text(self.results,
                                   'coredata/citation-count')) +
              ' times by ' +
              str(get_encoded_text(self.results,
                                   'coredata/cited-by-count')) +
              ' people (' +
              str(get_encoded_text(self.results,
                                   'coauthor-count')) +
              ' coauthors)']
        s += ['#first author papers {0}'.format(self.n_first_author_papers())]
        s += ['#last author papers {0}'.format(self.n_last_author_papers())]
        s += ['h-index: ' +
              str(get_encoded_text(self.results,
                                   'h-index')) +
              '        AIF(2014) = ' +
              '{0:1.2f}'.format(self.author_impact_factor(2015)[2])]

        s += ['Scopus ID created on {}'.format(self.date_created)]

        # Current Affiliation. Note this is what Scopus thinks is current.
        s += ['\nCurrent affiliation according to Scopus:']
        s += ['  ' +
              (get_encoded_text(self.results,
                                ('author-profile/affiliation-current/'
                                 'affiliation/ip-doc/afdispname')) or '')]

        # subject areas
        s += ['\nSubject areas']

        area_elements = self.results.findall('subject-areas/subject-area')
        # {code: name}
        d = {int(ae.attrib['code']): ae.text for ae in area_elements}

        classifications = self.results.findall('author-profile'
                                               '/classificationgroup/'
                                               'classifications/'
                                               'classification')
        # {code: frequency}
        c = {int(cls.text): int(cls.attrib['frequency'])
             for cls in classifications}

        categories = [(d[code], c[code]) for code in d]
        categories.sort(reverse=True, key=itemgetter(1))

        s += [textwrap.fill(', '.join(['{0} ({1})'.format(el[0], el[1])
                                       for el in categories]),
                            initial_indent='  ',
                            subsequent_indent='  ')]

        # journals published in
        temp_s = [el.text
                  for el in
                  self.results.findall('author-profile/journal-history/'
                                       'journal/sourcetitle-abbrev')]
        s += ['\nPublishes in:\n' +
              textwrap.fill(', '.join(temp_s),
                            initial_indent='  ',
                            subsequent_indent='  ')]

        # affiliation history
        s += ['\nAffiliation history:']
        for aff in self.affiliation_history:
            s += [str(aff)]

        # print a bibliography
        s += [self.get_document_summary()]

        return '\n'.join(s)

    def author_impact_factor(self, year=2014):
        '''get author_impact_factor'''
        scopus_abstracts = [ScopusAbstract(eid, refresh=True)
                            for eid in self.get_document_eids()
                            if ScopusAbstract(eid).aggregationType == 'Journal']

        cites = [int(ab.citedby_count) for ab in scopus_abstracts]
        years = [int(ab.coverDate.split('-')[0]) for ab in scopus_abstracts]

        data = zip(years, cites, scopus_abstracts)
        from operator import itemgetter
        data = sorted(data, key=itemgetter(1), reverse=True)

        # now get aif papers for year-1 and year-2
        aif_data = [tup for tup in data if tup[0] in (year - 1, year - 2)]
        Ncites = sum([tup[1] for tup in aif_data])
        if len(aif_data) > 0:
            return (Ncites, len(aif_data), Ncites / float(len(aif_data)))
        else:
            return (Ncites, len(aif_data), 0)

    def n_first_author_papers(self):
        'Return number of papers with author as the first author.'
        scopus_abstracts = [ScopusAbstract(eid)
                            for eid in self.get_document_eids()
                            if ScopusAbstract(eid).aggregationType == 'Journal']
        first_authors = [1 for ab in scopus_abstracts
                         if ab.authors[0].scopusid == self.author_id]

        return sum(first_authors)

    def n_last_author_papers(self):
        'Return number of papers with author as the last author.'
        scopus_abstracts = [ScopusAbstract(eid)
                            for eid in self.get_document_eids()
                            if ScopusAbstract(eid).aggregationType == 'Journal']
        first_authors = [1 for ab in scopus_abstracts
                         if ab.authors[-1].scopusid == self.author_id]
        return sum(first_authors)

    def n_journal_articles(self):
        'Return the number of journal articles.'
        return len([ScopusAbstract(eid)
                    for eid in self.get_document_eids()
                    if ScopusAbstract(eid).aggregationType == 'Journal'])
