from collections import namedtuple
from typing import List, NamedTuple, Optional, Tuple, Union

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import check_integrity, check_parameter_value,\
    check_field_consistency, listify, make_search_summary


class AuthorSearch(Search):
    @property
    def authors(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples storing author information,
        where each namedtuple corresponds to one author.
        The information in each namedtuple is `(eid orcid surname initials givenname
        documents affiliation affiliation_id city country areas)`.

        All entries are `str` or `None`.  Areas combines abbreviated subject
        areas followed by the number of documents in this subject.

        Raises
        ------
        ValueError
            If the elements provided in `integrity_fields` do not match the
            actual field names (listed above).
        """
        # Initiate namedtuple with ordered list of fields
        fields = 'eid orcid surname initials givenname affiliation documents '\
                 'affiliation_id city country areas'
        auth = namedtuple('Author', fields)
        check_field_consistency(self._integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            name = item.get('preferred-name', {})
            aff = item.get('affiliation-current', {})
            fields = item.get('subject-area',
                              [{'@abbrev': '', '@frequency': ''}])
            areas = [f"{d.get('@abbrev', '')} ({d.get('@frequency', '')})"
                     for d in listify(fields)]
            new = auth(eid=item.get('eid'),
                       orcid=item.get('orcid'),
                       initials=name.get('initials'),
                       surname=name.get('surname'),
                       areas="; ".join(areas),
                       givenname=name.get('given-name'),
                       documents=int(item['document-count']),
                       affiliation=aff.get('affiliation-name'),
                       affiliation_id=aff.get('affiliation-id'),
                       city=aff.get('affiliation-city'),
                       country=aff.get('affiliation-country'))
            out.append(new)
        # Finalize
        check_integrity(out, self._integrity, self._action)
        return out or None

    def __init__(self,
                 query: str,
                 refresh: Union[bool, int] = False,
                 verbose: bool = False,
                 download: bool = True,
                 integrity_fields: Union[List[str], Tuple[str, ...]] = None,
                 integrity_action: str = "raise",
                 **kwds: str
                 ) -> None:
        """Interaction with the Author Search API.

        :param query: A string of the query.  For allowed fields and values see
                      https://dev.elsevier.com/sc_author_search_tips.html.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If `int` is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param download: Whether to download results (if they have not been
                         cached).
        :param verbose: Whether to print a download progress bar.
        :param integrity_fields: Names of fields whose completeness should
                                 be checked.  `ScopusSearch` will perform the
                                 action specified in `integrity_action` if
                                 elements in these fields are missing.  This
                                 helps avoiding idiosynchratically missing
                                 elements that should always be present
                                 (e.g., EID or source ID).
        :param integrity_action: What to do in case integrity of provided fields
                                 cannot be verified.  Possible actions:
                                 - `"raise"`: Raise an `AttributeError`
                                 - `"warn"`: Raise a `UserWarning`
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/AuthorSearchAPI.wadl.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds 5000, which is the API's
            maximum number of results returned.  The error prevents the
            download attempt and avoids making use of your API key.

        ValueError
            If any of the parameters `integrity_action` or `refresh` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/STANDARD/{fname}`,
        where  `path` is specified in your configuration file, and `fname` is
        the md5-hashed version of `query`.
        """
        # Checks
        allowed = ("warn", "raise")
        check_parameter_value(integrity_action, allowed, "integrity_action")

        # Query
        self._action = integrity_action
        self._integrity = integrity_fields or []
        self._query = query
        self._refresh = refresh
        self._view = "STANDARD"
        Search.__init__(self, query=query, api='AuthorSearch',
                        download=download, verbose=verbose, **kwds)

    def __str__(self):
        """Print a summary string."""
        names = [f'{n["preferred-name"].get("surname", "?")}, '
                 f'{n["preferred-name"].get("given-name", "?")}; '
                 f'{n["dc:identifier"]} ({int(n["document-count"]):,} document(s))'
                 for n in self._json]
        return make_search_summary(self, "author", names)
