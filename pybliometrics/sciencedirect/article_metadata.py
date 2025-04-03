from collections import namedtuple
from typing import Optional, Union

from pybliometrics.superclasses import Search
from pybliometrics.utils import check_field_consistency, chained_get, \
    check_integrity, check_parameter_value, deduplicate, \
    make_search_summary, VIEWS


class ArticleMetadata(Search):
    @property
    def results(self) -> Optional[list[namedtuple]]:
        """A list of namedtuples in the form `(authorKeywords authors available_online_date
        first_author abstract_text doi title eid link openArchiveArticle openaccess_status
        openaccessArticle openaccessUserLicense pii aggregationType copyright coverDate
        coverDisplayDate edition endingPage isbn publicationName startingPage teaser
        api_link publicationType vor_available_online_date)`.

        Field definitions correspond to the `Article Metadata Views
        <https://dev.elsevier.com/sd_article_meta_views.html>`__ and return the
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
        fields = 'authorKeywords authors available_online_date first_author abstract_text ' \
            'doi title eid link openArchiveArticle openaccess_status openaccessArticle '\
            'openaccessUserLicense pii aggregationType copyright coverDate coverDisplayDate '\
            'edition endingPage isbn publicationName startingPage teaser api_link publicationType '\
            'vor_available_online_date'
        doc = namedtuple('Document', fields)
        check_field_consistency(self._integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            # Get authors and create ";" separated string
            authors_list = [author.get('$') for author in chained_get(item, ['authors', 'author'], [])]
            authors_list = deduplicate(authors_list)
            authors = ';'.join(authors_list)
            first_author = item.get('dc:creator')[0].get('$')
            link = item.get('link')[0].get('@href')
            doi = item.get("prism:doi") or item.get("dc:identifier")[4:] if item.get("dc:identifier") else None
            new = doc(
                authorKeywords=item.get('authkeywords'),
                authors=authors,
                available_online_date=item.get('available-online-date'),
                first_author=first_author,
                abstract_text=item.get('dc:description'),
                doi=doi,
                title=item.get('dc:title'),
                eid=item.get('eid'),
                link=link,
                openArchiveArticle=item.get('openArchiveArticle'),
                openaccess_status=item.get('openaccess'),
                openaccessArticle=item.get('openaccessArticle'),
                openaccessUserLicense=item.get('openaccessUserLicense'),
                pii=item.get('pii'),
                aggregationType=item.get('prism:aggregationType'),
                copyright=item.get('prism:copyright'),
                coverDate=item.get('prism:coverDate'),
                coverDisplayDate=item.get('prism:coverDisplayDate'),
                edition=item.get('prism:edition'),
                endingPage=item.get('prism:endingPage'),
                isbn=item.get('prism:isbn'),
                publicationName=item.get('prism:publicationName'),
                startingPage=item.get('prism:startingPage'),
                teaser=item.get('prism:teaser'),
                api_link=item.get('prism:url'),
                publicationType=item.get('pubType'),
                vor_available_online_date=item.get('vor-available-online-date'),
            )
            out.append(new)
        check_integrity(out, self._integrity, self._action)
        return out or None

    def __init__(self,
                 query: str,
                 refresh: Union[bool, int] = False,
                 view: str = None,
                 verbose: bool = False,
                 download: bool = True,
                 integrity_fields: Union[list[str], tuple[str, ...]] = None,
                 integrity_action: str = "raise",
                 subscriber: bool = True,
                 **kwds: str
                 ) -> None:
        """Interaction with the ScienceDirect Article Metadata API.

        :param query: A string of the query as used in the `Advanced Search <https://dev.elsevier.com/tecdoc_sdsearch_migration.html>`__.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: Which view to use for the query, see `the documentation <https://dev.elsevier.com/sd_article_meta_views.html>`__.
                     Allowed values: `STANDARD`, `COMPLETE`.  If `None`, defaults to
                     `COMPLETE` if `subscriber=True` and to `STANDARD` if
                     `subscriber=False`.
        :param verbose: Whether to print a download progress bar.
        :param download: Whether to download results (if they have not been
                         cached).
        :param integrity_fields: A list or tuple with the names of fields whose completeness should
                                 be checked.  `ArticleMetadata` will perform the
                                 action specified in `integrity_action` if
                                 elements in these fields are missing.  This
                                 helps to avoid idiosynchratically missing
                                 elements that should always be present
                                 (e.g., EID or source ID).
        :param integrity_action: What to do in case integrity of provided fields
                                 cannot be verified.  Possible actions:
                                 - `"raise"`: Raise an `AttributeError`
                                 - `"warn"`: Raise a `UserWarning`
        :param subscriber: Whether you access ScienceDirect with a subscription or not.
                           For subscribers, ScienceDirect's cursor navigation will be
                           used.  Sets the number of entries in each query
                           iteration to the maximum number allowed by the
                           corresponding view.
        :param unescape: Convert named and numeric characters in the `results` to
                        their corresponding Unicode characters.
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
        """
        # Check view or set to default
        if view:
            check_parameter_value(view, VIEWS['ArticleMetadata'], "view")
        else:
            view = "COMPLETE" if subscriber else "STANDARD"

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
        return make_search_summary(self, "document", self.get_eids())

    def get_eids(self):
        """EIDs of retrieved documents."""
        return [d['eid'] for d in self._json]
