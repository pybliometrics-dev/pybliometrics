import warnings
from collections import namedtuple

from scopus.classes import Search


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
        """A list of namedtuples in the form (eid doi pii title subtype
        creator authname authid afid coverDate coverDisplayDate
        publicationName issn source_id aggregationType volume issueIdentifier
        pageRange citedby_count openaccess).
        Field definitions correspond to
        https://dev.elsevier.com/guides/ScopusSearchViews.htm, except for
        authname, authid and afid:  These are the ;-joined names resp. Scopus
        IDs resp. Affiliation IDs of the authors of the document.  In case
        the author has multiple affiliations, they are joined on "-".
        """
        out = []
        fields = 'eid doi pii title subtype creator authname authid afid '\
                 'coverDate coverDisplayDate publicationName issn source_id '\
                 'aggregationType volume issueIdentifier pageRange '\
                 'citedby_count openaccess'
        doc = namedtuple('Document', fields)
        for item in self._json:
            try:
                # Deduplicate list of authors
                authors = []
                for i in item['author']:
                    if i not in authors:
                        authors.append(i)
                # Extract information
                authname = ";".join([d['authname'] for d in authors])
                authid = ";".join([d['authid'] for d in authors])
                affs = []
                for auth in authors:
                    aff = auth.get('afid', [])
                    if not isinstance(aff, list):
                        aff = [aff]
                    affs.append('-'.join([d['$'] for d in aff]))
                afid = ';'.join(affs)
                if afid == "":
                    afid = None
            except KeyError:
                authname = None
                authid = None
                afid = None
            date = item.get('prism:coverDate')
            if isinstance(date, list):
                date = date[0].get('$')
            new = doc(eid=item['eid'], doi=item.get('prism:doi'),
                      pii=item.get('pii'), title=item.get('dc:title'),
                      subtype=item.get('subtype'), issn=item.get('prism:issn'),
                      creator=item.get('dc:creator'), authname=authname,
                      coverDate=date, volume=item.get('prism:volume'),
                      coverDisplayDate=item.get('prism:coverDisplayDate'),
                      publicationName=item.get('prism:publicationName'),
                      source_id=item.get('source-id'), authid=authid,
                      aggregationType=item.get('prism:aggregationType'),
                      issueIdentifier=item.get('prism:issueIdentifier'),
                      pageRange=item.get('prism:pageRange'), afid=afid,
                      citedby_count=item.get('citedby-count'),
                      openaccess=item.get('openaccess'))
            out.append(new)
        return out

    def __init__(self, query, refresh=False):
        """Class to search a query, and retrieve a list of EIDs as results.

        Parameters
        ----------
        query : str
            A string of the query.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file if it exists or not.

        Raises
        ------
        ScopusQueryError
            If the number of search results exceeds 5000.

        Notes
        -----
        Json results are cached in ~/.scopus/scopus_search/{fname},
        where fname is the md5-hashed version of query.

        The COMPLETE view is used to access more fields, see
        https://dev.elsevier.com/guides/ScopusSearchViews.htm.
        """

        self.query = query
        Search.__init__(self, query, 'ScopusSearch', refresh,
                        max_entries=5000, count=25, start=0, view='COMPLETE')

    def __str__(self):
        eids = self.get_eids()
        s = """Search {} yielded {} document(s):\n    {}"""
        return s.format(self.query, len(eids), '\n    '.join(eids))

    def get_eids(self):
        """EIDs of retrieved documents."""
        return [d['eid'] for d in self._json]
