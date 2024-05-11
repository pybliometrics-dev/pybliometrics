from collections import namedtuple
from typing import Optional , Union

from pybliometrics.scopus.utils import (
    chained_get,
    check_parameter_value,
    detect_id_type,
    make_bool_if_possible,
    make_int_if_possible,
    VIEWS,
)
from pybliometrics.scopus.superclasses import Retrieval


class ArticleRetrieval(Retrieval):
    @property
    def abstract(self) -> Optional[str]:
        """The abstract of a document."""
        abstract = chained_get(self._json, ['coredata', 'dc:description'])
        if abstract:
            abstract = abstract.strip()
        return abstract


    @property
    def aggregationType(self) -> Optional[str]:
        """The aggregation type of a document."""
        return chained_get(self._json, ['coredata', 'prism:aggregationType'])


    @property
    def authors(self) -> list:
        """The authors of a document."""
        out = []
        auth = namedtuple('Author', 'surname given_name')
        for author in chained_get(self._json, ['coredata', 'dc:creator']):
            surname, given_name = author['$'].split(',')
            new = auth(surname=surname,
                    given_name=given_name)
            out.append(new)
        return out


    @property
    def copyright(self) -> Optional[str]:
        """The copyright of a document."""
        return chained_get(self._json, ['coredata', 'prism:copyright'])


    @property
    def coverDate(self) -> Optional[str]:
        """The date of the cover the document is in."""
        return chained_get(self._json, ['coredata', 'prism:coverDate'])


    @property
    def coverDisplayDate(self) -> Optional[str]:
        """The cover display date of a document."""
        return chained_get(self._json, ['coredata', 'prism:coverDisplayDate'])
 

    @property
    def doi(self) -> str:
        """The doi of a document."""
        return chained_get(self._json, ['coredata', 'prism:doi'])


    @property
    def eid(self) -> Optional[str]:
        """The eid of a document."""
        return chained_get(self._json, ['coredata', 'eid'])


    @property
    def endingPage(self) -> Optional[str]:
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
    def openaccessSponsorName(self) -> Optional[str]:
        """The open access sponsor name of a document."""
        return chained_get(self._json, ['coredata', 'openaccessSponsorName'])


    @property
    def openaccessSponsorType(self) -> Optional[str]:
        """The open access sponsor type of a document."""
        return chained_get(self._json, ['coredata', 'openaccessSponsorType'])


    @property
    def openaccessType(self) -> Optional[str]:
        """The open access type of a document."""
        return chained_get(self._json, ['coredata', 'openaccessType'])


    @property
    def openaccessUserLicense(self) -> Optional[str]:
        """The open access user license of a document."""
        return chained_get(self._json, ['coredata', 'openaccessUserLicense'])


    @property
    def openArchiveArticle(self) -> bool:
        """The document is an open archive article."""
        open_archive = chained_get(self._json, ['coredata', 'openArchiveArticle'])
        return make_bool_if_possible(open_archive)


    @property
    def pageRange(self) -> Optional[str]:
        """The prism:pageRange of a document."""
        return chained_get(self._json, ['coredata', 'prism:pageRange'])


    @property
    def publicationName(self) -> str:
        """The publication name of a document (e.g. Journal of Economy and Technology)."""
        return chained_get(self._json, ['coredata', 'prism:publicationName'])


    @property
    def publisher(self) -> Optional[str]:
        """The publisher of a document."""
        return chained_get(self._json, ['coredata', 'prism:publisher'])


    @property
    def pubType(self) -> Optional[str]:
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
    def startingPage(self) -> Optional[str]:
        """The starting page of a document."""
        return chained_get(self._json, ['coredata', 'prism:startingPage'])


    @property
    def subjects(self) -> Optional[str]:
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
    def volume(self) -> Optional[str]:
        """The prism:volume of a document."""
        vol = chained_get(self._json, ['coredata', 'prism:volume'])
        return make_int_if_possible(vol)


    def __init__(self,
                 identifier: Union[int, str] = None,
                 refresh: Union[bool, int] = False,
                 view: str = 'META',
                 id_type: str = None,
                 **kwds: str
                 ):
        """Interaction with the Article Retrieval API.
        
        :param identifier: The indentifier of an article."""
        identifier = str(identifier)
        check_parameter_value(view, VIEWS['ArticleRetrieval'], "view")
        if id_type is None:
            id_type = detect_id_type(identifier)
        else:
            allowed_id_types = ('eid', 'pii', 'scopus_id', 'pubmed_id', 'doi', 'pui')
            check_parameter_value(id_type, allowed_id_types, "id_type")

        self._view = view
        self._refresh = refresh

        Retrieval.__init__(
            self,
            identifier=identifier,
            id_type=id_type,
            api="ArticleRetrieval",
            **kwds
        )

        self._json = self._json['full-text-retrieval-response']
