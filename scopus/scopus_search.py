import warnings
from collections import namedtuple

from scopus.classes import Search
from scopus.utils import listify


class ScopusSearch(Search):
    @property
    def EIDS(self):
        """Outdated property, will be removed in a future release.  Please use
        get_eids() instead.  For details see
        https://scopus.readthedocs.io/en/latest/tips.html#migration-guide-to-0-x-to-1-x.
        """
        text = "Outdated property, will be removed in a future release.  "\
               "Please use get_eids() instead.  For details see "\
               "https://scopus.readthedocs.io/en/latest/tips.html#"\
               "migration-guide-to-0-x-to-1-x."
        warnings.warn(text, DeprecationWarning)
        return self.get_eids()

    @property
    def results(self):
        """A list of namedtuples in the form (eid doi pii pubmed_id title
        subtype creator afid affilname affiliation_city affiliation_country
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

        Notes
        -----
        The list of authors and the list of affiliations per author are
        deduplicated.
        """
        out = []
        fields = 'eid doi pii pubmed_id title subtype creator afid affilname '\
                 'affiliation_city affiliation_country author_count '\
                 'author_names author_ids author_afids coverDate '\
                 'coverDisplayDate publicationName issn source_id eIssn '\
                 'aggregationType volume issueIdentifier article_number '\
                 'pageRange description authkeywords citedby_count '\
                 'openaccess fund_acr fund_no fund_sponsor'
        doc = namedtuple('Document', fields)
        for item in self._json:
            info = {}
            # Parse affiliations
            try:
                info["affilname"] = _join(item['affiliation'], 'affilname')
                info["afid"] = _join(item['affiliation'], 'afid')
                info["aff_city"] = _join(item['affiliation'], 'affiliation-city')
                info["aff_country"] = _join(item['affiliation'],
                                            'affiliation-country')
            except KeyError:
                pass
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
                title=item.get('dc:title'), fund_sponsor=item.get('fund-sponsor'),
                subtype=item.get('subtype'), issn=item.get('prism:issn'),
                creator=item.get('dc:creator'), affilname=info.get("affilname"),
                author_names=info.get("auth_names"), doi=item.get('prism:doi'),
                coverDate=date, volume=item.get('prism:volume'),
                coverDisplayDate=item.get('prism:coverDisplayDate'),
                publicationName=item.get('prism:publicationName'),
                source_id=item.get('source-id'), author_ids=info.get("auth_ids"),
                aggregationType=item.get('prism:aggregationType'),
                issueIdentifier=item.get('prism:issueIdentifier'),
                pageRange=item.get('prism:pageRange'),
                author_afids=info.get("auth_afid"), fund_no=item.get('fund-no'),
                affiliation_country=info.get("aff_country"),
                citedby_count=item.get('citedby-count'),
                openaccess=item.get('openaccess'), eIssn=item.get('prism:eIssn'),
                author_count=item.get('author-count', {}).get('$'),
                affiliation_city=info.get("aff_city"), afid=info.get("afid"),
                description=item.get('dc:description'), pii=item.get('pii'),
                authkeywords=item.get('authkeywords'), eid=item['eid'],
                fund_acr=item.get('fund-acr'), pubmed_id=item.get('pubmed-id'))
            out.append(new)
        return out or None

    def __init__(self, query, refresh=False, view="COMPLETE"):
        """Class to search a query, and retrieve a list of EIDs as results.

        Parameters
        ----------
        query : str
            A string of the query.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        view : str (optional, default=COMPLETE)
            Which view to use for the query, see
            https://dev.elsevier.com/guides/ScopusSearchViews.htm.
            Allowed values: STANDARD, COMPLETE.  By default, the COMPLETE view
            is used, which returns more fields but results in a slower query.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds 5000.

        ValueError
            If the view parameter is not one of the allowed ones.

        Notes
        -----
        Json results are cached in ~/.scopus/scopus_search/{fname},
        where fname is the md5-hashed version of query.
        """
        # Checks
        allowed_views = ('STANDARD', 'COMPLETE')
        if view not in allowed_views:
            raise ValueError('view parameter must be one of ' +
                             ', '.join(allowed_views))
        # Query
        self.query = query
        if view == "COMPLETE":
            count = 25
        else:
            count = 200
        Search.__init__(self, query, 'ScopusSearch', refresh, max_entries=5000,
                        count=count, start=0, view=view)

    def __str__(self):
        eids = self.get_eids()
        s = """Search {} yielded {} document(s):\n    {}"""
        return s.format(self.query, len(eids), '\n    '.join(eids))

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


def _join(lst, key, sep=";"):
    """Auxiliary function to join same elements of a list of dictionaries if
    the elements are not None.
    """
    return sep.join([d[key] for d in lst if d[key]])


def _replace_none(lst, repl=""):
    """Auxiliary function to replace None's with another value."""
    return ['' if v is None else v for v in lst]
