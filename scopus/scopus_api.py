from . import ns, get_encoded_text, MY_API_KEY
import requests
import xml.etree.ElementTree as ET
import os

SCOPUS_XML_DIR = os.path.expanduser('~/.scopus/xml')
SCOPUS_ISSN_DIR = os.path.expanduser('~/.scopus/issn')

if not os.path.exists(SCOPUS_XML_DIR):
    os.makedirs(SCOPUS_XML_DIR)

if not os.path.exists(SCOPUS_ISSN_DIR):
    os.makedirs(SCOPUS_ISSN_DIR)


class ScopusAbstract(object):
    '''Class to represent the results from a Scopus abstract.

    The results are retrieved by the EID from a query. The results
    are cached in a folder ~/.scopus/xml/{eid}.
    '''
    def __init__(self, EID, refresh=False):
        '''EID is the electronic scopus id for an abstract and should be a string.

        refresh is a boolean that determines if the result should be downloaded
        again.
        '''

        fEID = os.path.join(SCOPUS_XML_DIR, EID)
        self.file = fEID

        if os.path.exists(fEID):
            with open(fEID) as f:
                text = f.read()
                self.xml = text
                results = ET.fromstring(text)
        else:
            url = ("http://api.elsevier.com/content/abstract/eid/" +
                   EID + '?view=META_ABS')

            resp = requests.get(url,
                                headers={'Accept': 'application/xml',
                                         'X-ELS-APIKey': MY_API_KEY})
            self.xml = resp.text
            with open(fEID, 'w') as f:
                f.write(self.xml)

            results = ET.fromstring(resp.text.encode('utf-8'))

        coredata = results.find('dtd:coredata', ns)
        authors = results.find('dtd:authors', ns)
        self.results = results
        if results.tag == 'service-error':
            raise Exception('\n{0}\n{1}'.format(EID, self.xml))

        self.coredata = coredata
        self.authors_xml = authors
        self.url = get_encoded_text(coredata, 'prism:url')

        self.identifier = get_encoded_text(coredata, 'dc:identifier')
        self.eid = get_encoded_text(coredata, 'dtd:eid')
        self.doi = get_encoded_text(coredata, 'prism:doi')
        self.title = get_encoded_text(coredata, 'dc:title')

        self.aggregationType = get_encoded_text(coredata,
                                                'prism:aggregationType')
        self.publicationName = get_encoded_text(coredata,
                                                'prism:publicationName')
        self.srctype = get_encoded_text(coredata, 'dtd:srctype')
        self.citedby_count = get_encoded_text(coredata, 'dtd:citedby-count')
        self.publisher = get_encoded_text(coredata, 'dc:publisher')
        self.source_id = get_encoded_text(coredata, 'dtd:source-id')
        self.issn = get_encoded_text(coredata, 'prism:issn')
        self.volume = get_encoded_text(coredata, 'prism:volume')
        self.issueIdentifier = get_encoded_text(coredata,
                                                'prism:issueIdentifier')
        self.article_number = get_encoded_text(coredata, 'dtd:article-number')
        self.startingPage = get_encoded_text(coredata, 'prism:startingPage')
        self.endingPage = get_encoded_text(coredata, 'prism:endingPage')
        self.pageRange = get_encoded_text(coredata, 'prism:pageRange')
        self.coverDate = get_encoded_text(coredata, 'prism:coverDate')
        self.creator = get_encoded_text(coredata, 'dc:creator')
        self.description = get_encoded_text(coredata, 'dc:description')

        sl = coredata.find('dtd:link[@rel="scopus"]', ns).get('href', None)
        self_link = coredata.find('dtd:link[@rel="self"]',
                                  ns).get('href', None)
        cite_link = coredata.find('dtd:link[@rel="cited-by"]',
                                  ns)
        if cite_link:
            cite_link = cite_link.get('href', None)
        self.scopus_link = sl
        self.self_link = self_link
        self.cite_link = cite_link

        self.authors = [ScopusAuthor(author) for author in authors]
        self.affiliations = [ScopusAffiliation(aff) for aff
                             in results.findall('dtd:affiliation', ns)]

    @property
    def nauthors(self):
        'Return number of authors listed in the abstract'
        return len(self.authors)

    # def get_corresponding_author_info(self):
    #     '''Try to get corresponding author information.
    #     Returns (scopus-id, name, email).

    #     This may not work anymore. Scopus may be hiding the email address now
    #     from scrapers like this one ;)

    #     <a href="http://www.scopus.com/authid/detail.url?authorId=56273017000&amp;amp;eid=2-s2.0-84927602604" title="Show Author Details">Zhang, Z.-J.</a><a role="presentation" href="#" aria-labelledby="superscript_c"><sup>c</sup></a><img src="http://www.scopus.com/static/images/s.gif" class="" border="0" height="0" width="4" alt="" title=""><a href="/cdn-cgi/l/email-protection#1c66747d727b6674757669725c6f746932797869327f72" OnClick="authorEmailEvent(this,'abstract')" title="Email to this author" class="correspondenceEmail">&nbsp;</a><font>,&nbsp;</font>

    #     '''
    #     resp = requests.get(self.scopus_link)
    #     import re
    #     m = re.search('<a href="http://www.scopus.com/authid/detail.url'
    #                   '\?authorId=([0-9]*)[^"]*"'  # group 1 has scopus id
    #                    # group 2 has author name
    #                   ' title="Show Author Details">([^<]*)'
    #                   '</a>.*'
    #                   # group 3 has email address
    #                   '<a href="mailto:([^"]*)".*class="correspondenceEmail">',
    #                   resp.text.encode('utf-8'))
    #     if m:
    #         return (m.group(1), m.group(2), m.group(3))
    #     else:
    #         return (None, None, None)

    def get_corresponding_author_info(self):
        '''Try to get corresponding author information.
        Returns (scopus-id, name, email).
        '''
        resp = requests.get(self.scopus_link)
        from lxml import html

        parsed_doc = html.fromstring(resp.content)
        for div in parsed_doc.body.xpath('.//div'):
            for a in div.xpath('a'):
                if '/cdn-cgi/l/email-protection' in a.get('href', ''):
                    encoded_text = a.attrib['href'].replace('/cdn-cgi/l/email-protection#', '')
                    key = int(encoded_text[0:2], 16)
                    email = ''.join([chr(int('0x{}'.format(x), 16) ^ key)
                                     for x in
                                     map(''.join, zip(*[iter(encoded_text[2:])]*2))])
                    for aa in div.xpath('a'):
                        if 'http://www.scopus.com/authid/detail.url' in aa.get('href', ''):
                            scopus_url = aa.attrib['href']
                            name = aa.text

                        return (scopus_url, name, email)

    def __str__(self):
        '''return pretty text version of the abstract.
        Assumes the abstract is a journal article.'''

        if len(self.authors) > 1:
            authors = ', '.join([str(a.initials) +
                                 ' ' +
                                 str(a.surname)
                                 for a in self.authors[0:-1]])
            authors += (' and ' +
                        str(self.authors[-1].initials) +
                        ' ' + str(self.authors[-1].surname))
        else:
            a = self.authors[0]
            authors = str(a.given_name) + ' ' + str(a.surname)

        s = '[[{self.scopus_link}][{self.eid}]]  '
        s += '{authors}, {self.title}, {self.publicationName}, '
        s += '{self.volume}'
        if self.issueIdentifier:
            s += '({self.issueIdentifier}), '
        else:
            s += ', '
        if self.pageRange:
            s += 'p. {self.pageRange}, '
        elif self.startingPage:
            s += 'p. {self.startingPage}, '
        elif self.article_number:
            s += 'Art. No. {self.article_number} '
        else:
            s += '(no pages found) '

        from dateutil.parser import parse
        pubDate = parse(self.coverDate)

        s += '({}).'.format(pubDate.year)
        s += ' http://dx.doi.org/{self.doi},'
        s += ' {self.scopus_link},'
        s += ' cited {self.citedby_count} times (Scopus).\n'
        s += 'Affiliations:\n   '
        s += '\n   '.join([str(aff) for aff in self.affiliations])

        return s.format(authors=authors,
                        self=self)

    @property
    def latex(self):
        s = ('{authors}, \\textit{{{title}}}, {journal}, {volissue}, '
             '{pages}, ({date}). {doi}, {scopus_url}.')
        if len(self.authors) > 1:
            authors = ', '.join([str(a.given_name) +
                                 ' ' + str(a.surname)
                                 for a in self.authors[0:-1]])
            authors += (' and ' +
                        str(self.authors[-1].given_name) +
                        ' ' + str(self.authors[-1].surname))
        else:
            a = self.authors[0]
            authors = str(a.given_name) + ' ' + str(a.surname)
        title = self.title
        journal = self.publicationName
        volume = self.volume
        issue = self.issueIdentifier
        if volume and issue:
            volissue = '\\textbf{{{0}({1})}}'.format(volume, issue)
        elif volume:
            volissue = '\\textbf{{0}}'.format(volume)
        else:
            volissue = 'no volume'
        date = self.coverDate
        if self.pageRange:
            pages = 'p. {0}'.format(self.pageRange)
        elif self.startingPage:
            pages = 'p. {self.startingPage}'.format(self)
        elif self.article_number:
            pages = 'Art. No. {self.article_number}, '.format(self)
        else:
            pages = '(no pages found)'
        doi = '\\href{{http://dx.doi.org/{0}}}{{doi:{1}}}'.format(self.doi,
                                                                  self.doi)
        scopus_url = '\href{{{0}}}{{scopus:{1}}}'.format(self.scopus_link,
                                                         self.eid)

        return s.format(**locals())

    @property
    def html(self):
        'Returns an HTML citation.'
        s = ('{authors}, {title}, {journal}, {volissue}, {pages}, '
             '({date}). {doi}.')

        au_link = ('<a href="http://www.scopus.com/authid/detail.url'
                   '?origin=AuthorProfile&authorId={0}">{1}</a>')

        if len(self.authors) > 1:
            authors = ', '.join([au_link.format(a.auid,
                                                (str(a.given_name) +
                                                 ' ' + str(a.surname)))
                                 for a in self.authors[0:-1]])
            authors += (' and ' +
                        au_link.format(self.authors[-1].auid,
                                       (str(self.authors[-1].given_name) +
                                        ' ' +
                                        str(self.authors[-1].surname))))
        else:
            a = self.authors[0]
            authors = au_link.format(a.auid,
                                     str(a.given_name) + ' ' + str(a.surname))

        title = '<a href="{link}">{title}</a>'.format(link=self.scopus_link,
                                                      title=self.title)

        jname = self.publicationName
        sid = self.source_id
        jlink = ('<a href="http://www.scopus.com/source/sourceInfo.url'
                 '?sourceId={sid}">{journal}</a>')
        journal = jlink.format(sid=sid, journal=jname)

        volume = self.volume
        issue = self.issueIdentifier
        if volume and issue:
            volissue = '<b>{0}({1})</b>'.format(volume, issue)
        elif volume:
            volissue = '<b>{0}</b>'.format(volume)
        else:
            volissue = 'no volume'
        date = self.coverDate
        if self.pageRange:
            pages = 'p. {0}'.format(self.pageRange)
        elif self.startingPage:
            pages = 'p. {self.startingPage}'.format(self=self)
        elif self.article_number:
            pages = 'Art. No. {self.article_number}, '.format(self=self)
        else:
            pages = '(no pages found)'
        doi = '<a href="http://dx.doi.org/{0}">doi:{0}</a>'.format(self.doi,
                                                                   self.doi)

        html = s.format(**locals())
        return html.replace('None', '')

    @property
    def bibtex(self):
        '''Returns a string representing a bibtex entry for the article.
        Only Journal types currently supported. A uuid is used for a key.
        Required fields: author, title, journal, year, volume
        Optional fields: number, pages, month, note, key
        '''
        if self.aggregationType == 'Journal':
            template = '''@article{{{uuid},
  author = {{{author}}},
  title = {{{title}}},
  journal = {{{journal}}},
  year = {{{year}}},
  volume = {{{volume}}},
  number = {{{number}}},
  pages = {{{pages}}},
  doi = {{{doi}}}
}}

'''
        if self.pageRange:
            pages = self.pageRange
        elif self.startingPage:
            pages = self.startingPage
        elif self.article_number:
            pages = self.article_number
        else:
            pages = 'no pages found'
        import uuid
        return template.format(uuid=uuid.uuid1(),
                               author=' and '.join([str(a.given_name) +
                                                    ' ' +
                                                    str(a.surname)
                                                    for a in self.authors]),
                               title=self.title,
                               journal=self.publicationName,
                               year=self.coverDate[0:4],
                               volume=self.volume,
                               number=self.issueIdentifier,
                               pages=pages,
                               doi=self.doi)

    @property
    def ris(self):
        "Return an RIS string representing an entry."
        if self.aggregationType == 'Journal':
            s = '''TY  - JOUR\n'''
            for i, au in enumerate(self.authors):
                s += 'AU  - {0}\n'.format(str(au.indexed_name))
            s += 'TI  - {0}\n'.format(self.title)
            s += 'JO  - {0}\n'.format(self.publicationName)
            s += 'VL  - {0}\n'.format(self.volume)
            if self.issueIdentifier is not None:
                s += 'IS  - {0}\n'.format(self.issueIdentifier)
            s += 'DA  - {0}\n'.format(self.coverDate)
            s += 'SP  - {0}\n'.format(self.pageRange)
            s += 'PY  - {0}\n'.format(self.coverDate[0:4])
            s += 'DO  - {0}\n'.format(self.doi)
            s += 'UR  - http://dx.doi.org/{0}\n'.format(self.doi)
            s += 'ER  - \n\n'

            return s


