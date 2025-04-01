from collections import namedtuple
from typing import Optional, Union

from pybliometrics.superclasses import Search
from pybliometrics.utils import check_field_consistency, chained_get, \
    check_integrity, check_parameter_value, deduplicate, \
    make_search_summary, VIEWS


class ScienceDirectSearch(Search):
    @property
    def results(self) -> Optional[list[namedtuple]]:
        """A list of namedtuples in the form `(authors first_author doi title link
        load_date openaccess_status pii coverDate endingPage publicationName startingPage
        api_link volume)`.

        Field definitions correspond to the `ScienceDirect Search Views
        <https://dev.elsevier.com/sd_search_views.htmll>`__ and return the
        values as-is, except for `authors` which are joined on `";"`.

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
        fields = 'authors first_author doi title link load_date openaccess_status pii '\
            'coverDate endingPage publicationName startingPage api_link volume'
        doc = namedtuple('Document', fields)
        check_field_consistency(self._integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            # Get authors and create ";" separated string
            authors_list = self._get_authors(item)
            authors_list = deduplicate(authors_list)
            authors = ';'.join(authors_list)
            # Get links
            links_found = item.get('link')
            links = {'api_link': None, 'scidir': None}
            for link in links_found:
                if link.get('@ref') == 'self':
                    links['api_link'] = link.get('@href')
                elif link.get('@ref') == 'scidir':
                    links['scidir'] = link.get('@href')
            # Get doi
            doi = item.get("prism:doi") or item.get("dc:identifier")[4:] if item.get("dc:identifier") else None
            new = doc(
                authors=authors,
                first_author=item.get('dc:creator'),
                doi=doi,
                title=item.get("dc:title"),
                link=links["scidir"],
                load_date=item.get("load-date"),
                openaccess_status=item.get("openaccess"),
                pii=item.get("pii"),
                coverDate=item.get("prism:coverDate"),
                endingPage=item.get("prism:endingPage"),
                publicationName=item.get("prism:publicationName"),
                startingPage=item.get("prism:startingPage"),
                api_link=links["api_link"] or item.get("prism:url"),
                volume=item.get("prism:volume")
            )
            out.append(new)
        check_integrity(out, self._integrity, self._action)
        return out or None

    def __init__(self,
                 query: str,
                 refresh: Union[bool, int] = False,
                 view: Optional[str] = None,
                 verbose: bool = False,
                 download: bool = True,
                 integrity_fields: Optional[Union[list[str], tuple[str, ...]]] = None,
                 integrity_action: str = "raise",
                 subscriber: bool = True,
                 **kwds: str
                 ) -> None:
        """Interaction with the ScienceDirect Search API. This represents a search against the
        ScienceDirect cluster, which contains serial/nonserial full-text articles. Note that this API
        replicates the search experience on `ScienceDirect <www.sciencedirect.com>`__.

        :param query: A string of the query as used in the `ScienceDirect Search <https://dev.elsevier.com/tecdoc_sdsearch_migration.html>`__.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: Which view to use for the query, see `the documentation <https://dev.elsevier.com/sd_search_views.html>`__.
                     Allowed values: `STANDARD`.
        :param verbose: Whether to print a download progress bar.
        :param download: Whether to download results (if they have not been
                         cached).
        :param integrity_fields: A list or tuple with the names of fields whose completeness should
                                 be checked.  `ArticleMetadata` will perform the
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
                     fields and values mentioned in the `API specification <https://dev.elsevier.com/documentation/ArticleMetadataAPI.wadl>`__.

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
        the md5-hashed version of `query`.

        The ScienceDirect Search API V2 has two available interfaces: `PUT` and `GET`. This library uses the
        `GET` interface.
        """
        # Check view or set to default
        if view:
            check_parameter_value(view, VIEWS['ScienceDirectSearch'], "view")
        else:
            view = "STANDARD"

        allowed = ("warn", "raise")
        check_parameter_value(integrity_action, allowed, "integrity_action")

        # Query
        self._action = integrity_action
        self._integrity = integrity_fields or []
        self._refresh = refresh
        self._query = query
        self._view = view
        Search.__init__(self, query=query, download=download, verbose=verbose, **kwds)

    def __str__(self):
        """Print a summary string."""
        return make_search_summary(self, "document", self.get_dois())

    def get_dois(self):
        """DOIs of retrieved documents."""
        return [d.get("prism:doi") or d.get("dc:identifier")[4:] if d.get("dc:identifier") else None for d in self._json]

    def _get_authors(self, item: dict) -> list:
        """Auxiliary function to get the authors."""
        authors_data = chained_get(item, ['authors', 'author'], [])
        if isinstance(authors_data, list):
            authors_list = [a.get('$') for a in authors_data]
        elif isinstance(authors_data, str):
            authors_list = [authors_data]
        else:
            authors_list = []
        return authors_list
