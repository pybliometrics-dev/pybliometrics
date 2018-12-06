from collections import namedtuple
from warnings import warn

from scopus.classes import Retrieval
from scopus.utils import detect_id_type


class AbstractRetrieval(Retrieval):
    @property
    def abstract(self):
        """The abstract of a document.
        Note: Requires the FULL view of the abstract.
        """
        return self._head.get('abstracts')

    @property
    def affiliation(self):
        """A list of namedtuples representing listed affiliations in
        the form (id, name, city, country).
        Note: Might be empty.
        """
        out = []
        aff = namedtuple('Affiliation', 'id name city country')
        affs = self._json.get('affiliation', [])
        if not isinstance(affs, list):
            affs = [affs]
        for item in affs:
            new = aff(id=item.get('@id'), name=item.get('affilname'),
                      city=item.get('affiliation-city'),
                      country=item.get('affiliation-country'))
            out.append(new)
        return out or None

    @property
    def aggregationType(self):
        """Aggregation type of source the abstract is published in."""
        return self._json['coredata'].get('prism:aggregationType')

    @property
    def authkeywords(self):
        """List of author-provided keywords of the abstract."""
        keywords = self._json['authkeywords']
        if keywords is None:
            return None
        else:
            try:
                return [d['$'] for d in keywords['author-keyword']]
            except TypeError:  # Singleton keyword
                return [keywords['author-keyword']['$']]

    @property
    def authors(self):
        """A list of namedtuples representing the article's authors, in the
        form (auid, indexed_name, surname, given_name, affiliation_id,
        affiliation, city, country).
        Note: Affiliations listed here are often incomplete and sometimes
        use the first author's affiliation for all others.  Rather use
        property author_group.
        """
        out = []
        fields = 'auid indexed_name surname given_name affiliation'
        auth = namedtuple('Author', fields)
        for item in self._json['authors']['author']:
            affs = item.get('affiliation', {})
            if not isinstance(affs, list):
                affs = [affs]
            new = auth(auid=item['@auid'], indexed_name=item['ce:indexed-name'],
                       surname=item['ce:surname'],
                       given_name=item['preferred-name'].get('ce:given-name'),
                       affiliation=[aff.get('@id') for aff in affs])
            out.append(new)
        return out

    @property
    def authorgroup(self):
        """A list of namedtuples representing the article's authors organized
        by affiliation, in the form (affiliation_id, organization, city_group,
        country, auid, indexed_name, surname, given_name).  If no
        "given_name" is given, fall back to initials.
        Note: Requires the FULL view of the abstract.  Affiliation information
        might be missing or mal-assigned even when it lookes correct in
        the web view.  In this case please request a correction.
        """
        out = []
        fields = 'affiliation_id organization city_group country '\
                 'auid indexed_name surname given_name'
        auth = namedtuple('Author', fields)
        items = self._head.get('author-group', [])
        if not isinstance(items, list):
            items = [items]
        for item in items:
            # Affiliation information
            aff = item.get('affiliation', {})
            try:
                org = aff['organization']
                if not isinstance(org, str):
                    try:
                        org = org['$']
                    except TypeError:  # Multiple names given
                        org = ', '.join([d['$'] for d in org if d])
            except KeyError:  # Author group w/o affiliation
                org = None
            # Author information (might relate to collaborations)
            authors = item.get('author', item.get('collaboration', []))
            if not isinstance(authors, list):
                authors = [authors]
            for au in authors:
                try:
                    given = au.get('ce:given-name', au['ce:initials'])
                except KeyError:  # Collaboration
                    given = au.get('ce:text')
                new = auth(affiliation_id=aff.get('@afid'), organization=org,
                           city_group=aff.get('city-group'),
                           country=aff.get('country'), auid=au.get('@auid'),
                           surname=au.get('ce:surname'), given_name=given,
                           indexed_name=au.get('preferred-name', {}).get('ce:indexed-name'))
                out.append(new)
        return out

    @property
    def citedby_count(self):
        """Number of articles citing the abstract."""
        return int(self._json['coredata']['citedby-count'])

    @property
    def citedby_link(self):
        """URL to Scopus page listing citing documents."""
        return self._json['coredata']['link'][2].get('@href')

    @property
    def chemicals(self):
        """List of namedtuples representing chemical entities in the form
        (source, chemical_name, cas_registry_number).  In case multiple
        numbers given, they are joined on ";".
        """
        items = self._head.get('enhancement', {}).get('chemicalgroup', {}).get('chemicals', [])
        if len(items) == 0:
            return None
        if not isinstance(items, list):
            items = [items]
        chemical = namedtuple('Chemical', 'source chemical_name cas_registry_number')
        out = []
        for item in items:
            chems = item['chemical']
            if not isinstance(chems, list):
                chems = [chems]
            for chem in chems:
                number = chem['cas-registry-number']
                try:  # Multiple numbers given
                    num = ";".join([n['$'] for n in number])
                except TypeError:
                    num = number
                new = chemical(source=item['@source'], cas_registry_number=num,
                               chemical_name=chem['chemical-name'])
                out.append(new)
        return out

    @property
    def confcode(self):
        """Code of the conference the abstract belong to.
        Note: Requires the FULL view of the abstract.
        """
        return self._confinfo.get('confevent', {}).get('confcode')

    @property
    def confdate(self):
        """Date range of the conference the abstract belongs to represented
        by two tuples in the form (YYYY, MM, DD).
        Note: Requires the FULL view of the abstract.
        """
        date = self._confinfo.get('confevent', {}).get('confdate', {})
        if len(date) > 0:
            start = (int(date['startdate']['@year']),
                     int(date['startdate']['@month']),
                     int(date['startdate']['@day']))
            end = (int(date['enddate']['@year']),
                   int(date['enddate']['@month']),
                   int(date['enddate']['@day']))
        else:
            start = (None, None, None)
            end = (None, None, None)
        return (start, end)

    @property
    def conflocation(self):
        """Location of the conference the abstract belongs to.
        Note: Requires the FULL view of the abstract.
        """
        return self._confinfo.get('confevent', {}).get('conflocation', {}).get('city-group')

    @property
    def confname(self):
        """Name of the conference the abstract belongs to.
        Note: Requires the FULL view of the abstract.
        """
        return self._confinfo.get('confevent', {}).get('confname')

    @property
    def confsponsor(self):
        """Sponsor(s) of the conference the abstract belongs to.
        Note: Requires the FULL view of the abstract.
        """
        sponsors = self._confinfo.get('confevent', {}).get('confsponsors', {}).get('confsponsor', [])
        if len(sponsors) == 0:
            return None
        if isinstance(sponsors, list):
            return [s['$'] for s in sponsors]
        return sponsors

    @property
    def contributor_group(self):
        """List of namedtuples representing contributors compiled by Scopus,
        in the form (given_name, initials, surname, indexed_name, role).
        """
        items = self._head.get('source', {}).get('contributor-group', [])
        if len(items) == 0:
            return None
        if not isinstance(items, list):
            items = [items]
        out = []
        fields = 'given_name initials surname indexed_name role'
        pers = namedtuple('Contributor', fields)
        for item in items:
            entry = item.get('contributor', {})
            new = pers(indexed_name=entry.get('ce:indexed-name'),
                role=entry.get('@role'), surname=entry.get('ce:surname'),
                given_name=entry.get('ce:given-name'),
                initials=entry.get('ce:initials'))
            out.append(new)
        return out

    @property
    def correspondence(self):
        """namedtuple representing the author to whom correspondence should
        be addressed, in the form
        (surname, initials, organization, country, city_group).
        Note: Requires the FULL view of the abstract.  Might be empty.
        """
        fields = 'surname initials organization country city_group'
        auth = namedtuple('Correspondence', fields)
        corr = self._head.get('correspondence')
        if corr is None:
            return None
        aff = corr.get('affiliation', {})
        try:
            org = aff['organization']
            if isinstance(org, dict):
                try:
                    org = org['$']
                except TypeError:  # Multiple names given
                    org = [d['$'] for d in org]
        except KeyError:
            org = None
        return auth(surname=corr.get('person', {}).get('ce:surname'),
                    initials=corr.get('person', {}).get('ce:initials'),
                    organization=org, country=aff.get('country'),
                    city_group=aff.get('city-group'))

    @property
    def coverDate(self):
        """The date of the cover the abstract is in."""
        return self._json['coredata']['prism:coverDate']

    @property
    def description(self):
        """Return the description of a record.
        Note: If this is empty, try property abstract instead.
        """
        return self._json['coredata'].get('dc:description')

    @property
    def doi(self):
        """DOI of the abstract."""
        return self._json['coredata'].get('prism:doi')

    @property
    def eid(self):
        """EID of the abstract."""
        return self._json['coredata']['eid']

    @property
    def endingPage(self):
        """Ending page."""
        return self._json['coredata'].get('prism:endingPage')

    @property
    def funding(self):
        """List of namedtuples parsed funding information in the form
        (agency string id acronym country).
        """
        funds = self._json['item'].get('xocs:meta', {}).get('xocs:funding-list', {}).get('xocs:funding', [])
        if len(funds) == 0:
            return None
        if not isinstance(funds, list):
            funds = [funds]
        out = []
        fund = namedtuple('Funding', 'agency string id acronym country')
        for item in funds:
            new = fund(agency=item.get('xocs:funding-agency'),
                string=item.get('xocs:funding-agency-matched-string'),
                id=item.get('xocs:funding-agency-id'),
                acronym=item.get('xocs:funding-agency-acronym'),
                country=item.get('xocs:funding-agency-country'))
            out.append(new)
        return out

    @property
    def funding_text(self):
        """The raw text from which Scopus derives funding information."""
        return self._json['item'].get('xocs:meta', {}).get('xocs:funding-list', {}).get('xocs:funding-text')

    @property
    def isbn(self):
        """ISBNs belonging to publicationName as tuple of variying length,
        (e.g. ISBN-10 or ISBN-13)."""
        isbns = self._head.get('source', {}).get('isbn', [])
        if not isinstance(isbns, list):
            isbns = [isbns]
        if len(isbns) == 0:
            return None
        else:
            return tuple((i['$'] for i in isbns))

    @property
    def issn(self):
        """ISSN belonging to the publicationName.
        Note: If E-ISSN is known to Scopus, this returns both
        ISSN and E-ISSN in random order separated by blank space.
        """
        return self._json['coredata'].get('prism:issn')

    @property
    def identifier(self):
        """ID of the abstract (same as EID without "2-s2.0-")."""
        return self._json['coredata']['dc:identifier'].split(':')[-1]

    @property
    def idxterms(self):
        """List of index terms."""
        try:
            terms = self._json.get("idxterms", {}).get('mainterm', [])
        except AttributeError:  # idxterms is empty
            return None
        if not isinstance(terms, list):
            terms = [terms]
        try:
            return [d['$'] for d in terms]
        except AttributeError:
            return None

    @property
    def issueIdentifier(self):
        """Issue number for abstract."""
        return self._json['coredata'].get('prism:issueIdentifier')

    @property
    def issuetitle(self):
        """Title of the issue the abstract is published in.
        Note: Requires the FULL view of the abstract.
        """
        return self._head.get('source', {}).get('issuetitle')

    @property
    def language(self):
        """Language of the article."""
        return self._json['language'].get('@xml:lang')

    @property
    def pageRange(self):
        """Page range."""
        return self._json['coredata'].get('prism:pageRange')

    @property
    def publicationName(self):
        """Name of source the abstract is published in."""
        return self._json['coredata'].get('prism:publicationName')

    @property
    def publisher(self):
        """Name of the publisher of the abstract.
        Note: Information provided in the FULL view of the article might be
        more complete.
        """
        # Return information from FULL view, fall back to other views
        full = self._head.get('source', {}).get('publisher', {}).get('publishername')
        if full is None:
            return self._json['coredata'].get('dc:publisher')
        else:
            return full

    @property
    def publisheraddress(self):
        """Name of the publisher of the abstract.
        Note: Requires the FULL view of the abstract. Might be empty, even
        for journal articles.
        """
        return self._head.get('source', {}).get('publisher', {}).get('publisheraddress')

    @property
    def refcount(self):
        """Number of references of an article.
        Note: Requires the FULL view of the article.
        """
        return self._tail.get('bibliography', {}).get('@refcount')

    @property
    def references(self):
        """List of namedtuples representing references listed in the abstract,
        in the form (position, id, doi, title, authors, sourcetitle,
        publicationyear, volume, issue, first, last, text, fulltext).
        `position` is the number at which the reference appears in the
        document, `id` is the Scopus ID of the referenced abstract (EID
        without the "2-s2.0-"), `authors` is a list of the names of the
        authors in the format "Surname, Initials", `first` and `last` refer
        to the page range, `text` is Scopus-provided information on the
        publication and `fulltext` is the text the authors used for
        the reference.
        Note: Requires the FULL view of the article.  Might be empty even if
        refcount is positive.
        """
        out = []
        fields = 'position id doi title authors sourcetitle publicationyear '\
                 'volume issue first last text fulltext'
        ref = namedtuple('Reference', fields)
        items = self._tail.get('bibliography', {}).get('reference', [])
        if not isinstance(items, list):
            items = [items]
        for item in items:
            info = item['ref-info']
            volisspag = info.get('ref-volisspag', {})
            try:
                auth = info['ref-authors']['author']
                if not isinstance(auth, list):
                    auth = [auth]
                authors = [', '.join([d['ce:surname'], d['ce:initials']])
                           for d in auth]
            except KeyError:  # No authors given
                authors = None
            ids = info['refd-itemidlist']['itemid']
            if not isinstance(ids, list):
                ids = [ids]
            try:
                doi = [d['$'] for d in ids if d['@idtype'] == 'DOI'][0]
            except IndexError:
                doi = None
            new = ref(position=item.get('@id'),
                      id=[d['$'] for d in ids if d['@idtype'] == 'SGR'][0],
                      doi=doi, authors=authors,
                      title=info.get('ref-title', {}).get('ref-titletext'),
                      sourcetitle=info.get('ref-sourcetitle'),
                      publicationyear=info.get('ref-publicationyear', {}).get('@first'),
                      volume=volisspag.get('voliss', {}).get('@volume'),
                      issue=volisspag.get('voliss', {}).get('@issue'),
                      first=volisspag.get('pagerange', {}).get('@first'),
                      last=volisspag.get('pagerange', {}).get('@last'),
                      text=info.get('ref-text'),
                      fulltext=item.get('ref-fulltext'))
            out.append(new)
        return out or None

    @property
    def scopus_link(self):
        """URL to the abstract page on Scopus."""
        return self._json['coredata']['link'][1].get('@href')

    @property
    def self_link(self):
        """URL to Scopus API page of this abstract."""
        return self._json['coredata']['link'][0].get('@href')

    @property
    def sequencebank(self):
        """List of namedtuples representing biological entities defined or
        mentioned in the text, in the form (name, sequence_number, type).
        """
        items = self._head.get('enhancement', {}).get('sequencebanks', {}).get('sequencebank', [])
        if len(items) == 0:
            return None
        if not isinstance(items, list):
            items = [items]
        bank = namedtuple('Sequencebank', 'name sequence_number type')
        out = []
        for item in items:
            numbers = item['sequence-number']
            if not isinstance(numbers, list):
                numbers = [numbers]
            for number in numbers:
                new = bank(name=item['@name'], sequence_number=number['$'],
                           type=number['@type'])
                out.append(new)
        return out

    @property
    def source_id(self):
        """Scopus source ID of the abstract."""
        return self._json['coredata']['source-id']

    @property
    def sourcetitle_abbreviation(self):
        """Abbreviation of the source the abstract is published in.
        Note: Requires the FULL view of the article.
        """
        return self._head.get('source', {}).get('sourcetitle-abbrev')

    @property
    def srctype(self):
        """Aggregation type of source the abstract is published in (short
        version of aggregationType.
        """
        return self._json['coredata'].get('srctype')

    @property
    def startingPage(self):
        """Starting page."""
        return self._json['coredata'].get('prism:startingPage')

    @property
    def subject_areas(self):
        """List of namedtuples containing subject areas of the article
        in the form ().
        Note: Requires the FULL view of the article.
        """
        out = []
        area = namedtuple('Area', 'area abbreviation code')
        try:
            items = self._json.get('subject-areas', {}).get('subject-area', [])
        except AttributeError:  # subject-areas empty
            return None
        if not isinstance(items, list):
            items = [items]
        for item in items:
            new = area(area=item['$'], abbreviation=item['@abbrev'],
                       code=item['@code'])
            out.append(new)
        return out

    @property
    def title(self):
        """Title of the abstract."""
        return self._json['coredata']['dc:title']

    @property
    def url(self):
        """URL to the API view of the abstract."""
        return self._json['coredata']['prism:url']

    @property
    def volume(self):
        """Volume for the abstract."""
        return self._json['coredata'].get('prism:volume')

    @property
    def website(self):
        """Website of publisher."""
        return self._head.get('source', {}).get('website', {}).get('ce:e-address', {}).get('$')

    def __init__(self, identifier=None, view='META_ABS', refresh=False,
                 id_type=None, EID=None):
        """Class to represent the results from a Scopus abstract.

        Parameters
        ----------
        identifier : str or int
            The identifier of an abstract.  Can be the Scoups EID, the Scopus
            ID, the PII, the Pubmed-ID or the DOI.

        EID : str (deprecated since 1.2)
            Deprecated in favor of `identifier`, will be removed in a future
            release.

        id_type: str (optional, default=None)
            The type of used ID. Allowed values: None, 'eid', 'pii',
            'scopus_id', 'pubmed_id', 'doi'.  If the value is None, the
            function tries to infer the ID type itself.

        view : str (optional, default=META_ABS)
            The view of the file that should be downloaded.  Will not take
            effect for already cached files. Allowed values: META, META_ABS,
            FULL, where FULL includes all information of META_ABS view and
            META_ABS includes all information of the META view .  See
            https://dev.elsevier.com/guides/AbstractRetrievalViews.htm
            for details.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        ValueError
            If the id_type parameters contains invalid entries.
            If the view parameters contains invalid entries.

        Notes
        -----
        The files are cached in ~/.scopus/abstract_retrieval/{eid}.

        DOI always contains '/' symbol, which is a path separator in some operating
        systems so '/' has to be replaced in the filename for caching.
        """
        # Checks
        if identifier is None and EID:
            text = "Parameter EID is deprecated in favor of parameter "\
                   "identifier.  Please update your code."
            warn(text, UserWarning)
            identifier = EID
        identifier = str(identifier)
        allowed_views = ('META', 'META_ABS', 'FULL')
        if view not in allowed_views:
            raise ValueError('view parameter must be one of ' +
                             ', '.join(allowed_views))
        if id_type is None:
            id_type = detect_id_type(identifier)
        else:
            allowed_id_types = ('eid', 'pii', 'scopus_id', 'pubmed_id', 'doi')
            if id_type not in allowed_id_types:
                raise ValueError('id_type parameter must be one of ' +
                                 ', '.join(allowed_id_types))
        # Load json
        Retrieval.__init__(self, identifier, 'AbstractRetrieval', refresh,
                           id_type, view)
        self._json = self._json['abstracts-retrieval-response']
        self._head = self._json.get('item', {}).get('bibrecord', {}).get('head', {})
        self._tail = self._json.get('item', {}).get('bibrecord', {}).get('tail', {})
        if self._tail is None:
            self._tail = {}
        self._confinfo = self._head.get('source', {}).get('additional-srcinfo', {}).get('conferenceinfo', {})

    def __str__(self):
        """Return pretty text version of the abstract.

        Assumes the abstract is a journal article and was loaded with
        view="META_ABS" or view="FULL".
        """
        # Authors
        if len(self.authors) > 1:
            authors = ', '.join([a.given_name + ' ' + a.surname
                                 for a in self.authors[0:-1]])
            authors += (' and ' + self.authors[-1].given_name + ' ' +
                        self.authors[-1].surname)
        else:
            a = self.authors[0]
            authors = str(a.given_name) + ' ' + str(a.surname)
        # All other information
        s = '[[{link}][{eid}]]  {auth}, {title}, {jour}, {vol}'.format(
            link=self.scopus_link, eid=self.eid, auth=authors,
            title=self.title, jour=self.publicationName, vol=self.volume)
        if self.issueIdentifier:
            s += '({}), '.format(self.issueIdentifier)
        else:
            s += ', '
        if self.pageRange:
            s += 'pp. {}, '.format(self.pageRange)
        elif self.startingPage:
            s += 'pp. {}-{}, '.format(self.startingPage, self.endingPage)
        else:
            s += '(no pages found) '
        s += '({}).'.format(self.coverDate[:4])
        if self.doi:
            s += ' https://doi.org/{},'.format(self.doi)
        s += ' {}, cited {} times (Scopus).\n  Affiliations:\n   '.format(
            self.scopus_link, self.citedby_count)
        s += '\n   '.join([aff.name for aff in self.affiliation])
        return s

    def get_bibtex(self):
        """Bibliographic entry in BibTeX format.

        Raises
        ------
        ValueError
            If the item's aggregationType is not Journal.
        """
        if self.aggregationType != 'Journal':
            raise ValueError('Only Journal articles supported.')
        # Item key
        year = self.coverDate[0:4]
        first = self.title.split()[0].title()
        last = self.title.split()[-1].title()
        key = ''.join([self.authors[0].surname, year, first, last])
        # Authors
        authors = ' and '.join(["{} {}".format(a.given_name, a.surname)
                                for a in self.authors])
        # Pages
        if self.pageRange:
            pages = self.pageRange
        elif self.startingPage:
            pages = '{}-{}'.format(self.startingPage, self.endingPage)
        else:
            pages = '-'
        # All information
        bib = "@article{{{key},\n  author = {{{auth}}},\n  title = "\
              "{{{{{title}}}}},\n  journal = {{{jour}}},\n  year = "\
              "{{{year}}},\n  volume = {{{vol}}},\n  number = {{{number}}},"\
              "\n  pages = {{{pages}}}".format(
                key=key, auth=authors, title=self.title, year=year,
                jour=self.publicationName, vol=self.volume,
                number=self.issueIdentifier, pages=pages)
        # DOI
        if self.doi:
            bib += ",\n  doi = {{{}}}".format(self.doi)
        bib += "}"
        return bib

    def get_html(self):
        """Bibliographic entry in html format."""
        # Author links
        au_link = ('<a href="https://www.scopus.com/authid/detail.url'
                   '?origin=AuthorProfile&authorId={0}">{1}</a>')
        if len(self.authors) > 1:
            authors = u', '.join([au_link.format(a.auid, a.given_name +
                                                 ' ' + a.surname)
                                 for a in self.authors[0:-1]])
            authors += (u' and ' +
                        au_link.format(self.authors[-1].auid,
                                       (str(self.authors[-1].given_name) +
                                        ' ' +
                                        str(self.authors[-1].surname))))
        else:
            a = self.authors[0]
            authors = au_link.format(a.auid, a.given_name + ' ' + a.surname)
        # Title links
        title = u'<a href="{}">{}</a>'.format(self.scopus_link, self.title)
        # Volume and issue
        if self.volume and self.issueIdentifier:
            volissue = u'<b>{}({})</b>'.format(self.volume, self.issueIdentifier)
        elif self.volume:
            volissue = u'<b>{}</b>'.format(self.volume)
        else:
            volissue = 'no volume'
        # Journal link
        jlink = '<a href="https://www.scopus.com/source/sourceInfo.url'\
                '?sourceId={}">{}</a>'.format(
                    self.source_id, self.publicationName)
        # Pages
        if self.pageRange:
            pages = u'pp. {}'.format(self.pageRange)
        elif self.startingPage:
            pages = u'pp. {}-{}'.format(self.startingPage, self.endingPage)
        else:
            pages = '(no pages found)'
        # All information
        s = "{auth}, {title}, {jour}, {volissue}, {pages}, ({year}).".format(
                auth=authors, title=title, jour=jlink, volissue=volissue,
                pages=pages, year=self.coverDate[:4])
        # DOI
        if self.doi:
            s += ' <a href="https://doi.org/{0}">doi:{0}</a>.'.format(self.doi)
        return s

    def get_latex(self):
        """Bibliographic entry in LaTeX format."""
        if len(self.authors) > 1:
            authors = ', '.join([' '.join([a.given_name, a.surname])
                                 for a in self.authors[0:-1]])
            authors += (' and ' + self.authors[-1].given_name +
                        ' ' + self.authors[-1].surname)
        else:
            a = self.authors
            authors = ' '.join([a.given_name, a.surname])
        if self.volume and self.issueIdentifier:
            volissue = '\\textbf{{{}({})}}'.format(self.volume, self.issueIdentifier)
        elif self.volume:
            volissue = '\\textbf{{{}}}'.format(self.volume)
        else:
            volissue = 'no volume'
        if self.pageRange:
            pages = 'pp. {}'.format(self.pageRange)
        elif self.startingPage:
            pages = 'pp. {}-{}'.format(self.startingPage, self.endingPage)
        else:
            pages = '(no pages found)'
        s = '{auth}, \\textit{{{title}}}, {jour}, {vol}, {pages} ({year}).'.format(
                auth=authors, title=self.title, jour=self.publicationName,
                vol=volissue, pages=pages, year=self.coverDate[:4])
        if self.doi is not None:
            s += ' \\href{{https://doi.org/{0}}}{{doi:{0}}}, '.format(self.doi)
        s += '\\href{{{0}}}{{scopus:{1}}}.'.format(self.scopus_link, self.eid)
        return s

    def get_ris(self):
        """Bibliographic entry in RIS (Research Information System Format)
        format for journal articles.

        Raises
        ------
        ValueError
            If the item's aggregationType is not Journal.
        """
        if self.aggregationType != 'Journal':
            raise ValueError('Only Journal articles supported.')
        # Basic information
        ris = "TY  - JOUR\nTI  - {title}\nJO  - {jour}\nVL  - {vol}\n"\
              "DA  - {date}\nPY  - {year}\nSP  - {pages}\n".format(
                title=self.title, jour=self.publicationName, vol=self.volume,
                date=self.coverDate, year=self.coverDate[0:4],
                pages=self.pageRange)
        # Authors
        for au in self.authors:
            ris += 'AU  - {}\n'.format(au.indexed_name)
        # DOI
        if self.doi is not None:
            ris += 'DO  - {0}\nUR  - https://doi.org/{0}\n'.format(self.doi)
        # Issue
        if self.issueIdentifier is not None:
            ris += 'IS  - {}\n'.format(self.issueIdentifier)
        ris += 'ER  - \n\n'
        return ris