class ScopusAffiliation(object):
    '''Class to represent the affiliations in an Abstract.'''
    def __init__(self, affiliation):
        '''affiliation should be an xml element from the main abstract'''
        self.affiliation = affiliation
        self.affilname = get_encoded_text(affiliation, 'dtd:affilname')
        self.href = affiliation.attrib.get('href', None)
        self.id = affiliation.attrib.get('id', None)

    def __str__(self):
        return 'id:{0.id} {0.affilname}'.format(self)


class ScopusAuthorAffiliation(object):
    '''Class to represent the affiliation in an Author element'''
    def __init__(self, affiliation):
        '''affiliation should be an xml element from an Author element.'''
        self.affiliation = affiliation
        self.id = affiliation.get('id', None)
        self.href = affiliation.get('href', None)

    def __str__(self):
        return 'affiliation_id:{0.id}'.format(self)


class ScopusAuthor(object):
    '''A class for a author in a ScopusAbstract.'''
    def __init__(self, author):
        '''author should be an xml element.
        The following attributes are supported:

        author
        indexed_name
        given_name
        surname
        initials
        author_url - the scopus api url to get more information
        auid - the scopus id for the author
        scopusid - the scopus id for the author
        seq - the index of the author in the author list.
        affiliations - a list of ScopusAuthorAffiliation objects

        This class is not the same as the one in scopus.scopus_author, which
        uses the scopus author api.

        '''
        self.author = author
        self.indexed_name = get_encoded_text(author, 'ce:indexed-name')
        self.given_name = get_encoded_text(author, 'ce:given-name')
        self.surname = get_encoded_text(author, 'ce:surname')
        self.initials = get_encoded_text(author, 'ce:initials')
        self.author_url = get_encoded_text(author, 'dtd:author-url')
        self.auid = author.attrib.get('auid', None)
        self.scopusid = self.auid
        self.seq = author.attrib.get('seq', None)

        self.affiliations = [ScopusAuthorAffiliation(aff)
                             for aff in author.findall('dtd:affiliation', ns)]

    def __str__(self):
        s = '''{0.seq}. {0.given_name} {0.surname} scopusid:{0.auid} '''
        s += ' '.join([str(aff) for aff in self.affiliations])
        return s.format(self)


