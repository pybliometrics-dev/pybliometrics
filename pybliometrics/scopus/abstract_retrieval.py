from collections import defaultdict, namedtuple
from typing import List, NamedTuple, Optional, Tuple, Union

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import chained_get, check_parameter_value,\
    deduplicate, get_id, detect_id_type, get_link, listify,\
    make_int_if_possible, parse_date_created, VIEWS


class AbstractRetrieval(Retrieval):
    @property
    def abstract(self) -> Optional[str]:
        """The abstract of a document.
        Note: If this is empty, try `description` property instead.
        """
        return self._head.get('abstracts')

    @property
    def affiliation(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing listed affiliations in
        the form `(id, name, city, country)`.
        """
        out = []
        aff = namedtuple('Affiliation', 'id name city country')
        affs = listify(self._json.get('affiliation', []))
        for item in affs:
            new = aff(id=make_int_if_possible(item.get('@id')), name=item.get('affilname'),
                      city=item.get('affiliation-city'),
                      country=item.get('affiliation-country'))
            out.append(new)
        return out or None

    @property
    def aggregationType(self) -> str:
        """Aggregation type of source the document is published in."""
        return chained_get(self._json, ['coredata', 'prism:aggregationType'])

    @property
    def authkeywords(self) -> Optional[List[str]]:
        """List of author-provided keywords of the document."""
        keywords = self._json.get('authkeywords')
        if not keywords:
            return None
        else:
            try:
                return [d['$'] for d in keywords['author-keyword']]
            except TypeError:  # Singleton keyword
                return [keywords['author-keyword']['$']]

    @property
    def authorgroup(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing the article's authors and collaborations
        organized by affiliation, in the form `(affiliation_id, collaboration_id, dptid,
        organization, city, postalcode, addresspart, country, auid, orcid,
        indexed_name, surname, given_name)`.
        If `given_name` is not present, fall back to initials.
        Note: Affiliation information might be missing or mal-assigned even
        when it looks correct in the web view.  In this case please request
        a correction.  It is generally missing for collaborations.
        """
        # Information can be one of three forms:
        # 1. A dict with one key (author) or two keys (affiliation and author)
        # 2. A list of dicts with as in 1, one for each affiliation (incl. missing)
        # 3. A list of two dicts with one key each (author and collaboration)
        # Initialization
        fields = 'affiliation_id collaboration_id dptid organization city postalcode '\
            'addresspart country auid orcid indexed_name surname given_name'
        auth = namedtuple('Author', fields, defaults=[None for _ in fields.split()])
        items = listify(self._head.get('author-group', []))
        out = []
        for item in filter(None, items):
            # Get all possible items: affiliation, author, collaboration
            aff = item.get('affiliation', {})
            authors = item.get('author', [])
            collaborations = item.get('collaboration', {})
            # Affiliation information
            aff_id = make_int_if_possible(aff.get("@afid"))
            dep_id = make_int_if_possible(aff.get("@dptid"))
            org = _get_org(aff)
            # Author information
            for author in authors:
                new = auth(affiliation_id=aff_id,
                            organization=org,
                            city=aff.get('city'),
                            dptid=dep_id,
                            postalcode=aff.get('postal-code'),
                            addresspart=aff.get('address-part'),
                            country=aff.get('country'),
                            auid=make_int_if_possible(author.get('@auid')),
                            orcid=author.get('@orcid'),
                            surname=author.get('ce:surname'),
                            given_name=author.get('ce:given-name', author['ce:initials']),
                            indexed_name=chained_get(author, ['preferred-name', 'ce:indexed-name']))
                out.append(new)
            # Collaboration information
            for collaboration in filter(None, listify(collaborations)):
                new = auth(collaboration_id=collaboration.get('@collaboration-instance-id'),
                        indexed_name=collaboration.get('ce:indexed-name'))
                out.append(new)
        return out or None

    @property
    def authors(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing the article's authors, in the
        form `(auid, indexed_name, surname, given_name, affiliation)`.  In case
        multiple affiliation IDs are given, they are joined on `";"`.
        Note: The affiliation referred to here is what Scopus' algorithm
        determined as the main affiliation.  Property `authorgroup` provides
        all affiliations.
        """
        out = []
        fields = 'auid indexed_name surname given_name affiliation'
        auth = namedtuple('Author', fields)
        for item in chained_get(self._json, ['authors', 'author'], []):
            affs = [a for a in listify(item.get('affiliation')) if a] or None
            try:
                aff = ";".join([aff.get('@id') for aff in affs])
            except TypeError:
                aff = None
            new = auth(auid=int(item['@auid']), surname=item.get('ce:surname'),
                       indexed_name=item.get('ce:indexed-name'), affiliation=aff,
                       given_name=chained_get(item, ['preferred-name', 'ce:given-name']))
            out.append(new)
        return out or None

    @property
    def citedby_count(self) -> Optional[int]:
        """Number of articles citing the document."""
        path = ['coredata', 'citedby-count']
        return make_int_if_possible(chained_get(self._json, path))

    @property
    def citedby_link(self) -> str:
        """URL to Scopus page listing citing documents."""
        return get_link(self._json, 2)

    @property
    def chemicals(self) -> Optional[List[NamedTuple]]:
        """List of namedtuples representing chemical entities in the form
        `(source, chemical_name, cas_registry_number)`.  In case multiple
        numbers given, they are joined on `";"`.
        """
        path = ['enhancement', 'chemicalgroup', 'chemicals']
        items = listify(chained_get(self._head, path, []))
        fields = 'source chemical_name cas_registry_number'
        chemical = namedtuple('Chemical', fields)
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
    def confcode(self) -> Optional[int]:
        """Code of the conference the document belongs to."""
        return make_int_if_possible(self._confevent.get('confcode'))

    @property
    def confdate(self) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Date range of the conference the document belongs to represented
        by two tuples in the form (YYYY, MM, DD).
        """
        dates = self._confevent.get('confdate', {})
        try:
            keys = ("startdate", "enddate")
            date_order = ("@year", "@month", "@day")
            d = (tuple(int(dates[k1][k2]) for k2 in date_order) for k1 in keys)
            return tuple(d)
        except KeyError:
            return None

    @property
    def conflocation(self) -> Optional[str]:
        """Location of the conference the document belongs to."""
        return chained_get(self._confevent, ['conflocation', 'city-group'])

    @property
    def confname(self) -> Optional[str]:
        """Name of the conference the document belongs to."""
        return self._confevent.get('confname')

    @property
    def confsponsor(self) -> Optional[Union[List[str], str]]:
        """Sponsor(s) of the conference the document belongs to."""
        path = ['confsponsors', 'confsponsor']
        sponsors = chained_get(self._confevent, path, [])
        if len(sponsors) == 0:
            return None
        if isinstance(sponsors, list):
            return [s['$'] for s in sponsors]
        return sponsors

    @property
    def contributor_group(self) -> Optional[List[NamedTuple]]:
        """List of namedtuples representing contributors compiled by Scopus,
        in the form `(given_name, initials, surname, indexed_name, role)`.
        """
        path = ['source', 'contributor-group']
        items = listify(chained_get(self._head, path, []))
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
    def copyright(self) -> str:
        """The copyright statement of the document."""
        path = ['item', 'bibrecord', 'item-info', 'copyright', '$']
        return chained_get(self._json, path)

    @property
    def copyright_type(self) -> str:
        """The copyright holder of the document."""
        path = ['item', 'bibrecord', 'item-info', 'copyright', '@type']
        return chained_get(self._json, path)

    @property
    def correspondence(self) -> Optional[List[NamedTuple]]:
        """List of namedtuples representing the authors to whom correspondence
        should be addressed, in the form ´(surname, initials, organization,
        country, city_group)´. Multiple organziations are joined on semicolon.
        """
        fields = 'surname initials organization country city_group'
        auth = namedtuple('Correspondence', fields)
        items = listify(self._head.get('correspondence', []))
        out = []
        for item in items:
            aff = item.get('affiliation', {})
            try:
                org = aff['organization']
                try:
                    org = org['$']
                except TypeError:  # Multiple names given
                    org = "; ".join([d['$'] for d in org])
            except KeyError:
                org = None
            new = auth(surname=item.get('person', {}).get('ce:surname'),
                       initials=item.get('person', {}).get('ce:initials'),
                       organization=org, country=aff.get('country'),
                       city_group=aff.get('city-group'))
            out.append(new)
        return out or None

    @property
    def coverDate(self) -> str:
        """The date of the cover the document is in."""
        return chained_get(self._json, ['coredata', 'prism:coverDate'])

    @property
    def date_created(self) -> Optional[Tuple[int, int, int]]:
        """Return the `date_created` of a record.
        """
        path = ["item", "bibrecord", "item-info", "history"]
        d = chained_get(self._json, path, {})
        try:
            return parse_date_created(d)
        except KeyError:
            return None

    @property
    def description(self) -> Optional[str]:
        """Return the description of a record.
        Note: If this is empty, try `abstract` property instead.
        """
        return chained_get(self._json, ['coredata', 'dc:description'])

    @property
    def document_entitlement_status(self) -> Optional[str]:
        """Returns the document entitlement status, i.e. tells if the requestor 
        is entitled to the requested resource.
        Note: Only works with `ENTITLED` view.
        """
        return chained_get(self._json, ['document-entitlement', 'status'])
        

    @property
    def doi(self) -> Optional[str]:
        """DOI of the document."""
        return chained_get(self._json, ['coredata', 'prism:doi'])

    @property
    def eid(self) -> str:
        """EID of the document."""
        return chained_get(self._json, ['coredata', 'eid'])

    @property
    def endingPage(self) -> Optional[str]:
        """Ending page. If this is empty, try `pageRange` property instead."""
        # Try coredata first, fall back to head afterwards
        ending = chained_get(self._json, ['coredata', 'prism:endingPage'])
        if not ending:
            path = ['source', 'volisspag', 'pagerange', '@last']
            ending = chained_get(self._head, path)
        return ending

    @property
    def funding(self) -> Optional[List[NamedTuple]]:
        """List of namedtuples parsed funding information in the form
        `(agency, agency_id, string, funding_id, acronym, country)`.
        """

        def _get_funding_id(f_dict: dict) -> list:
            funding_get = f_dict.get('xocs:funding-id', [])
            try:
                return [v['$'] for v in funding_get] or None  # multiple or empty
            except TypeError:
                return [funding_get]  # single

        path = ['item', 'xocs:meta', 'xocs:funding-list', 'xocs:funding']
        funds = listify(chained_get(self._json, path, []))
        out = []
        fields = 'agency agency_id string funding_id acronym country'
        fund = namedtuple('Funding', fields)
        for item in funds:
            new = fund(agency=item.get('xocs:funding-agency'),
                       agency_id=item.get('xocs:funding-agency-id'),
                       string=item.get('xocs:funding-agency-matched-string'),
                       funding_id=_get_funding_id(item),
                       acronym=item.get('xocs:funding-agency-acronym'),
                       country=item.get('xocs:funding-agency-country'))
            out.append(new)
        return out or None

    @property
    def funding_text(self) -> Optional[str]:
        """The raw text from which Scopus derives funding information."""
        path = ['item', 'xocs:meta', 'xocs:funding-list', 'xocs:funding-text']
        return chained_get(self._json, path)

    @property
    def isbn(self) -> Optional[Tuple[str, ...]]:
        """ISBNs `Optional[str]` to publicationName as tuple of variying length,
        (e.g. ISBN-10 or ISBN-13)."""
        isbns = listify(chained_get(self._head, ['source', 'isbn'], []))
        if len(isbns) == 0:
            return None
        else:
            return tuple((i['$'] for i in isbns))

    @property
    def issn(self) -> Optional[NamedTuple]:
        """Namedtuple in the form `(print electronic)`.
        Note: If the source has an E-ISSN, the META view will return None.
        Use FULL view instead.
        """
        container = defaultdict(lambda: None)
        # Parse information from head (from FULL view)
        info = listify(chained_get(self._head, ['source', 'issn'], []))
        for t in info:
            try:
                container[t["@type"]] = t["$"]
            except TypeError:
                container["print"] = t
        # Parse information from coredata as fallback
        fallback = chained_get(self._json, ['coredata', 'prism:issn'])
        if fallback and len(container) < 2:
            parts = fallback.split()
            if len(parts) == 2:
                if len(container) == 1:
                    for n, o in (("electronic", "print"), ("print", "electronic")):
                        if n not in container:
                            container[n] = [p for p in parts if p != container[o]]
                else:
                    # no way to find out which is which
                    pass
            else:
                container["print"] = parts[0]
        # Finalize
        issns = namedtuple('ISSN', 'print electronic', defaults=(None, None))
        if not container:
            return None
        else:
            return issns(**container)

    @property
    def identifier(self) -> int:
        """ID of the document (same as EID without "2-s2.0-")."""
        return get_id(self._json)

    @property
    def idxterms(self) -> Optional[List[str]]:
        """List of index terms (these are just one category of those
        Scopus provides in the web version)
        ."""
        try:
            terms = listify(self._json.get("idxterms", {}).get('mainterm', []))
        except AttributeError:  # idxterms is empty
            return None
        try:
            return [d['$'] for d in terms] or None
        except AttributeError:
            return None

    @property
    def issueIdentifier(self) -> Optional[str]:
        """Number of the issue the document was published in."""
        return chained_get(self._json, ['coredata', 'prism:issueIdentifier'])

    @property
    def issuetitle(self) -> Optional[str]:
        """Title of the issue the document was published in."""
        return chained_get(self._head, ['source', 'issuetitle'])

    @property
    def language(self) -> Optional[str]:
        """Language of the article."""
        return chained_get(self._json, ['language', '@xml:lang'])

    @property
    def openaccess(self) -> Optional[int]:
        """The openaccess status encoded in single digits."""
        path = ['coredata', 'openaccess']
        return make_int_if_possible(chained_get(self._json, path))

    @property
    def openaccessFlag(self) -> Optional[bool]:
        """Whether the document is available via open access or not."""
        flag = chained_get(self._json, ['coredata', 'openaccessFlag'])
        if flag:
            flag = flag == "true"
        return flag

    @property
    def pageRange(self) -> Optional[str]:
        """Page range.  If this is empty, try `startingPage` and
        `endingPage` properties instead.
        """
        # Try data from coredata first, fall back to head afterwards
        pages = chained_get(self._json, ['coredata', 'prism:pageRange'])
        if not pages:
            return chained_get(self._head, ['source', 'volisspag', 'pages'])
        return pages

    @property
    def pii(self) -> Optional[str]:
        """The PII (Publisher Item Identifier) of the document."""
        return chained_get(self._json, ['coredata', 'pii'])

    @property
    def publicationName(self) -> Optional[str]:
        """Name of source the document is published in."""
        return chained_get(self._json, ['coredata', 'prism:publicationName'])

    @property
    def publisher(self) -> Optional[str]:
        """Name of the publisher of the document.
        Note: Information provided in the FULL view of the article might be
        more complete.
        """
        # Return information from FULL view, fall back to other views
        full = chained_get(self._head, ['source', 'publisher', 'publishername'])
        if full is None:
            return chained_get(self._json, ['coredata', 'dc:publisher'])
        else:
            return full

    @property
    def publisheraddress(self) -> Optional[str]:
        """Name of the publisher of the document."""
        return chained_get(self._head, ['source', 'publisher', 'publisheraddress'])

    @property
    def pubmed_id(self) -> Optional[int]:
        """The PubMed ID of the document."""
        path = ['coredata', 'pubmed-id']
        return make_int_if_possible(chained_get(self._json, path))

    @property
    def refcount(self) -> Optional[int]:
        """Number of references of an article.
        Note: Requires either the FULL view or REF view.
        """
        try:  # REF view
            return int(self._ref['@total-references'])
        except KeyError:  # FULL view
            try:
                return int(self._ref['@refcount'])
            except KeyError:
                return None

    @property
    def references(self) -> Optional[List[NamedTuple]]:
        """List of namedtuples representing references listed in the document,
        in the form `(position, id, doi, title, authors, authors_auid,
        authors_affiliationid, sourcetitle, publicationyear, coverDate, volume,
        issue, first, last, citedbycount, type, text, fulltext)`.

        `position` is the number at which the reference appears in the
        document, `id` is the Scopus ID of the referenced document (EID
        without the "2-s2.0-"), `authors` is a string of the names of the
        authors in the format "Surname1, Initials1; Surname2, Initials2",
        `authors_auid` is a string of the author IDs joined on "; ",
        `authors_affiliationid` is a string of the authors' affiliation IDs
        joined on "; ", `sourcetitle` is the name of the source (e.g. the
        journal), `publicationyear` is the year of the publication as string
        (FULL view only), `coverDate` is the date of the publication as string
        (REF view only), `volume` and `issue`, are strings referring to the
        volume and issue, `first` and `last` refer to the page range,
        `citedbycount` the total number of citations of the cited item (REF
        view only), `type` describes the parsing status of the reference
        (resolved or not), `text` is information on the publication,
        `fulltext` is the text the authors used for the reference.

        Note: Requires either the FULL view or REF view.
        Might be empty even if refcount is positive.  Specific fields can
        be empty.
        The lists `authors` and `authors_auid` may contain duplicates because of
        the 1:1 pairing with the list `authors_affiliationid`.
        """
        out = []
        fields = 'position id doi title authors authors_auid '\
                 'authors_affiliationid sourcetitle publicationyear coverDate '\
                 'volume issue first last citedbycount type text fulltext'
        ref = namedtuple('Reference', fields)
        items = listify(self._ref.get("reference", []))
        for item in items:
            try:
                info = item.get('ref-info', item)
            except AttributeError:  # item not a dictionary
                continue
            volisspag = info.get('volisspag', {}) or {}
            if isinstance(volisspag, list):
                volisspag = volisspag[0]
            volis = volisspag.get("voliss", {})
            if isinstance(volis, list):
                volis = volis[0]
            # Parse author information
            if self._view == 'FULL':  # FULL view parsing
                auth = listify(info.get('ref-authors', {}).get('author', []))
                authors = [', '.join(filter(None, [d.get('ce:surname'),
                                                   d.get('ce:initials')]))
                           for d in auth]
                auids = None
                affids = None
                ids = listify(info['refd-itemidlist']['itemid'])
                doi = _select_by_idtype(ids, id_type='DOI')
                scopus_id = _select_by_idtype(ids, id_type='SGR')
            else:  # REF view parsing
                auth = (info.get('author-list') or {}).get('author', [])
                auth = deduplicate(auth)
                authors = [', '.join(filter(None, [d.get('ce:surname'),
                                                   d.get('ce:given-name')]))
                           for d in auth]
                auids = "; ".join(filter(None, [d.get('@auid') for d in auth]))
                affs = filter(None, [d.get('affiliation') for d in auth])
                affids = "; ".join([aff.get('@id') for aff in affs])
                doi = info.get('ce:doi')
                scopus_id = info.get('scopus-id')
            # Combine information
            new = ref(position=item.get('@id'), id=scopus_id, doi=doi,
                authors="; ".join(authors), authors_auid=auids or None,
                authors_affiliationid=affids or None,
                title=info.get('ref-title', {}).get('ref-titletext', info.get('title')),
                sourcetitle=info.get('ref-sourcetitle', info.get('sourcetitle')),
                publicationyear=info.get('ref-publicationyear', {}).get('@first'),
                coverDate=info.get('prism:coverDate'),
                volume=volis.get('@volume'), issue=volis.get('@issue'),
                first=volisspag.get('pagerange', {}).get('@first'),
                last=volisspag.get('pagerange', {}).get('@last'),
                citedbycount=info.get('citedby-count'), type=info.get('type'),
                text=info.get('ref-text'),
                fulltext=item.get('ref-fulltext'))
            out.append(new)
        return out or None

    @property
    def scopus_link(self) -> str:
        """URL to the document page on Scopus."""
        return get_link(self._json, 1)

    @property
    def self_link(self) -> str:
        """URL to Scopus API page of this document."""
        return get_link(self._json, 0)

    @property
    def sequencebank(self) -> Optional[List[NamedTuple]]:
        """List of namedtuples representing biological entities defined or
        mentioned in the text, in the form `(name, sequence_number, type)`.
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
    def source_id(self) -> Optional[int]:
        """Scopus source ID of the document."""
        path = ['coredata', 'source-id']
        return make_int_if_possible(chained_get(self._json, path))

    @property
    def sourcetitle_abbreviation(self) -> Optional[str]:
        """Abbreviation of the source the document is published in.
        Note: Requires the FULL view of the article.
        """
        return self._head.get('source', {}).get('sourcetitle-abbrev')

    @property
    def srctype(self) -> Optional[str]:
        """Aggregation type of source the document is published in (short
        version of aggregationType).
        """
        return chained_get(self._json, ['coredata', 'srctype'])

    @property
    def startingPage(self) -> Optional[str]:
        """Starting page.  If this is empty, try `pageRange` property instead."""
        # Try coredata first, fall back to bibrecord afterwards
        starting = chained_get(self._json, ['coredata', 'prism:startingPage'])
        if not starting:
            path = ['source', 'volisspag', 'pagerange', '@first']
            starting = chained_get(self._head, path)
        return starting

    @property
    def subject_areas(self) -> Optional[List[NamedTuple]]:
        """List of namedtuples containing subject areas of the article
        in the form `(area abbreviation code)`.
        Note: Requires the FULL view of the article.
        """
        area = namedtuple('Area', 'area abbreviation code')
        path = ['subject-areas', 'subject-area']
        out = [area(area=item['$'], abbreviation=item['@abbrev'],
                    code=int(item['@code']))
               for item in listify(chained_get(self._json, path, []))]
        return out or None

    @property
    def subtype(self) -> str:
        """Type of the document.  Refer to the Scopus Content Coverage Guide
        for a list of possible values.  Short version of subtypedescription.
        """
        return chained_get(self._json, ['coredata', 'subtype']) or None

    @property
    def subtypedescription(self) -> str:
        """Type of the document.  Refer to the Scopus Content Coverage Guide
        for a list of possible values.  Long version of subtype.
        """
        return chained_get(self._json, ['coredata', 'subtypeDescription']) or None

    @property
    def title(self) -> Optional[str]:
        """Title of the document."""
        return chained_get(self._json, ['coredata', 'dc:title'])

    @property
    def url(self) -> Optional[str]:
        """URL to the API view of the document."""
        return chained_get(self._json, ['coredata', 'prism:url'])

    @property
    def volume(self) -> Optional[str]:
        """Volume for the document."""
        return chained_get(self._json, ['coredata', 'prism:volume'])

    @property
    def website(self) -> str:
        """Website of publisher."""
        path = ['source', 'website', 'ce:e-address', '$']
        return chained_get(self._head, path)

    def __init__(self,
                 identifier: Union[int, str] = None,
                 refresh: Union[bool, int] = False,
                 view: str = 'META_ABS',
                 id_type: str = None,
                 **kwds: str
                 ) -> None:
        """Interaction with the Abstract Retrieval API.

        :param identifier: The identifier of a document.  Can be the Scopus EID
                           , the Scopus ID, the PII, the Pubmed-ID or the DOI.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param id_type: The type of used ID. Allowed values: None, 'eid', 'pii',
                        'scopus_id', 'pubmed_id', 'doi'.  If the value is None,
                        the function tries to infer the ID type itself.
        :param view: The view of the file that should be downloaded.  Allowed
                     values: META, META_ABS, REF, FULL, ENTITLED, where FULL includes all
                     information of META_ABS view and META_ABS includes all
                     information of the META view.  For details see
                     https://dev.elsevier.com/sc_abstract_retrieval_views.html.
                     Note: `ENTITLED` view only contains the `document_entitlement_status`.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values listed in the API specification at
                     https://dev.elsevier.com/documentation/AbstractRetrievalAPI.wadl.

        Raises
        ------
        ValueError
            If any of the parameters `id_type`, `refresh` or `view` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{identifier}`,
        where `path` is specified in your configuration file.  In case
        `identifier` is a DOI, an underscore replaces the forward slash.
        """
        # Checks
        identifier = str(identifier)
        check_parameter_value(view, VIEWS['AbstractRetrieval'], "view")
        if id_type is None:
            id_type = detect_id_type(identifier)
        else:
            allowed_id_types = ('eid', 'pii', 'scopus_id', 'pubmed_id', 'doi')
            check_parameter_value(id_type, allowed_id_types, "id_type")

        # Load json
        self._view = view
        self._refresh = refresh
        Retrieval.__init__(self, identifier=identifier, id_type=id_type,
                           api='AbstractRetrieval', **kwds)
        if self._view in ('META', 'META_ABS', 'REF', 'FULL'):
            self._json = self._json['abstracts-retrieval-response']
        self._head = chained_get(self._json, ["item", "bibrecord", "head"], {})
        conf_path = ['source', 'additional-srcinfo', 'conferenceinfo', 'confevent']
        self._confevent = chained_get(self._head, conf_path, {})
        if self._view == "REF":
            ref_path = ["references"]
        else:
            ref_path = ['item', 'bibrecord', 'tail', 'bibliography']
        self._ref = chained_get(self._json, ref_path, {})

    def __str__(self):
        """Return pretty text version of the document.

        Assumes the document is a journal article and was loaded with
        view="META_ABS" or view="FULL".
        """
        def convert_citedbycount(entry):
                try:
                    return float(entry.citedbycount) or 0
                except (ValueError, TypeError):
                    return 0
            
        def get_date(coverDate):
            try:
                return coverDate[:4]
            except TypeError:
                return None
                
        if self._view in ('FULL', 'META_ABS', 'META'):
            date = self.get_cache_file_mdate().split()[0]
            # Authors
            if self.authors:
                if len(self.authors) > 1:
                    authors = _list_authors(self.authors)
                else:
                    a = self.authors[0]
                    authors = str(a.given_name) + ' ' + str(a.surname)
            else:
                authors = "(No author found)"
            # All other information
            s = f'{authors}: "{self.title}", {self.publicationName}, {self.volume}'
            if self.issueIdentifier:
                s += f'({self.issueIdentifier})'
            s += ', '
            s += _parse_pages(self)
            s += f'({self.coverDate[:4]}).'
            if self.doi:
                s += f' https://doi.org/{self.doi}.\n'
            s += f'{self.citedby_count} citation(s) as of {date}'
            if self.affiliation:
                s += "\n  Affiliation(s):\n   "
                s += '\n   '.join([aff.name for aff in self.affiliation])
        
        elif self._view in ('REF'):
            try:
                # Sort reference list by citationcount
                top_n = 5
                references = sorted(self.references, key=convert_citedbycount, reverse=True)

                top_references = [f'{reference.title} ({get_date(reference.coverDate)}). '+
                                f'EID: {reference.id}' for reference in references[:top_n]]
            except TypeError:
                top_n = 0

            s = f'A total of {self.refcount or 0} references were found. '
            if top_n:
                s += f'Top {top_n} references:\n\t'
                s += '\n\t'.join(top_references)

        return s

    def get_bibtex(self) -> str:
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
        authors = ' and '.join([f"{a.given_name} {a.surname}"
                                for a in self.authors])
        # Pages
        if self.pageRange:
            pages = self.pageRange
        elif self.startingPage:
            pages = f'{self.startingPage}-{self.endingPage}'
        else:
            pages = '-'
        # All information
        bib = f"@article{{{key},\n  author = {{{authors}}},\n  title = "\
              f"{{{{{self.title}}}}},\n  journal = {{{self.publicationName}}},"\
              f"\n  year = {{{year}}},\n  volume = {{{self.volume}}},\n  "\
              f"number = {{{self.issueIdentifier}}},\n  pages = {{{pages}}}"
        # DOI
        if self.doi:
            bib += f",\n  doi = {{{self.doi}}}"
        bib += "}"
        return bib

    def get_html(self) -> str:
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
        title = f'<a href="{self.scopus_link}">{self.title}</a>'
        if self.volume and self.issueIdentifier:
            volissue = f'<b>{self.volume}({self.issueIdentifier})</b>'
        elif self.volume:
            volissue = f'<b>{self.volume}</b>'
        else:
            volissue = 'no volume'
        jlink = '<a href="https://www.scopus.com/source/sourceInfo.url'\
                f'?sourceId={self.source_id}">{self.publicationName}</a>'
        s = f"{authors}, {title}, {jlink}, {volissue}, " +\
            f"{_parse_pages(self, unicode=True)}, ({self.coverDate[:4]})."
        if self.doi:
            s += f' <a href="https://doi.org/{self.doi}">doi:{self.doi}</a>.'
        return s

    def get_latex(self) -> str:
        """Bibliographic entry in LaTeX format."""
        if len(self.authors) > 1:
            authors = _list_authors(self.authors)
        else:
            a = self.authors
            authors = ' '.join([a.given_name, a.surname])
        if self.volume and self.issueIdentifier:
            volissue = f'\\textbf{{{self.volume}({self.issueIdentifier})}}'
        elif self.volume:
            volissue = f'\\textbf{{{self.volume}}}'
        else:
            volissue = 'no volume'
        s = f'{authors}, \\textit{{{self.title}}}, {self.publicationName}, ' +\
            f'{volissue}, {_parse_pages(self)} ({self.coverDate[:4]}).'
        if self.doi:
            s += f' \\href{{https://doi.org/{self.doi}}}{{doi:{self.doi}}}, '
        s += f'\\href{{{self.scopus_link}}}{{scopus:{self.eid}}}.'
        return s

    def get_ris(self) -> str:
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
        ris = f"TY  - JOUR\nTI  - {self.title}\nJO  - {self.publicationName}"\
              f"\nVL  - {self.volume}\nDA  - {self.coverDate}\n"\
              f"PY  - {self.coverDate[0:4]}\nSP  - {self.pageRange}\n"
        # Authors
        for au in self.authors:
            ris += f'AU  - {au.indexed_name}\n'
        # DOI
        if self.doi:
            ris += f'DO  - {self.doi}\nUR  - https://doi.org/{self.doi}\n'
        # Issue
        if self.issueIdentifier:
            ris += f'IS  - {self.issueIdentifier}\n'
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
        pages = f'pp. {self.pageRange}'
    elif self.startingPage:
        pages = f'pp. {self.startingPage}-{self.endingPage}'
    else:
        pages = '(no pages found)'
    if unicode:
        pages = f'{pages}'
    return pages


def _select_by_idtype(lst, id_type):
    """Auxiliary function to return items matching a special idtype."""
    try:
        return [d['$'] for d in lst if d['@idtype'] == id_type][0]
    except IndexError:
        return None
