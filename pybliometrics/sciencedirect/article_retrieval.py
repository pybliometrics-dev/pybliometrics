from typing import NamedTuple

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import (
    chained_get,
    check_parameter_value,
    detect_id_type,
    list_authors,
    make_bool_if_possible,
    make_int_if_possible,
    parse_pages,
    VIEWS,
)


class Author(NamedTuple):
    """Named tuple representing an author."""
    surname: str
    given_name: str


class ArticleRetrieval(Retrieval):
    @property
    def abstract(self) -> str | None:
        """The abstract of a document."""
        abstract = chained_get(self._json, ['coredata', 'dc:description'])
        if abstract:
            abstract = abstract.strip()
        return abstract

    @property
    def aggregationType(self) -> str | None:
        """The aggregation type of a document."""
        return chained_get(self._json, ['coredata', 'prism:aggregationType'])

    @property
    def authors(self) -> list[Author] | None:
        """The authors of a document."""
        out = []
        for author in chained_get(self._json, ['coredata', 'dc:creator']):
            surname, given_name = author['$'].split(', ')
            new = Author(surname=surname, given_name=given_name)
            out.append(new)
        return out or None

    @property
    def copyright(self) -> str | None:
        """The copyright of a document."""
        return chained_get(self._json, ['coredata', 'prism:copyright'])

    @property
    def coverDate(self) -> str | None:
        """The date of the cover the document is in."""
        return chained_get(self._json, ['coredata', 'prism:coverDate'])

    @property
    def coverDisplayDate(self) -> str | None:
        """The cover display date of a document."""
        return chained_get(self._json, ['coredata', 'prism:coverDisplayDate'])

    @property
    def document_entitlement_status(self) -> str | None:
        """Returns the document entitlement status, i.e. tells if the requestor 
        is entitled to the requested resource.
        Note: Only works with `ENTITLED` view.
        """
        return chained_get(self._json, ['document-entitlement', 'status'])

    @property
    def doi(self) -> str:
        """The doi of a document."""
        return chained_get(self._json, ['coredata', 'prism:doi'])

    @property
    def eid(self) -> str | None:
        """The eid of a document."""
        return chained_get(self._json, ['coredata', 'eid'])

    @property
    def endingPage(self) -> str | None:
        """The ending page of a document."""
        page = chained_get(self._json, ['coredata', 'prism:endingPage'])
        return page

    @property
    def issn(self) -> int:
        """The issn of a document."""
        return make_int_if_possible(chained_get(self._json, ['coredata', 'prism:issn']))

    @property
    def openaccess(self) -> bool:
        """The document is open access."""
        open_access = chained_get(self._json, ['coredata', 'openaccessArticle'])
        return make_bool_if_possible(open_access)

    @property
    def openaccessSponsorName(self) -> str | None:
        """The open access sponsor name of a document."""
        return chained_get(self._json, ['coredata', 'openaccessSponsorName'])

    @property
    def openaccessSponsorType(self) -> str | None:
        """The open access sponsor type of a document."""
        return chained_get(self._json, ['coredata', 'openaccessSponsorType'])

    @property
    def openaccessType(self) -> str | None:
        """The open access type of a document."""
        return chained_get(self._json, ['coredata', 'openaccessType'])

    @property
    def openaccessUserLicense(self) -> str | None:
        """The open access user license of a document."""
        return chained_get(self._json, ['coredata', 'openaccessUserLicense'])

    @property
    def openArchiveArticle(self) -> bool:
        """The document is an open archive article."""
        open_archive = chained_get(self._json, ['coredata', 'openArchiveArticle'])
        return make_bool_if_possible(open_archive)

    @property
    def originalText(self) -> str | None:
        """Complete document text."""
        return self._json.get('originalText')

    @property
    def pageRange(self) -> str | None:
        """The prism:pageRange of a document."""
        return chained_get(self._json, ['coredata', 'prism:pageRange'])

    @property
    def publicationName(self) -> str:
        """The publication name of a document (e.g. Journal of Economy and Technology)."""
        return chained_get(self._json, ['coredata', 'prism:publicationName'])

    @property
    def publisher(self) -> str | None:
        """The publisher of a document."""
        return chained_get(self._json, ['coredata', 'prism:publisher'])

    @property
    def pubType(self) -> str | None:
        """The publication type of a document."""
        return chained_get(self._json, ['coredata', 'pubType'])

    @property
    def pii(self) -> str:
        """The pii of a document."""
        return chained_get(self._json, ['coredata', 'pii'])

    @property
    def sciencedirect_link(self) -> str:
        """The ScienceDirect link of a document."""
        links = chained_get(self._json, ['coredata', 'link'])
        for link in links:
            if link['@rel'] == 'scidir':
                return link['@href']

    @property
    def self_link(self) -> str:
        """The API link of a document."""
        links = chained_get(self._json, ['coredata', 'link'])
        for link in links:
            if link['@rel'] == 'self':
                return link['@href']

    @property
    def startingPage(self) -> str | None:
        """The starting page of a document."""
        return chained_get(self._json, ['coredata', 'prism:startingPage'])

    @property
    def subjects(self) -> list[str] | None:
        """The subjects of a document."""
        subjects = chained_get(self._json, ['coredata', 'dcterms:subject'])
        return [subject['$'] for subject in subjects]

    @property
    def title(self) -> str:
        """The title of a document."""
        return chained_get(self._json, ['coredata', 'dc:title'])

    @property
    def url(self) -> str:
        """The url of a document."""
        return chained_get(self._json, ['coredata', 'prism:url'])

    @property
    def volume(self) -> int | None:
        """The prism:volume of a document."""
        vol = chained_get(self._json, ['coredata', 'prism:volume'])
        return make_int_if_possible(vol)

    def __init__(self,
                 identifier: int | str,
                 refresh: bool | int = False,
                 view: str = 'META',
                 id_type: str | None = None,
                 **kwds: str
                 ):
        """Interaction with the Article Retrieval API.
        
        :param identifier: The indentifier of an article.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: The view of the file that should be downloaded. Allowed values:
                     'META', 'META_ABS', 'META_ABS_REF', 'FULL', 'ENTITLED'. Default: 'META'.
        :param id_type: The type of used ID. Allowed values: `None`, 'eid', 'pii',
                        'scopus_id', 'pubmed_id' and 'doi'.  If the value is `None`,
                        pybliometrics tries to infer the ID type itself.
        """
        identifier = str(identifier)
        check_parameter_value(view, VIEWS['ArticleRetrieval'], "view")
        if id_type is None:
            id_type = detect_id_type(identifier)
        else:
            allowed_id_types = ('eid', 'pii', 'scopus_id', 'pubmed_id', 'doi')
            check_parameter_value(id_type, allowed_id_types, "id_type")

        self._view = view
        self._refresh = refresh

        Retrieval.__init__(self, identifier=identifier, id_type=id_type, **kwds)
        if self._view != "ENTITLED":
            self._json = self._json['full-text-retrieval-response']

    def __str__(self):
        s = ''
        if self._view in ('FULL', 'META_ABS', 'META'):
            if self.authors:
                if len(self.authors) > 1:
                    authors = list_authors(self.authors)
                else:
                    a = self.authors[0]
                    authors = str(a.given_name) + ' ' + str(a.surname)
            else:
                authors = "(No author found)"
            # All other information
            s += f'{authors}: "{self.title}", {self.publicationName}'
            s += f', {self.volume}' if self.volume else ''
            s += ', '
            s += parse_pages(self)
            s += f'({self.coverDate[:4]}).'
            if self.doi:
                s += f' https://doi.org/{self.doi}.'
        return s
