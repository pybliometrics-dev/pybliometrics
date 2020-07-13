from collections import namedtuple

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import check_integrity, check_integrity_params,\
    check_field_consistency, listify, make_search_summary


class ScopusSearch(Search):
    @property
    def results(self):
        """A list of namedtuples in the form (eid doi pii pubmed_id title
        subtype subtypeDescription creator afid affilname affiliation_city affiliation_country
        author_count author_names author_ids author_afids coverDate
        coverDisplayDate publicationName issn source_id eIssn aggregationType
        volume issueIdentifier article_number pageRange description
        authkeywords citedby_count openaccess fund_acr fund_no fund_sponsor).
        Field definitions correspond to
        https://dev.elsevier.com/guides/ScopusSearchViews.htm, except for
        afid, affilname, affiliation_city, affiliation_country, author_count,
        author_names, author_ids and author_afids:  These information are
        joined on ";".  In case an author has multiple affiliations, they are
        joined on "-" (e.g. Author1Aff;Author2Aff1-Author2Aff2).

        Raises
        ------
        ValueError
            If the elements provided in integrity_fields do not match the
            actual field names (listed above).

        Notes
        -----
        The list of authors and the list of affiliations per author are
        deduplicated.
        """
        # Initiate namedtuple with ordered list of fields
        fields = 'eid doi pii pubmed_id title subtype subtypeDescription creator ' \
                 'afid affilname affiliation_city affiliation_country author_count ' \
                 'author_names author_ids author_afids coverDate '\
                 'coverDisplayDate publicationName issn source_id eIssn '\
                 'aggregationType volume issueIdentifier article_number '\
                 'pageRange description authkeywords citedby_count '\
                 'openaccess fund_acr fund_no fund_sponsor'
        doc = namedtuple('Document', fields)
        check_field_consistency(self.integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            info = {}
            # Parse affiliations
            info["affilname"] = _join(item, 'affilname')
            info["afid"] = _join(item, 'afid')
            info["aff_city"] = _join(item, 'affiliation-city')
            info["aff_country"] = _join(item, 'affiliation-country')
            # Parse authors
            try:
                # Deduplicate list of authors
                authors = _deduplicate(item['author'])
                # Extract information
                surnames = _replace_none([d['surname'] for d in authors])
                firstnames = _replace_none([d['given-name'] for d in authors])
                info["auth_names"] = ";".join([", ".join([t[0], t[1]]) for t in
                                               zip(surnames, firstnames)])
                info["auth_ids"] = ";".join([d['authid'] for d in authors])
                affs = []
                for auth in authors:
                    aff = listify(_deduplicate(auth.get('afid', [])))
                    affs.append('-'.join([d['$'] for d in aff]))
                info["auth_afid"] = (';'.join(affs) or None)
            except KeyError:
                pass
            date = item.get('prism:coverDate')
            if isinstance(date, list):
                date = date[0].get('$')
            new = doc(article_number=item.get('article-number'),
                      title=item.get('dc:title'), fund_no=item.get('fund-no'),
                      fund_sponsor=item.get('fund-sponsor'),
                      subtype=item.get('subtype'), doi=item.get('prism:doi'),
                      subtypeDescription=item.get('subtypeDescription'),
                      issn=item.get('prism:issn'), creator=item.get('dc:creator'),
                      affilname=info.get("affilname"),
                      author_names=info.get("auth_names"),
                      coverDate=date, volume=item.get('prism:volume'),
                      coverDisplayDate=item.get('prism:coverDisplayDate'),
                      publicationName=item.get('prism:publicationName'),
                      source_id=item.get('source-id'), author_ids=info.get("auth_ids"),
                      aggregationType=item.get('prism:aggregationType'),
                      issueIdentifier=item.get('prism:issueIdentifier'),
                      pageRange=item.get('prism:pageRange'),
                      author_afids=info.get("auth_afid"),
                      affiliation_country=info.get("aff_country"),
                      citedby_count=item.get('citedby-count'),
                      openaccess=item.get('openaccess'), eIssn=item.get('prism:eIssn'),
                      author_count=item.get('author-count', {}).get('$'),
                      affiliation_city=info.get("aff_city"), afid=info.get("afid"),
                      description=item.get('dc:description'), pii=item.get('pii'),
                      authkeywords=item.get('authkeywords'), eid=item.get('eid'),
                      fund_acr=item.get('fund-acr'), pubmed_id=item.get('pubmed-id'))
            out.append(new)
        # Finalize
        check_integrity(out, self.integrity, self.action)
        return out or None

    def __init__(self, query, refresh=False, subscriber=True, view=None,
                 download=True, integrity_fields=None,
                 integrity_action="raise", verbose=False, **kwds):
        """Interaction with the Scopus Search API.

        Parameters
        ----------
        query : str
            A string of the query.

        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        subscriber : bool (optional, default=True)
            Whether the user accesses Scopus with a subscription or not.
            For subscribers, Scopus's cursor navigation will be used.
            Sets the number of entries in each query iteration to the maximum
            number allowed by the corresponding view.

        view : str (optional, default=None)
            Which view to use for the query, see
            https://dev.elsevier.com/guides/ScopusSearchViews.htm.
            Allowed values: STANDARD, COMPLETE.  If None, defaults to
            COMPLETE if subscriber=True and to STANDARD if subscriber=False.

        download : bool (optional, default=True)
            Whether to download results (if they have not been cached).

        integrity_fields : None or iterable (default=None)
            Iterable of field names whose completeness should be checked.
            ScopusSearch will perform the action specified in
            `integrity_action` if elements in these fields are missing.  This
            helps avoiding idiosynchratically missing elements that should
            always be present, such as the EID or the source ID.

        integrity_action : str (optional, default="raise")
            What to do in case integrity of provided fields cannot be
            verified.  Possible actions:
            - "raise": Raise an AttributeError
            - "warn": Raise a UserWarning

        verbose : bool (optional, default=False)
            Whether to print a downloading progress bar to terminal.
            Has no effect for download=False or when query file is
            in cache.

        kwds : key-value parings, optional
            Keywords passed on as query parameters.  Must contain fields
            and values listed mentioned in the API specification
            (https://dev.elsevier.com/documentation/SCOPUSSearchAPI.wadl),
            such as "field" or "date".

        Raises
        ------
        ScopusQueryError
            For non-subscribers, if the number of search results exceeds 5000.

        ValueError
            If the view or the integrity_action parameter is not one of
            the allowed ones.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/ScopusSearch.html.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{fname}`,
        where `path` is specified in `~/.scopus/config.ini` and fname is
        the md5-hashed version of `query`.
        """
        # Checks
        allowed_views = ('STANDARD', 'COMPLETE')
        if view and view not in allowed_views:
            msg = 'view parameter must be one of ' + ', '.join(allowed_views)
            raise ValueError(msg)
        check_integrity_params(integrity_action)

        # Parameters
        if not view:
            if subscriber:
                view = "COMPLETE"
            else:
                view = "STANDARD"
        count = 25
        if view == "STANDARD" and subscriber:
            count = 200
        if "cursor" in kwds:
            subscriber = kwds["cursor"]
            kwds.pop("cursor")

        # Query
        self.query = query
        Search.__init__(self, query=query, api='ScopusSearch', refresh=refresh,
                        count=count, cursor=subscriber, view=view,
                        download=download, verbose=verbose, **kwds)
        self.integrity = integrity_fields or []
        self.action = integrity_action

    def __str__(self):
        """Print a summary string."""
        return make_search_summary(self, "document", self.get_eids())

    def get_eids(self):
        """EIDs of retrieved documents."""
        return [d['eid'] for d in self._json]


def _deduplicate(lst):
    """Auxiliary function to deduplicate lst."""
    out = []
    for i in lst:
        if i not in out:
            out.append(i)
    return out


def _join(item, key, sep=";"):
    """Auxiliary function to join same elements of a list of dictionaries if
    the elements are not None.
    """
    try:
        return sep.join([d[key] or "" for d in item["affiliation"]])
    except (KeyError, TypeError):
        return None


def _replace_none(lst, repl=""):
    """Auxiliary function to replace None's with another value."""
    return ['' if v is None else v for v in lst]
