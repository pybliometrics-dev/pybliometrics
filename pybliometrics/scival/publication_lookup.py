from collections import namedtuple
from typing import Union, Optional

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import make_int_if_possible, chained_get, list_authors


class PublicationLookup(Retrieval):

    @property
    def authors(self) -> Optional[list[namedtuple]]:
        """A list of namedtuples representing listed authors in
        the form `(id, name, uri)`.
        """
        out = []
        fields = 'id name uri'
        auth = namedtuple('Author', fields)
        for item in chained_get(self._json, ['publication', 'authors'], []):
            new = auth(id=make_int_if_possible(item['id']), name=item.get('name'),
                       uri=item.get('uri'))
            out.append(new)
        return out or None

    @property
    def citation_count(self) -> Optional[int]:
        """Count of citations"""
        return make_int_if_possible(chained_get(self._json, ['publication', 'citationCount']))

    @property
    def doi(self) -> Optional[str]:
        """Digital Object Identifier (DOI)"""
        return chained_get(self._json, ['publication', 'doi'])

    @property
    def id(self) -> Optional[int]:
        """ID of the document (same as EID without "2-s2.0-")."""
        return make_int_if_possible(chained_get(self._json, ['publication', 'id']))

    @property
    def institutions(self) -> Optional[list[namedtuple]]:
        """A list of namedtuples representing listed institutions in
        the form `(id, name, country, country_code)`.
        """
        out = []
        fields = 'id name country country_code'
        auth = namedtuple('Institution', fields)
        for item in chained_get(self._json, ['publication', 'institutions'], []):
            new = auth(id=make_int_if_possible(item['id']), name=item.get('name'),
                       country=item.get('country'), country_code=item.get('countryCode'))
            out.append(new)
        return out or None

    @property
    def link(self) -> Optional[str]:
        """URL link"""
        return chained_get(self._json, ['link', '@href'])

    @property
    def publication_year(self) -> Optional[int]:
        """Year of publication"""
        return make_int_if_possible(chained_get(self._json, ['publication', 'publicationYear']))

    @property
    def sdgs(self) -> Optional[list[str]]:
        """Sustainable Development Goals."""
        return chained_get(self._json, ['publication', 'sdg'])

    @property
    def source_title(self) -> Optional[str]:
        """Title of source"""
        return chained_get(self._json, ['publication', 'sourceTitle'])

    @property
    def title(self) -> Optional[str]:
        """Publication title"""
        return chained_get(self._json, ['publication', 'title'])

    @property
    def topic_cluster_id(self) -> Optional[int]:
        """Topic cluster id"""
        return make_int_if_possible(chained_get(self._json, ['publication', 'topicClusterId']))

    @property
    def topic_id(self) -> Optional[int]:
        """Topic id"""
        return make_int_if_possible(chained_get(self._json, ['publication', 'topicId']))

    @property
    def type(self) -> Optional[str]:
        """Type of publication"""
        return chained_get(self._json, ['publication', 'type'])

    def __str__(self):
        """Return pretty text version of the document."""
        if len(self.authors) >= 1:
            author_count = len(self.authors)
            authors = f"{author_count} author(s) found"
        else:
            authors = "(No author found)"

        if len(self.institutions) >= 1:
            institution_count = len(self.institutions)
            institutions = f"{institution_count} institution(s) found"
        else:
            institutions = "(No institution found)"
        return (
            f"Document with Scopus Id {self.id or 'N/A'} received:\n"
            f"- Title: {self.title}\n"
            f"- DOI: {self.doi}\n"
            f"- Type: {self.type}\n"
            f"- Publication Year: {self.publication_year}\n"
            f"- {authors}\n"
            f"- {institutions}\n"
        )

    def __init__(self,
                 identifier: Union[int, str] = None,
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ) -> None:
        """Interaction with the Publication Lookup API.

            :param identifier: The Scopus ID of the publication.
            :param refresh: Whether to refresh the cached file if it exists or not.
                If int is passed, cached file will be refreshed if the
                number of days since last modification exceeds that value.
            :param kwds: Keywords passed on as query parameters.  Must contain
                fields and values mentioned in the API specification at
                https://dev.elsevier.com/documentation/SciValPublicationAPI.wadl.
        """
        self._view = ''
        self._refresh = refresh
        Retrieval.__init__(self, identifier=str(identifier), **kwds)
