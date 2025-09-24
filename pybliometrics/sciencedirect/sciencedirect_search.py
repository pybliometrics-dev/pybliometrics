"""ScienceDirectSearch class for searching documents in ScienceDirect."""
from collections import namedtuple
from typing import Optional, Union

from pybliometrics.superclasses import Search
from pybliometrics.utils import check_field_consistency, chained_get, \
    check_integrity, check_parameter_value, deduplicate, make_int_if_possible, \
    make_search_summary, VIEWS


class ScienceDirectSearch(Search):
    @property
    def results(self) -> Optional[list]:
        """
        A list of namedtuples in the form `(authors, doi, loadDate, openAccess, first_page, last_page
        pii, publicationDate, sourceTitle, title, uri, volumeIssue)`.

        Field definitions correspond to the `ScienceDirect Search API Migration Documentation
        <https://dev.elsevier.com/tecdoc_sdsearch_migration.html>`__ and return the
        values as-is, except for `authors` which are joined on `";"` and pages which are
        parsed into `first_page` and `last_page`.

        Raises
        ------
        ValueError
            If the elements provided in `integrity_fields` do not match the
            actual field names (listed above).

        Notes
        -----
        The list of authors and the list of affiliations per author are
        deduplicated.
        """
        fields = 'authors doi loadDate openAccess first_page last_page pii publicationDate ' \
                 'sourceTitle title uri volumeIssue'
        doc = namedtuple('Document', fields)
        check_field_consistency(self._integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            # Get authors and create ";" separated string
            authors_list = deduplicate([a.get('name') for a in item.get('authors', {})])
            authors = "; ".join(authors_list)
            new = doc(
                authors=authors,
                doi=item.get('doi'),
                loadDate=item.get('loadDate'),
                openAccess=item.get('openAccess'),
                first_page=make_int_if_possible(chained_get(item, ('pages', 'first'))),
                last_page=make_int_if_possible(chained_get(item, ('pages', 'last'))),
                pii=item.get('pii'),
                publicationDate=item.get('publicationDate'),
                sourceTitle=item.get('sourceTitle'),
                title=item.get('title'),
                uri=item.get('uri'),
                volumeIssue=item.get('volumeIssue')
            )
            out.append(new)
        check_integrity(out, self._integrity, self._action)
        return out or None

    def __init__(self,
                 query: Optional[str] = None,
                 refresh: Union[bool, int] = False,
                 view: Optional[str] = None,
                 verbose: bool = False,
                 download: bool = True,
                 integrity_fields: Optional[Union[list[str], tuple[str, ...]]] = None,
                 integrity_action: str = "raise",
                 subscriber: bool = True,
                 **kwds: str
                 ) -> None:
        """
        Interaction with the ScienceDirect Search API using the `PUT` method.
        See the official `documentation <https://dev.elsevier.com/tecdoc_sdsearch_migration.html>`__ 
        for more details.

        :param query: Free text query string as the `qs`field in the `documentation
                      <https://dev.elsevier.com/tecdoc_sdsearch_migration.html>`__.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: Which view to use for the query, see `the documentation <https://dev.elsevier.com/sd_search_views.html>`__.
                     Allowed values: `STANDARD`.
        :param verbose: Whether to print a download progress bar.
        :param download: Whether to download results (if they have not been
                         cached).
        :param integrity_fields: A list or tuple with the names of fields whose completeness should
                                 be checked.  `ScienceDirectSearch` will perform the
                                 action specified in `integrity_action` if
                                 elements in these fields are missing.  This
                                 helps to avoid idiosynchratically missing
                                 elements that should always be present
                                 (e.g., doi or authors).
        :param integrity_action: What to do in case integrity of provided fields
                                 cannot be verified.  Possible actions:
                                 - `"raise"`: Raise an `AttributeError`
                                 - `"warn"`: Raise a `UserWarning`
        :param subscriber: Whether you access ScienceDirect with a subscription or not.
                           For subscribers, ScienceDirect's cursor navigation will be
                           used.  Sets the number of entries in each query
                           iteration to the maximum number allowed by the
                           corresponding view.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the `API specification <https://dev.elsevier.com/tecdoc_sdsearch_migration.html>`__.
        
        Raises
        ------
        ScopusQueryError
            For non-subscribers, if the number of search results exceeds 5000.

        ValueError
            If any of the parameters `integrity_action`, `refresh` or `view`
            is not one of the allowed values.
        
        Notes
        -----
        The directory for cached results is `{path}/{view}/{fname}`,
        where `path` is specified in your configuration file and `fname` is
        the md5-hashed version of the flattened `query`.

        """
        # Check if the query and keyword arguments are empty
        if not (query or kwds):
            msg = "The query is empty. Please provide either a query string or keyword arguments."
            raise ValueError(msg)
        query = query or ''

        if view:
            check_parameter_value(view, VIEWS["ScienceDirectSearch"], "view")
        else:
            view = "STANDARD"

        allowed = ("warn", "raise")
        check_parameter_value(integrity_action, allowed, "integrity_action")

        self._action = integrity_action
        self._integrity = integrity_fields or []
        self._refresh = refresh
        self._query = query
        self._view = view

        Search.__init__(self, query=query,
                        cursor=subscriber, download=download,
                        verbose=verbose, **kwds)

    def __str__(self):
        """Print a summary string."""
        dois = [d.doi for d in self.results] if self.results else []
        return make_search_summary(self, "document", dois)
