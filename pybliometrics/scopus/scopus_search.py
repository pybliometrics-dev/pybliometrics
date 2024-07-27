from collections import namedtuple
from typing import List, NamedTuple, Optional, Tuple, Union

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import check_integrity, chained_get,\
    check_parameter_value, check_field_consistency, deduplicate,\
    get_freetoread, html_unescape, listify, make_search_summary, VIEWS


class ScopusSearch(Search):
    @property
    def results(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples in the form `(eid doi pii pubmed_id title
        subtype subtypeDescription creator afid affilname affiliation_city
        affiliation_country author_count author_names author_ids author_afids
        coverDate coverDisplayDate publicationName issn source_id eIssn
        aggregationType volume issueIdentifier article_number pageRange
        description authkeywords citedby_count openaccess freetoread
        freetoreadLabel fund_acr fund_no fund_sponsor)`.
        Field definitions correspond to
        https://dev.elsevier.com/guides/ScopusSearchViews.htm and return the
        values as-is, except for `afid`, `affilname`, `affiliation_city`,
        `affiliation_country`, `author_names`, `author_ids` and `author_afids`:  These
        information are joined on `";"`.  In case an author has multiple
        affiliations, they are joined on `"-"`
        (e.g. `Author1Aff;Author2Aff1-Author2Aff2`).

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
        # Initiate namedtuple with ordered list of fields
        fields = 'eid doi pii pubmed_id title subtype subtypeDescription ' \
                 'creator afid affilname affiliation_city ' \
                 'affiliation_country author_count author_names author_ids '\
                 'author_afids coverDate coverDisplayDate publicationName '\
                 'issn source_id eIssn aggregationType volume '\
                 'issueIdentifier article_number pageRange description '\
                 'authkeywords citedby_count openaccess freetoread '\
                 'freetoreadLabel fund_acr fund_no fund_sponsor'
        doc = namedtuple('Document', fields)
        check_field_consistency(self._integrity, fields)
        # Parse elements one-by-one
        out = []
        for item in self._json:
            info = {}
            # Parse affiliations
            for field, key in [('affilname', 'affilname'),
                               ('afid', 'afid'),
                               ('aff_city', 'affiliation-city'),
                               ('aff_country', 'affiliation-country')]:
                info[field] = _join(item, key, unescape=self.unescape)
            # Parse authors
            try:
                # Deduplicate list of authors
                authors = deduplicate(item['author'])
                # Extract information
                surnames = _replace_none([d['surname'] for d in authors])
                firstnames = _replace_none([d['given-name'] for d in authors])
                info["auth_names"] = ";".join([", ".join([t[0], t[1]]) for t in
                                               zip(surnames, firstnames)])
                info["auth_ids"] = ";".join([d['authid'] for d in authors])
                affs = []
                for auth in authors:
                    aff = listify(deduplicate(auth.get('afid', [])))
                    affs.append('-'.join([d['$'] for d in aff]))
                if [a for a in affs if a]:
                    info["auth_afid"] = ';'.join(affs)
                else:
                    info["auth_afid"] = None
            except KeyError:
                pass
            date = item.get('prism:coverDate')
            if isinstance(date, list):
                date = date[0].get('$')
            default = [None, {"$": None}]
            freetoread = get_freetoread(item, ["freetoread", "value"], default)
            freetoreadLabel = get_freetoread(item, ["freetoreadLabel", "value"], default)
            # Get text fields and unescape
            for key in ['dc:title', 'dc:description', 'authkeywords']:
                value = item.get(key)
                info[key] = html_unescape(value) if (self.unescape and value) else value
            new = doc(article_number=item.get('article-number'),
                      title=info.get('dc:title'),
                      fund_no=item.get('fund-no'),
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
                      citedby_count=int(item['citedby-count']),
                      openaccess=int(item['openaccess']),
                      freetoread=freetoread, freetoreadLabel=freetoreadLabel,
                      eIssn=item.get('prism:eIssn'),
                      author_count=item.get('author-count', {}).get('$'),
                      affiliation_city=info.get("aff_city"), afid=info.get("afid"),
                      description=info.get('dc:description'),
                      pii=item.get('pii'),
                      authkeywords=info.get('authkeywords'),
                      eid=item.get('eid'),
                      fund_acr=item.get('fund-acr'), pubmed_id=item.get('pubmed-id'))
            out.append(new)
        # Finalize
        check_integrity(out, self._integrity, self._action)
        return out or None

    def __init__(self,
                 query: str,
                 refresh: Union[bool, int] = False,
                 view: str = None,
                 verbose: bool = False,
                 download: bool = True,
                 integrity_fields: Union[List[str], Tuple[str, ...]] = None,
                 integrity_action: str = "raise",
                 subscriber: bool = True,
                 unescape: bool = True,
                 **kwds: str
                 ) -> None:
        """Interaction with the Scopus Search API.

        :param query: A string of the query as used in the Advanced Search
                     on scopus.com.  All fields except "INDEXTERMS()" and
                     "LIMIT-TO()" work.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: Which view to use for the query, see
                     https://dev.elsevier.com/sc_search_views.html.
                     Allowed values: `STANDARD`, `COMPLETE`.  If `None`, defaults to
                     `COMPLETE` if `subscriber=True` and to `STANDARD` if
                     `subscriber=False`.
        :param verbose: Whether to print a download progress bar.
        :param download: Whether to download results (if they have not been
                         cached).
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
        :param subscriber: Whether you access Scopus with a subscription or not.
                           For subscribers, Scopus's cursor navigation will be
                           used.  Sets the number of entries in each query
                           iteration to the maximum number allowed by the
                           corresponding view.
        :param unescape: Convert named and numeric characters in the `results` to
                        their corresponding Unicode characters.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/ScopusSearchAPI.wadl.

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
        # Checks
        if view:
            check_parameter_value(view, VIEWS['ScopusSearch'], "view")
        allowed = ("warn", "raise")
        check_parameter_value(integrity_action, allowed, "integrity_action")

        # Parameters
        if not view:
            if subscriber:
                view = "COMPLETE"
            else:
                view = "STANDARD"
        size = 25  # for pagination
        if view == "STANDARD" and subscriber:
            size = 200
        if "cursor" in kwds:
            subscriber = kwds["cursor"]
            kwds.pop("cursor")

        # Query
        self._action = integrity_action
        self._integrity = integrity_fields or []
        self._refresh = refresh
        self._query = query
        self._view = view
        Search.__init__(self, query=query, api='ScopusSearch', size=size,
                        cursor=subscriber, download=download,
                        verbose=verbose, **kwds)
        self.unescape = unescape

    def __str__(self):
        """Print a summary string."""
        return make_search_summary(self, "document", self.get_eids())

    def get_eids(self):
        """EIDs of retrieved documents."""
        return [d['eid'] for d in self._json]


def _join(item, key, sep=";", unescape=False):
    """Auxiliary function to join same elements of a list of dictionaries if
    the elements are not None.
    """
    try:
        string = sep.join([d[key] or "" for d in item["affiliation"]])
        return html_unescape(string) if unescape else string
    except (KeyError, TypeError):
        return None


def _replace_none(lst, repl=""):
    """Auxiliary function to replace None's with another value."""
    return [repl if v is None else v for v in lst]
