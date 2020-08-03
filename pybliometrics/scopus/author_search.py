from collections import namedtuple

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import check_integrity, check_integrity_params,\
    check_field_consistency, listify, make_search_summary


class AuthorSearch(Search):
    @property
    def authors(self):
        """A list of namedtuples storing author information,
        where each namedtuple corresponds to one author.
        The information in each namedtuple is (eid surname initials givenname
        documents affiliation affiliation_id city country areas).

        All entries are strings or None.  Areas combines abbreviated subject
        areas followed by the number of documents in this subject.

        Raises
        ------
        ValueError
            If the elements provided in integrity_fields do not match the
            actual field names (listed above).
        """
        # Initiate namedtuple with ordered list of fields
        fields = 'eid surname initials givenname affiliation documents '\
                 'affiliation_id city country areas'
        auth = namedtuple('Author', fields)
        check_field_consistency(self.integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            name = item.get('preferred-name', {})
            aff = item.get('affiliation-current', {})
            fields = item.get('subject-area',
                              [{'@abbrev': '', '@frequency': ''}])
            areas = [f"{d.get('@abbrev', '')} ({d.get('@frequency', '')})"
                     for d in listify(fields)]
            new = auth(eid=item.get('eid'), initials=name.get('initials'),
                       surname=name.get('surname'), areas="; ".join(areas),
                       givenname=name.get('given-name'),
                       documents=item.get('document-count', '0'),
                       affiliation=aff.get('affiliation-name'),
                       affiliation_id=aff.get('affiliation-id'),
                       city=aff.get('affiliation-city'),
                       country=aff.get('affiliation-country'))
            out.append(new)
        # Finalize
        check_integrity(out, self.integrity, self.action)
        return out or None

    def __init__(self, query, refresh=False, count=200, download=True,
                 integrity_fields=None, integrity_action="raise",
                 verbose=False):
        """Interaction with the Author Search API.

        Parameters
        ----------
        query : str
            A string of the query, e.g. "authlast(Einstein) and
            authfirst(Albert)".

        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        count : int (optional, default=200)
            The number of entries to be displayed at once.  A smaller number
            means more queries with each query having less results.

        download : bool (optional, default=True)
            Whether to download results (if they have not been cached).

        integrity_fields : None or iterable (default=None)
            Iterable of field names whose completeness should be checked.
            ScopusSearch will perform the action specified in
            `integrity_action` if elements in these fields are missing.  This
            helps avoiding idiosynchratically missing elements that should
            always be present, such as the EID.

        integrity_action : str (optional, default="raise")
            What to do in case integrity of provided fields cannot be
            verified.  Possible actions:
            - "raise": Raise an AttributeError
            - "warn": Raise a UserWarning

        verbose : bool (optional, default=False)
            Whether to print a downloading progress bar to terminal. Has no
            effect for download=False.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds 5000.

        ValueError
            If the integrity_action parameter is not one of the allowed ones.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/AuthorSearch.html.

        Notes
        -----
        The directory for cached results is `{path}/STANDARD/{fname}`,
        where  `path` is specified in `~/.scopus/config.ini` and fname is
        the md5-hashed version of `query`.
        """
        # Checks
        check_integrity_params(integrity_action)

        # Query
        self.query = query
        Search.__init__(self, query=query, refresh=refresh, view="STANDARD",
                        api='AuthorSearch', count=count, download=download,
                        verbose=verbose)
        self.integrity = integrity_fields or []
        self.action = integrity_action

    def __str__(self):
        """Print a summary string."""
        names = [f'{n["preferred-name"].get("surname", "?")}, '\
                 f'{n["preferred-name"].get("given-name", "?")}; '\
                 f'{n["dc:identifier"]} ({int(n["document-count"]):,} document(s))'\
                 for n in self._json]
        return make_search_summary(self, "author", names)
