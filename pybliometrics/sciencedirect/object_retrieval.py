"""Module to retrieve a specific object of a document."""

from io import BytesIO
from typing import Optional, Union

from pybliometrics.sciencedirect import ArticleRetrieval
from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import check_parameter_value, detect_id_type


class ObjectRetrieval(Retrieval):
    @property
    def object(self) -> BytesIO:
        """The object retrieved."""
        return BytesIO(self._object)

    def __init__(self,
                 identifier: Union[int, str],
                 filename: str,
                 id_type: Optional[str] = None,
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ):
        """Class to retrieve a specific object of a document by its filename.

        :param identifier: The indentifier of the document.
        :param filename: Filename of the object to be retrieved.  To get a list
                         of all available objects of a document (and its
                         corresponding filename) use the class `ObjectMetadata`.
        :param id_type: Document identifier.  Allowed values: `doi`, `pii`,
                        `scopus_id`, `pubmed_id`, `eid`.
        :param refresh: Whether to refresh the cached file if it exists.  Default: False.
        """
        identifier = str(identifier)

        if id_type is None:
            id_type = detect_id_type(identifier)
        else:
            allowed_id_types = ('doi', 'pii', 'scopus_id', 'pubmed_id', 'eid')
            check_parameter_value(id_type, allowed_id_types, "id_type")

        if id_type != 'eid':
            identifier = self._get_eid(identifier)
        file_identifier = f'{identifier}-{filename}'

        self._view = ''
        self._refresh = refresh

        super().__init__(file_identifier, 'eid', **kwds)

    def _get_eid(self, identifier: str) -> str:
        """Get the EID of a document."""
        am = ArticleRetrieval(identifier, field='eid')
        return am.eid
