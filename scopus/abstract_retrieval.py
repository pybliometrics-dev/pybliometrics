from collections import namedtuple
from warnings import warn

from scopus.classes import Retrieval
from scopus.utils import chained_get, get_id, detect_id_type, get_link, listify


class AbstractRetrieval(Retrieval):
    @property
    def abstract(self):
        """The abstract of a document.
        Note: If this is empty, try property description instead.
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
        affs = listify(self._json.get('affiliation', []))
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
    def authorgroup(self):
        """A list of namedtuples representing the article's authors organized
        by affiliation, in the form (affiliation_id, dptid, organization,
        city, postalcode, addresspart, country, auid, indexed_name,
        surname, given_name).
        If "given_name" is not present, fall back to initials.
        Note: Affiliation information might be missing or mal-assigned even
        when it lookes correct in the web view.  In this case please request
        a correction.
        """
        out = []
        fields = 'affiliation_id dptid organization city postalcode '\
                 'addresspart country auid indexed_name surname given_name'
        auth = namedtuple('Author', fields)
        items = listify(self._head.get('author-group', []))
        for item in items:
            # Affiliation information
            aff = item.get('affiliation', {})            
            try:
                aff_ids = listify(aff['affiliation-id'])
                aff_id = ", ".join([a["@afid"] for a in aff_ids])
            except KeyError:
                aff_id = aff.get("@afid")
            org = _get_org(aff)
            # Author information (might relate to collaborations)
            authors = listify(item.get('author', item.get('collaboration', [])))
            for au in authors:
                try:
                    given = au.get('ce:given-name', au['ce:initials'])
                except KeyError:  # Collaboration
                    given = au.get('ce:text')
                new = auth(affiliation_id=aff_id, organization=org,
                           city=aff.get('city'), dptid=aff.get("@dptid"),
                           postalcode=aff.get('postal-code'),
                           addresspart=aff.get('address-part'),
                           country=aff.get('country'), auid=au.get('@auid'),
                           surname=au.get('ce:surname'), given_name=given,
                           indexed_name=chained_get(au, ['preferred-name', 'ce:indexed-name']))
                out.append(new)
        return out or None

    @property
    def authors(self):
        """A list of namedtuples representing the article's authors, in the
        form (auid, indexed_name, surname, given_name, affiliation_id,
        affiliation, city, country).
        Note: The affiliation referred to here is what Scopus' algorithm
        determined as the main affiliation.  Property `authorgroup` provides
        all affiliations.
        """
        out = []
        fields = 'auid indexed_name surname given_name affiliation'
        auth = namedtuple('Author', fields)
        for item in chained_get(self._json, ['authors', 'author'], []):
            affs = [a for a in listify(item.get('affiliation')) if a]
            if affs:
                aff = [aff.get('@id') for aff in affs]
            else:
                aff = None
            new = auth(auid=item['@auid'], surname=item.get('ce:surname'),
                indexed_name=item.get('ce:indexed-name'), affiliation=aff,
                given_name=chained_get(item, ['preferred-name', 'ce:given-name']))
            out.append(new)
        return out or None

    @property
    def citedby_count(self):
        """Number of articles citing the abstract."""
        return int(self._json['coredata']['citedby-count'])

    @property
    def citedby_link(self):
        """URL to Scopus page listing citing documents."""
        return get_link(self._json, 2)

    @property
    def chemicals(self):
        """List of namedtuples representing chemical entities in the form
        (source, chemical_name, cas_registry_number).  In case multiple
        numbers given, they are joined on ";".
        """
        path = ['enhancement', 'chemicalgroup', 'chemicals']
        items = listify(chained_get(self._head, path, []))
        chemical = namedtuple('Chemical', 'source chemical_name cas_registry_number')
        out = []
        for item in items:
            for chem in listify(item['chemical']):
                number = chem.get('cas-registry-number')
                try:  # Multiple numbers given
                    num = ";".join([n['$'] for n in number])
                except TypeError:
                    num = number
                new = chemical(source=item['@source'], cas_registry_number=num,
                               chemical_name=chem['chemical-name'])
                out.append(new)
        return out or None

    @property
    def confcode(self):
        """Code of the conference the abstract belong to."""
        return self._confevent.get('confcode')

    @property
    def confdate(self):
        """Date range of the conference the abstract belongs to represented
        by two tuples in the form (YYYY, MM, DD).
        """
        date = self._confevent.get('confdate', {})
        if len(date) > 0:
            start = {k: int(v) for k, v in date['startdate'].items()}
            end = {k: int(v) for k, v in date['enddate'].items()}
            return ((start['@year'], start['@month'], start['@day']),
                    (end['@year'], end['@month'], end['@day']))
        else:
            return ((None, None, None), (None, None, None))

    @property
    def conflocation(self):
        """Location of the conference the abstract belongs to."""
        return chained_get(self._confevent, ['conflocation', 'city-group'])

    @property
    def confname(self):
        """Name of the conference the abstract belongs to."""
        return self._confevent.get('confname')

    @property
    def confsponsor(self):
        """Sponsor(s) of the conference the abstract belongs to."""
        sponsors = chained_get(self._confevent, ['confsponsors', 'confsponsor'], [])
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
        items = listify(chained_get(self._head, ['source', 'contributor-group'], []))
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
        return out or None

    @property
    def correspondence(self):
        """namedtuple representing the author to whom correspondence should
        be addressed, in the form
        (surname, initials, organization, country, city_group).  Multiple
        organziations are joined on semicolon.
        """
        fields = 'surname initials organization country city_group'
        auth = namedtuple('Correspondence', fields)
        corr = self._head.get('correspondence')
        if corr is None:
            return None
        aff = corr.get('affiliation', {})
        try:
            org = aff['organization']
            try:
                org = org['$']
            except TypeError:  # Multiple names given
                org = "; ".join([d['$'] for d in org])
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
        path = ['item', 'xocs:meta', 'xocs:funding-list', 'xocs:funding']
        funds = listify(chained_get(self._json, path, []))
        out = []
        fund = namedtuple('Funding', 'agency string id acronym country')
        for item in funds:
            new = fund(agency=item.get('xocs:funding-agency'),
                string=item.get('xocs:funding-agency-matched-string'),
                id=item.get('xocs:funding-agency-id'),
                acronym=item.get('xocs:funding-agency-acronym'),
                country=item.get('xocs:funding-agency-country'))
            out.append(new)
        return out or None

    @property
    def funding_text(self):
        """The raw text from which Scopus derives funding information."""
        path = ['item', 'xocs:meta', 'xocs:funding-list', 'xocs:funding-text']
        return chained_get(self._json, path)

    @property
    def isbn(self):
        """ISBNs belonging to publicationName as tuple of variying length,
        (e.g. ISBN-10 or ISBN-13)."""
        isbns = listify(chained_get(self._head, ['source', 'isbn'], []))
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
        return get_id(self._json)

    @property
    def idxterms(self):
        """List of index terms."""
        try:
            terms = listify(self._json.get("idxterms", {}).get('mainterm', []))
        except AttributeError:  # idxterms is empty
            return None
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
        """Title of the issue the abstract is published in."""
        return self._head.get('source', {}).get('issuetitle')

    @property
    def language(self):
        """Language of the article."""
        return chained_get(self._json, ['language', '@xml:lang'])

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
        full = chained_get(self._head, ['source', 'publisher', 'publishername'])
        if full is None:
            return self._json['coredata'].get('dc:publisher')
        else:
            return full

    @property
    def publisheraddress(self):
        """Name of the publisher of the abstract."""
        return chained_get(self._head, ['source', 'publisher', 'publisheraddress'])

    @property
    def refcount(self):
        """Number of references of an article.
        Note: Requires the FULL view of the article.
        """
        path = ['item', 'bibrecord', 'tail', 'bibliography', '@refcount']
        return chained_get(self._json, path)

    @property
    def references(self):
        """List of namedtuples representing references listed in the abstract,
        in the form (position, id, doi, title, authors, authors_auid,
        authors_affiliationid, sourcetitle, publicationyear, volume, issue, first,
        last, citedbycount, text, fulltext).
        `position` is the number at which the reference appears in the
        document, `id` is the Scopus ID of the referenced abstract (EID
        without the "2-s2.0-"), `authors` is a string of the names of the
        authors in the format "Surname1, Initials1; Surname2, Initials2",
        `authors_auid` is a string of the author IDs joined on "; ",
        `authors_affiliationid` is a string of the authors' affiliation IDs
        joined on "; ", `sourcetitle` is the name of the source (e.g. the
        journal), `publicationyear` is the year of the publication as a string,
        `volume` and `issue`, are strings referring to the volume and issue,
        `first` and `last` refer to the page range, `citedbycount` is a string
        for the total number of citations of the cited item, `text` is
        Scopus-provided information on the publication, `fulltext` is the text
        the authors used for the reference.

        Note: Requires either the FULL view or REF view of the article.  Might
        be empty even if refcount is positive.  Specific fields can be empty.
        Author lists (authors, authors_auid, authors_affiliationid) may contain
        duplicates but have been filtered of None's.
        """
        out = []
        fields = 'position id doi title authors authors_auid '\
                 'authors_affiliationid sourcetitle publicationyear volume '\
                 'issue first last citedbycount text fulltext'
        ref = namedtuple('Reference', fields)
        path = ['item', 'bibrecord', 'tail', 'bibliography', 'reference']
        items = listify(chained_get(self._json, path,
                    self._json.get('references', {}).get('reference', [])))
        for item in items:
            info = item.get('ref-info', item)
            volisspag = info.get('volisspag', {}) or {}
            if isinstance(volisspag, list):
                volisspag = volisspag[0]
            # Parse author information
            try:  # FULL view parsing
                auth = listify(item['ref-info']['ref-authors']['author'])
                authors = [', '.join([d['ce:surname'], d['ce:initials']])
                           for d in auth]
                auids = None
                affids = None
            except KeyError:  # REF view parsing
                auth = (info.get('author-list') or {}).get('author', [])
                authors = [', '.join(filter(None, [d.get('ce:surname'),
                                                   d.get('ce:given-name')]))
                           for d in auth]
                auids = "; ".join(filter(None, [d.get('@auid') for d in auth]))
                affs = filter(None, [d.get('affiliation') for d in auth])
                affids = "; ".join([aff.get('@id') for aff in affs])
            # Parse IDs
            try:
                ids = listify(info['refd-itemidlist']['itemid'])
            except KeyError:
                ids = []
            try:
                doi = _select_by_idtype(ids, 'DOI')[0]
            except IndexError:
                doi = info.get('ce:doi')
            try:
                scopus_id = _select_by_idtype(ids, 'SGR')[0]
            except IndexError:
                scopus_id = info.get('scopus-id')
            # Combine information
            new = ref(position=item.get('@id'),
                      id=scopus_id,
                      doi=doi,
                      authors="; ".join(authors),
                      authors_auid=auids or None,
                      authors_affiliationid=affids or None,
                      title=info.get('ref-title', {}).get('ref-titletext', info.get('title')),
                      sourcetitle=info.get('ref-sourcetitle', info.get('sourcetitle')),
                      publicationyear=info.get('ref-publicationyear', {}).get('@first'),
                      volume=volisspag.get('voliss', {}).get('@volume'),
                      issue=volisspag.get('voliss', {}).get('@issue'),
                      first=volisspag.get('pagerange', {}).get('@first'),
                      last=volisspag.get('pagerange', {}).get('@last'),
                      citedbycount=info.get('citedby-count'),
                      text=info.get('ref-text'),
                      fulltext=item.get('ref-fulltext'))
            out.append(new)
        return out or None

    @property
    def scopus_link(self):
        """URL to the abstract page on Scopus."""
        return get_link(self._json, 1)

    @property
    def self_link(self):
        """URL to Scopus API page of this abstract."""
        return get_link(self._json, 0)

    @property
    def sequencebank(self):
        """List of namedtuples representing biological entities defined or
        mentioned in the text, in the form (name, sequence_number, type).
        """
        path = ['enhancement', 'sequencebanks', 'sequencebank']
        items = listify(chained_get(self._head, path, []))
        bank = namedtuple('Sequencebank', 'name sequence_number type')
        out = []
        for item in items:
            numbers = listify(item['sequence-number'])
            for number in numbers:
                new = bank(name=item['@name'], sequence_number=number['$'],
                           type=number['@type'])
                out.append(new)
        return out or None

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
        area = namedtuple('Area', 'area abbreviation code')
        path = ['subject-areas', 'subject-area']
        out = [area(area=item['$'], abbreviation=item['@abbrev'],
                    code=item['@code'])
               for item in listify(chained_get(self._json, path, []))]
        return out or None

    @property
    def title(self):
        """Title of the abstract."""
        return self._json['coredata'].get('dc:title')

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
        return chained_get(self._head, ['source', 'website', 'ce:e-address', '$'])

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
            effect for already cached files.  Allowed values: META, META_ABS,
            REF, FULL, where FULL includes all information of META_ABS view
            and META_ABS includes all information of the META view.  See
            https://dev.elsevier.com/guides/AbstractRetrievalViews.htm
            for details.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        Raises
        ------
        ValueError
            If the id_type parameter or the view parameter contains
            invalid entries.

        Notes
        -----
        The files are cached in ~/.scopus/abstract_retrieval/{identifier}.  In
        case a DOI is used as identifier, an underscore replaces the forward
        slash in the filename.
        """
        # Checks
        if identifier is None and EID:
            text = "Parameter EID is deprecated in favor of parameter "\
                   "identifier.  Please update your code."
            warn(text, UserWarning)
            identifier = EID
        identifier = str(identifier)
        allowed_views = ('META', 'META_ABS', 'REF', 'FULL')
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
        Retrieval.__init__(self, identifier=identifier, id_type=id_type,
                           api='AbstractRetrieval', refresh=refresh, view=view)
        self._json = self._json['abstracts-retrieval-response']
        self._head = chained_get(self._json, ["item", "bibrecord", "head"], {})
        path = ['source', 'additional-srcinfo', 'conferenceinfo', 'confevent']
        self._confevent = chained_get(self._head, path, {})

    def __str__(self):
        """Return pretty text version of the abstract.

        Assumes the abstract is a journal article and was loaded with
        view="META_ABS" or view="FULL".
        """
        # Authors
        if len(self.authors) > 1:
            authors = _list_authors(self.authors)
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
        title = u'<a href="{}">{}</a>'.format(self.scopus_link, self.title)
        if self.volume and self.issueIdentifier:
            volissue = u'<b>{}({})</b>'.format(self.volume, self.issueIdentifier)
        elif self.volume:
            volissue = u'<b>{}</b>'.format(self.volume)
        else:
            volissue = 'no volume'
        jlink = '<a href="https://www.scopus.com/source/sourceInfo.url'\
                '?sourceId={}">{}</a>'.format(
                    self.source_id, self.publicationName)
        pages = _parse_pages(self, unicode=True)
        s = "{auth}, {title}, {jour}, {volissue}, {pages}, ({year}).".format(
                auth=authors, title=title, jour=jlink, volissue=volissue,
                pages=pages, year=self.coverDate[:4])
        if self.doi:
            s += ' <a href="https://doi.org/{0}">doi:{0}</a>.'.format(self.doi)
        return s

    def get_latex(self):
        """Bibliographic entry in LaTeX format."""
        if len(self.authors) > 1:
            authors = _list_authors(self.authors)
        else:
            a = self.authors
            authors = ' '.join([a.given_name, a.surname])
        if self.volume and self.issueIdentifier:
            volissue = '\\textbf{{{}({})}}'.format(self.volume, self.issueIdentifier)
        elif self.volume:
            volissue = '\\textbf{{{}}}'.format(self.volume)
        else:
            volissue = 'no volume'
        pages = _parse_pages(self)
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


def _get_org(aff):
    """Auxiliary function to extract org information from affiliation
    for authorgroup.
    """
    try:
        org = aff['organization']
        if not isinstance(org, str):
            try:
                org = org['$']
            except TypeError:  # Multiple names given
                org = ', '.join([d['$'] for d in org if d])
    except KeyError:  # Author group w/o affiliation
        org = None
    return org


def _list_authors(lst):
    """Format a list of authors (Surname, Firstname and Firstname Surname)."""
    authors = ', '.join([' '.join([a.given_name, a.surname]) for a in lst[0:-1]])
    authors += ' and ' + ' '.join([lst[-1].given_name, lst[-1].surname])
    return authors


def _parse_pages(self, unicode=False):
    """Auxiliary function to parse and format page range of a document."""
    if self.pageRange:
        pages = 'pp. {}'.format(self.pageRange)
    elif self.startingPage:
        pages = 'pp. {}-{}'.format(self.startingPage, self.endingPage)
    else:
        pages = '(no pages found)'
    if unicode:
        pages = u'{}'.format(pages)
    return pages


def _select_by_idtype(lst, selector):
    """Auxiliary function to return items matching a special idtype."""
    return [d['$'] for d in lst if d['@idtype'] == selector]
