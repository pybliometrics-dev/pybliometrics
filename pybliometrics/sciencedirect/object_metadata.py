"""Module with the ObjectMetadata class."""

from typing import NamedTuple

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import chained_get, check_parameter_value, detect_id_type, make_int_if_possible, VIEWS


class Metadata(NamedTuple):
    """Named tuple representing metadata of a document object."""
    eid: str
    filename: str | None
    height: int | None
    mimetype: str | None
    ref: str | None
    size: int | None
    type: str | None
    url: str | None
    width: int | None


class ObjectMetadata(Retrieval):
    """Class to retrieve a the metadata of all objects of a document."""
    @property
    def results(self) -> list[Metadata]:
        """Metadata of the objects in a document. List of namedtuples in the form `eid`, `filename`,
        `height`, `mimetype`, `ref`, `size`, `type`, `url` and `width`.
        """
        refs = chained_get(self._json, ['attachment-metadata-response', 'attachment'], [])
        out = []
        for ref in refs:
            out.append(
                Metadata(
                    eid=ref["eid"],
                    filename=ref.get("filename"),
                    height=make_int_if_possible(ref.get("height")),
                    mimetype=ref.get("mimetype"),
                    ref=ref.get("ref"),
                    size=make_int_if_possible(ref.get("size")),
                    type=ref.get("type"),
                    url=ref.get("prism:url"),
                    width=make_int_if_possible(ref.get("width")),
                )
            )
        return out

    def __init__(self,
                 identifier: int | str,
                 view: str = 'META',
                 id_type: str | None = None,
                 refresh: bool | int = False,
                 **kwds: str
                 ):
        """Class to retrieve the metadata of all objects of a document.

        :param identifier: The indentifier of an article.
        :param view: The view of the object. Allowed value: `META`.
        :param id_type: The type of identifier supplied. Allowed values: `doi`,
                        `pii`, `scopus_id`, `pubmed_id`, `eid`.
        :param refresh: Whether to refresh the cached file if it exists. Default: `False`.
        """
        self.identifier = str(identifier)
        check_parameter_value(view, VIEWS['ObjectMetadata'], "view")

        self.id_type = id_type
        if self.id_type is None:
            self.id_type = detect_id_type(self.identifier)
        else:
            allowed_id_types = ('doi', 'pii', 'scopus_id', 'pubmed_id', 'eid')
            check_parameter_value(id_type, allowed_id_types, "id_type")

        self._view = view
        self._refresh = refresh

        super().__init__(self.identifier, self.id_type, **kwds)

    def __str__(self):
        return (f'Document with {self.id_type} {self.identifier} contains '
                f'{len(self.results)} objects.')
