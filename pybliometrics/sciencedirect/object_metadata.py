"""Module with the ObjectMetadata class."""

from typing import Optional, Union

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import chained_get, check_parameter_value, detect_id_type, VIEWS


class ObjectMetadata(Retrieval):
    """Class to retrieve a the metadata of all objects of a document."""
    @property
    def results(self) -> list[dict]:
        """List with metadata of objects in a document. The metadata includes the `url`, `eid`,
        `ref`, `filename`, `mimetype`, `size`, `height`, `width`, and `type` of the object.
        """
        refs = chained_get(self._json, ['attachment-metadata-response', 'attachment'], [])
        out = []
        for ref in refs:
            out.append({'url': ref.get('prism:url'),
                        'eid': ref.get('eid'),
                        'ref': ref.get('ref'),
                        'filename': ref.get('filename'),
                        'mimetype': ref.get('mimetype'),
                        'size': ref.get('size'),
                        'height': ref.get('height'),
                        'width': ref.get('width'),
                        'type': ref.get('type')})
        return out


    def __init__(self,
                 identifier: Union[int, str],
                 view: str = 'META',
                 id_type: Optional[str] = None,
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ):
        """Class to retrieve the metadata of all objects of a document.
        :param identifier: The indentifier of an article.
        :param view: The view of the object. Allowed values: `META`.
        :param id_type: The type of identifier supplied. Allowed values: `doi`, `pii`, `scopus_id`,
        `pubmed_id`, `eid`.
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