class ScopusJournal(object):
    '''Class to represent a journal from the Scopus API.
    '''
    def __init__(self, ISSN, refresh=False):
        ISSN = str(ISSN)
        self.issn = ISSN

        fISSN = os.path.join(SCOPUS_ISSN_DIR, ISSN)
        self.file = fISSN

        if os.path.exists(fISSN) and not refresh:
            self.url = fISSN
            with open(fISSN) as f:
                text = f.read()
                self.xml = text
                results = ET.fromstring(text)
                self.results = results
        else:
            url = ("http://api.elsevier.com/content/serial/title/issn:" +
                   ISSN)
            self.url = url
            resp = requests.get(url,
                                headers={'Accept': 'application/xml',
                                         'X-ELS-APIKey': MY_API_KEY})
            self.xml = resp.text.encode('utf-8')
            with open(fISSN, 'w') as f:
                f.write(resp.text)

            results = ET.fromstring(resp.text.encode('utf-8'))

        self.results = results

        self.publisher = get_encoded_text(self.results, 'entry/dc:publisher')
        self.title = get_encoded_text(self.results, 'entry/dc:title')
        self.aggregationType = get_encoded_text(self.results,
                                                'entry/prism:aggregationType')
        self.prism_url = get_encoded_text(self.results, 'entry/prism:url')

        # Impact factors
        SNIP = get_encoded_text(self.results,
                                'entry/SNIPList/SNIP')
        SNIP_year = self.results.find('entry/SNIPList/SNIP', ns)
        if SNIP_year:
            SNIP_year = SNIP_year.get('year')
        else:
            SNIP_year = -1

        IPP = get_encoded_text(self.results, 'entry/IPPList/IPP')
        IPP_year = self.results.find('entry/IPPList/IPP', ns)
        if IPP_year is not None:
            IPP_year = IPP_year.get('year')
        else:
            IPP_year = -1

        SJR = get_encoded_text(self.results, 'entry/SJRList/SJR')
        SJR_year = self.results.find('entry/SJRList/SJR', ns)
        if SJR_year is not None:
            SJR_year = SJR_year.get('year')
        else:
            SJR_year = -1
        if SNIP:
            self.SNIP = float(SNIP)
            self.SNIP_year = int(SNIP_year)
        else:
            self.SNIP = None
            self.SNIP_year = None

        if IPP:
            self.IPP = float(IPP)
            self.IPP_year = int(IPP_year)
        else:
            self.IPP = None
            self.IPP_year = None

        if SJR:
            self.SJR = float(SJR)
            self.SJR_year = int(SJR_year)
        else:
            self.SJR = None
            self.SJR_year = None

        scopus_url = self.results.find('entry/link[@ref="scopus-source"]')
        if scopus_url is not None:
            self.scopus_url = scopus_url.attrib['href']
        else:
            self.scopus_url = None

        homepage = self.results.find('entry/link[@ref="homepage"]')
        if homepage is not None:
            self.homepage = homepage.attrib['href']
        else:
            self.homepage = None

    def __str__(self):
        s = '''{self.title} {self.scopus_url}
    Homepage: {self.homepage}
    SJR:  {self.SJR} ({self.SJR_year})
    SNIP: {self.SNIP} ({self.SNIP_year})
    IPP:  {self.IPP} ({self.IPP_year})
'''.format(self=self)
        return s

    @property
    def org(self):
        "return org-representation of a Journal"
        s = '''[[{self.scopus_url}][{self.title}]] [[{self.homepage}][homepage]]
| SJR | SNIP | IPP |
| {self.SJR} | {self.SNIP} | {self.IPP} |'''.format(self=self)
        return s
