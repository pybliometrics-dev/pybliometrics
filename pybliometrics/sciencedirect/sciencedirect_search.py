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
        A list of namedtuples in the form `(authors doi loadDate openAccess first_page last_page
        pii publicationDate sourceTitle title uri volumeIssue)`.

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
                 query: dict,
                 refresh: Union[bool, int] = False,
                 view: Optional[str] = None,
                 verbose: bool = False,
                 download: bool = True,
                 integrity_fields: Optional[Union[list[str], tuple[str, ...]]] = None,
                 integrity_action: str = "raise",
                 subscriber: bool = True,
                 ) -> None:
        """
        Interaction with the ScienceDirect Search API using the `PUT` method.
        See the official `documentation <https://dev.elsevier.com/tecdoc_sdsearch_migration.html>`__ 
        for more details.

        Parameters
        ----------
        query : dict
            The query to be sent to the API, e.g.,
            {'qs': '"Neural Networks" AND "Shapley"', 'date': '2019-2020'}

        refresh : bool or int, optional
            Whether to refresh the cached file. If an int is passed, the cache
            will refresh if older than that many days.

        view : str, optional
            The API view to use. Default is "STANDARD".

        verbose : bool, optional
            Whether to print a download progress bar.

        download : bool, optional
            Whether to download results (if they haven't been cached).

        integrity_fields : list of str or tuple of str, optional
            Fields whose completeness should be checked. If any field is missing,
            the `integrity_action` will be triggered.

        integrity_action : {'raise', 'warn'}, optional
            What to do if required fields are missing:
            
            - 'raise' : Raise an AttributeError
            - 'warn' : Emit a UserWarning

        subscriber : bool, optional
            If True, cursor navigation is enabled, allowing more than 5,000 results.
        
        Raises
        ------
        ScopusQueryError
            For non-subscribers, if the number of search results exceeds 5000.

        ValueError
            If any of the parameters `integrity_action`, `refresh` or `view`
            is not one of the allowed values.

        """
        if view:
            check_parameter_value(view, VIEWS['ScienceDirectSearch'], "view")
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
                        verbose=verbose)

    def __str__(self):
        """Print a summary string."""
        dois = [d.doi for d in self.results] if self.results else []
        return make_search_summary(self, "document", dois)
