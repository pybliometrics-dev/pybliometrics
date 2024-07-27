from collections import namedtuple
from datetime import datetime
from hashlib import md5
from typing import List, NamedTuple, Optional, Tuple, Union
from warnings import warn

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import chained_get, check_parameter_value


class CitationOverview(Retrieval):
    @property
    def authors(self) -> Optional[List[Optional[NamedTuple]]]:
        """A list of lists of namedtuples storing author information,
        where each namedtuple corresponds to one author and each sub-list to
        one document.
        The information in each namedtuple is `(name surname initials id url)`.
        All entries are strings.
        """
        outer = []
        order = 'name surname initials id url'
        auth = namedtuple('Author', order)
        for doc in self._citeInfoMatrix:
            inner = []
            for author in doc.get('author', []):
                author = {k.split(":", 1)[-1]: v for k, v in author.items()}
                new = auth(name=author.get('index-name'),
                           id=author['authid'],
                           surname=author.get('surname'),
                           initials=author.get('initials'),
                           url=author.get('author-url'))
                inner.append(new)
            outer.append(inner or None)
        return _maybe_return_list(outer)

    @property
    def cc(self) -> List[List[Tuple[int, int]]]:
        """List of lists of tuples of yearly number of citations for specified
        years, where each sub-list corresponds to one document.
        """
        try:
            dates = self._date.split("-")
        except AttributeError:
            current_year = datetime.now().year
            dates = (current_year-2, current_year)
        _years = range(int(dates[0]), int(dates[1])+1)
        outer = []
        for doc in self._citeInfoMatrix:
            try:
                cites = [int(d['$']) for d in doc['cc']]
            except (AttributeError, KeyError, TypeError):  # No citations
                cites = [0]*len(_years)
            outer.append(list(zip(_years, cites)))
        return _maybe_return_list(outer)

    @property
    def citationType_long(self) -> Optional[List[str]]:
        """Type (long version) of the documents (e.g. article, review)."""
        path = ["citationType", "$"]
        out = [chained_get(e, path) for e in self._citeInfoMatrix]
        return _maybe_return_list(out)

    @property
    def citationType_short(self) -> Optional[List[str]]:
        """Type (short version) of the documents (e.g. ar, re)."""
        path = ["citationType", "@code"]
        out = [chained_get(e, path) for e in self._citeInfoMatrix]
        return _maybe_return_list(out)

    @property
    def columnTotal(self) -> int:
        """The yearly number of citations for all documents combined."""
        return [int(d["$"]) for d in self._citeCountHeader["columnTotal"]]

    @property
    def doi(self) -> Optional[List[str]]:
        """Document Object Identifier (DOI) of the documents."""
        out = [e.get('doi') for e in self._identifierlegend]
        return _maybe_return_list(out)

    @property
    def endingPage(self) -> Optional[List[str]]:
        """Ending pages of the documents."""
        out = [e.get('endingPage') for e in self._citeInfoMatrix]
        return _maybe_return_list(out)

    @property
    def grandTotal(self) -> int:
        """The total number of citations of all documents together."""
        return int(self._citeCountHeader["grandTotal"])

    @property
    def h_index(self) -> int:
        """Combined h-index of citations of all the documents."""
        return int(self._data['h-index'])

    @property
    def issn(self) -> Optional[List[Optional[Union[str, Tuple[str, str]]]]]:
        """ISSN of the publishers of the documents.
        Note: If E-ISSN is known to Scopus, this returns both
        ISSN and E-ISSN in random order separated by blank space.
        """
        out = [e.get('issn') for e in self._citeInfoMatrix]
        return _maybe_return_list(out)

    @property
    def issueIdentifier(self) -> Optional[List[Optional[str]]]:
        """Issue numbers of the documents."""
        out = [e.get('issueIdentifier') for e in self._citeInfoMatrix]
        return _maybe_return_list(out)

    @property
    def laterColumnTotal(self) -> int:
        """The total number of citations for all years after the end
        year for all documents combined.
        """
        return int(self._citeCountHeader["laterColumnTotal"])

    @property
    def lcc(self) -> List[int]:
        """Number of citations after the end year of each document."""
        return [int(m['lcc']) for m in self._citeInfoMatrix]

    @property
    def pcc(self) -> int:
        """Number of citations before the start year."""
        return [int(m['pcc']) for m in self._citeInfoMatrix]

    @property
    def pii(self) -> Optional[List[Optional[str]]]:
        """The Publication Item Identifier (PII) of the documents."""
        out = [e.get('pii') for e in self._identifierlegend]
        return _maybe_return_list(out)

    @property
    def prevColumnTotal(self) -> int:
        """The total number of citations for all years before the start
        year for all documents combined.
        """
        return int(self._citeCountHeader["prevColumnTotal"])

    @property
    def rangeColumnTotal(self) -> int:
        """The total number of citations for all specified years for all
        documents combined.
        """
        return int(self._citeCountHeader["rangeColumnTotal"])

    @property
    def rangeCount(self) -> List[int]:
        """Total citation count over the specified year range for
        each document.
        """
        return [int(e['rangeCount']) for e in self._citeInfoMatrix]

    @property
    def rowTotal(self) -> List[int]:
        """Total number of citations (specified and omitted years) for each
        document.
        """
        return [int(e['rowTotal']) for e in self._citeInfoMatrix]

    @property
    def scopus_id(self) -> List[int]:
        """The Scopus ID(s) of the documents.  Might differ from the
        ones provided.
        """
        return [int(e['scopus_id']) for e in self._identifierlegend]

    @property
    def sortTitle(self) -> Optional[List[Optional[str]]]:
        """Name of source the documents are published in (e.g. the Journal)."""
        out = [e.get('sortTitle') for e in self._citeInfoMatrix]
        return _maybe_return_list(out)

    @property
    def startingPage(self) -> Optional[List[Optional[str]]]:
        """Starting page."""
        out = [e.get('startingPage') for e in self._citeInfoMatrix]
        return _maybe_return_list(out)

    @property
    def title(self) -> List[str]:
        """Titles of each document."""
        return [e["title"] for e in self._citeInfoMatrix]

    @property
    def url(self) -> List[str]:
        """URL(s) to Citation Overview API view of each document."""
        return [e["url"] for e in self._citeInfoMatrix]

    @property
    def volume(self) -> Optional[str]:
        """Volume for the abstract."""
        out = [e.get('volume') for e in self._citeInfoMatrix]
        return _maybe_return_list(out)

    def __init__(self,
                 identifier: List[Union[int, str]],
                 date: Optional[str] = None,
                 start: Optional[Union[int, str]] = None,
                 end: Optional[Union[int, str]] = None,
                 id_type: str = "scopus_id",
                 refresh: Union[bool, int] = False,
                 citation: Optional[str] = None,
                 **kwds: str
                 ) -> None:
        """Interaction with the Citation Overview API.

        :param identifier: Up to 25 identifiers for which to look up
                           citations.  Must be Scopus IDs, DOIs, PIIs or
                           Pubmed IDs.
        :param data: Represents the year range for which the citations should be counted.
                     If `None`, Scopus returns data for the current and the previous
                     two years.
        :param start: (deprecated) The first year for which the citation count should
                      be loaded.
        :param end: (deprecated) The last year for which the citation count should be
                    loaded. Defaults to the current year.
        :param id_type: The type of the IDs provided in `identifier`.  Must be
                        one of `"scopus_id", "doi", "pii", "pubmed_id"`.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param citation: Allows for the exclusion of self-citations or those
                         by books.  If `None`, will count all citations.
                         Allowed values: `None, exclude-self, exclude-books`
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/AbstractCitationAPI.wadl.

        Raises
        -----
        ValueError
            If parameter `identifier` contains fewer than 1 or more than
            25 elements.

        ValueError
            If any of the parameters `citation`, `id_type` or `refresh` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/STANDARD/{id}-{citation}-{date}`,
        where `path` is specified in your configuration file, and `id` the
        md5-hashed version of a string joining `identifier` on underscore.

        Your API Key needs to be augmented by Elsevier's Scopus
        Integration Team to access this API.
        """
        # Checks
        allowed = ('scopus_id', 'doi', 'pii', 'pubmed_id')
        check_parameter_value(id_type, allowed, "id_type")
        if citation:
            allowed = ('exclude-self', 'exclude-books')
            check_parameter_value(citation, allowed, "citation")
        if len(identifier) < 0 or len(identifier) > 25:
            msg = "Provide at least 1 and at most than 25 identifiers"
            raise ValueError(msg)

        # Variables
        identifier = [str(i) for i in identifier]
        if start or end:
            msg = "Parameters `start` and `end` are deprecated and will be removed"\
                  f" in a future release.  Please use 'date={start}-{end}' instead."
            warn(msg, FutureWarning)
            if not date:
                date = f'{start}-{end}'
        self._date = date
        self._citation = citation
        self._refresh = refresh
        self._view = "STANDARD"

        # Get file content
        kwds.update({id_type: identifier})
        stem = md5("_".join(identifier).encode('utf8')).hexdigest()
        Retrieval.__init__(self, stem, api='CitationOverview', date=date,
                           citation=citation, **kwds)
        self._data = self._json['abstract-citations-response']

        # citeInfoMatrix
        matrix = self._data['citeInfoMatrix']['citeInfoMatrixXML']['citationMatrix']['citeInfo']
        self._citeInfoMatrix = [_parse_dict(e) for e in matrix]
        # identifier-legend
        identifier = self._data['identifier-legend']['identifier']
        self._identifierlegend = [_parse_dict(e) for e in identifier]
        # citeCountHeader
        self._citeCountHeader = self._data['citeColumnTotalXML']["citeCountHeader"]

    def __str__(self):
        """Return a summary string."""
        cits_dict = {'exclude-self': 'excluding self-citations',
                     'exclude-books': 'excluding citations from books'}
        date = self.get_cache_file_mdate().split()[0]
        cits_type = f'{cits_dict.get(self._citation, "")}'
        s = f"{len(self.scopus_id)} document(s) has/have the following "\
            f"total citation count{cits_type} as of {date}:\n    "\
            f"{'; '.join([str(n) for n in self.rowTotal])}"
        return s


def _parse_dict(dct):
    """Auxiliary function to change the keys of a dictionary."""
    return {k.split(":", 1)[-1]: v for k, v in dct.items()}


def _maybe_return_list(lst):
    """Return `lst` unless all of its elements are empty."""
    if all(e is None for e in lst):
        return None
    else:
        return lst
