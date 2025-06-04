"""Nonserial title class."""

from typing import Optional, Union

from pybliometrics.superclasses import Retrieval

from pybliometrics.utils import chained_get, check_parameter_value, VIEWS



class NonserialTitle(Retrieval):
    @property
    def aggregation_type(self) -> str:
        """The type of the source."""
        return self._entry['prism:aggregationType']

    @property
    def authors(self) -> Optional[str]:
        """The authors of the book."""
        return self._entry.get('authors')


    @property
    def description(self) -> Optional[str]:
        """The description of the book."""
        return self._entry.get('description')

    @property
    def edition(self) -> Optional[str]:
        """The edition of the book."""
        return self._entry.get('prism:edition')

    @property
    def editors(self) -> Optional[str]:
        """The editors of the book."""
        return self._entry.get('editors')

    @property
    def isbn(self) -> str:
        """The ISBN of the book."""
        return self._entry['prism:isbn']

    @property
    def link_coverimage(self) -> str:
        """The link to the cover image of the book."""
        links = self._entry.get('link')
        return [link['@href'] for link in links if link['@rel'] == 'coverimage'][0]

    @property
    def link_homepage(self) -> str:
        """The link to the homepage of the book."""
        links = self._entry.get('link')
        return [link['@href'] for link in links if link['@rel'] == 'homepage'][0]

    @property
    def link_search(self) -> str:
        """The link to search for the book."""
        links = self._entry.get('link')
        return [link['@href'] for link in links if link['@rel'] == 'search'][0]

    @property
    def publisher_id(self) -> str:
        """The publisher id of the book."""
        return chained_get(self._entry, ['dc:publisher', '@id'])

    @property
    def publisher_name(self) -> str:
        """The publisher of the book."""
        return chained_get(self._entry, ['dc:publisher', '$'])

    @property
    def self_link(self) -> str:
        """URL to the source's API page."""
        return self._entry['prism:url']

    @property
    def title(self) -> str:
        """The title of the book."""
        return self._entry['dc:title']

    def __init__(self,
                 isbn: Union[int, str],
                 view: str = "STANDARD",
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ) -> None:
        """Interaction with the ScienceDirect Nonserial Title API.

        :param isbn: The ISBN of the book.
        :param view: The view of the file that should be downloaded. Allowed value: "STANDARD".
                     For details see `the documentation <https://dev.elsevier.com/sd_nonserial_title_views.html>`_.
                     Note that although the "BASIC" view is documented, the API does not support it.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the number of days since
                        last modification exceeds that value.
        :param kwds: Keywords passed on as query parameters. Must contain fields and values
                     mentioned in the `API specification <https://dev.elsevier.com/documentation/NonSerialTitleAPI.wadl>`_.

        :raises ValueError: If any of the parameters `refresh` or `view` is not one of the allowed values.

        .. note::
           The directory for cached results is ``{path}/{view}/{source_id}``,
           where `path` is specified in your configuration file.
        """
        # Checks
        check_parameter_value(view, VIEWS['NonserialTitle'], "view")

        self._view = view
        self._refresh = refresh
        self._id = str(isbn)

        # Load json
        Retrieval.__init__(self, identifier=self._id, **kwds)

        # Parse json
        self._json = self._json['nonserial-metadata-response']
        self._entry = self._json['entry'][0]
