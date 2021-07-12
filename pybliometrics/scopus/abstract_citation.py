from collections import namedtuple
from datetime import datetime
from typing import List, NamedTuple, Optional, Tuple, Union

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import check_parameter_value


class CitationOverview(Retrieval):
    @property
    def authors(self) -> List[NamedTuple]:
        """A list of namedtuples storing author information,
        where each namedtuple corresponds to one author.
        The information in each namedtuple is (name surname initials id url).
        All entries are strings.
        """
        out = []
        order = 'name surname initials id url'
        auth = namedtuple('Author', order)
        for author in self._citeInfoMatrix.get('author'):
            author = {k.split(":", 1)[-1]: v for k, v in author.items()}
            new = auth(name=author.get('index-name'), id=author.get('authid'),
                       surname=author.get('surname'),
                       initials=author.get('initials'),
                       url=author.get('author-url'))
            out.append(new)
        return out or None

    @property
    def cc(self) -> List[Tuple]:
        """List of tuples of yearly number of citations
        for specified years."""
        _years = range(self._start, self._end+1)
        try:
            return list(zip(_years, [d.get('$') for d in self._citeInfoMatrix['cc']]))
        except AttributeError:  # No citations
            return list(zip(_years, [0]*len(_years)))

    @property
    def citationType_long(self) -> str:
        """Type (long version) of the abstract (e.g. article, review)."""
        return self._citeInfoMatrix.get('citationType', {}).get('$')

    @property
    def citationType_short(self) -> str:
        """Type (short version) of the abstract (e.g. ar, re)."""
        return self._citeInfoMatrix.get('citationType', {}).get('@code')

    @property
    def doi(self) -> Optional[str]:
        """Document Object Identifier (DOI) of the abstract."""
        return self._identifierlegend.get('doi')

    @property
    def endingPage(self) -> Optional[str]:
        """Ending page."""
        return self._citeInfoMatrix.get('endingPage')

    @property
    def h_index(self) -> str:
        """h-index of ciations of the abstract (according to Scopus)."""
        return self._data['h-index']

    @property
    def issn(self) -> Optional[Union[str, Tuple[str, str]]]:
        """ISSN of the publisher.
        Note: If E-ISSN is known to Scopus, this returns both
        ISSN and E-ISSN in random order separated by blank space.
        """
        return self._citeInfoMatrix.get('issn')

    @property
    def issueIdentifier(self) -> Optional[str]:
        """Issue number for abstract."""
        return self._citeInfoMatrix.get('issueIdentifier')

    @property
    def lcc(self) -> str:
        """Number of citations the abstract received
        after the specified end year.
        """
        return self._citeInfoMatrix.get('lcc')

    @property
    def pcc(self) -> str:
        """Number of citations the abstract received
        before the specified start year.
        """
        return self._citeInfoMatrix.get('pcc')

    @property
    def pii(self) -> Optional[str]:
        """The Publication Item Identifier (PII) of the abstract."""
        return self._identifierlegend.get('pii')

    @property
    def publicationName(self) -> str:
        """Name of source the abstract is published in (e.g. the Journal)."""
        return self._citeInfoMatrix.get('publicationName')

    @property
    def scopus_id(self) -> str:
        """The Scopus ID of the abstract.  It is the second part of an EID.
        The Scopus ID might differ from the one provided.
        """
        return self._identifierlegend.get('scopus_id')

    @property
    def startingPage(self) -> Optional[str]:
        """Starting page."""
        return self._citeInfoMatrix.get('startingPage')

    @property
    def rangeCount(self) -> Optional[str]:
        """Number of citations for specified years."""
        return self._citeInfoMatrix.get('rangeCount')

    @property
    def rowTotal(self) -> Optional[str]:
        """Number of citations (specified and omitted years)."""
        return self._citeInfoMatrix.get('rowTotal')

    @property
    def title(self) -> str:
        """Abstract title."""
        return self._citeInfoMatrix.get('title')

    @property
    def url(self) -> str:
        """URL to Citation Overview API view of the abstract."""
        return self._citeInfoMatrix.get('url')

    @property
    def volume(self) -> Optional[str]:
        """Volume for the abstract."""
        return self._citeInfoMatrix.get('volume')

    def __init__(self,
                 eid: str,
                 start: Union[int, str],
                 end: Union[int, str] = datetime.now().year,
                 citation: Optional[str] = None,
                 refresh: Union[bool, int] = False
                 ) -> None:
        """Interaction witht the Citation Overview API.

        :param eid: The EID of the abstract.
        :param start: The first year for which the citation count should
                      be loaded.
        :param end: The last year for which the citation count should be
                    loaded. Defaults to the current year.
        :param citation: Allows for the exclusion of self-citations or those by books.
                         If `None`, will count all citations.
                         Allowed values: None, exclude-self, exclude-books
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.

        Notes
        -----
        The directory for cached results is `{path}/STANDARD/{eid}{citation}`,
        where `path` is specified in your configuration file.

        Your API Key needs to be augmented by Elsevier's Scopus
        Integration Team to access this API.
        """
        # Checks
        if citation:
            allowed = ('exclude-self', 'exclude-books')
            check_parameter_value(citation, allowed, "citation")

        # Variables
        self._start = int(start)
        self._end = int(end)
        self._citation = citation
        self._refresh = refresh
        self._view = "STANDARD"

        # Get file content
        date = f'{start}-{end}'
        Retrieval.__init__(self, eid, api='CitationOverview', date=date,
                           citation=citation)
        self._data = self._json['abstract-citations-response']

        # citeInfoMatrix
        m = self._data['citeInfoMatrix']['citeInfoMatrixXML']['citationMatrix']['citeInfo'][0]
        self._citeInfoMatrix = _parse_dict(m)
        # identifier-legend
        l = self._data['identifier-legend']['identifier'][0]
        self._identifierlegend = _parse_dict(l)
        # citeColumnTotalXML
        self._citeColumnTotalXML = self._data['citeColumnTotalXML']  # not used

    def __str__(self):
        """Return a summary string."""
        cits_dict = {'exclude-self': 'self-citations',
                     'exclude-books': 'citations from books'}
        date = self.get_cache_file_mdate().split()[0]
        authors = [a.name for a in self.authors]
        if len(authors) > 1:
            authors[-1] = " and ".join([authors[-2], authors[-1]])
        cits_type = f'excluding {cits_dict.get(self._citation, "")}'
        s = f"Document '{self.title}' by {', '.join(authors)}\npublished in "\
            f"'{self.publicationName}' has the following citation trajectory "\
            f"{cits_type} as of {date}:\n    Before {self._start} {self.pcc}; "\
            f"{'; '.join([f'{item[0]}: {item[1]}' for item in self.cc])}; "\
            f"After {self._end}: {self.lcc} times "
        return s


def _parse_dict(dct):
    """Auxiliary function to change the keys of a dictionary."""
    return {k.split(":", 1)[-1]: v for k, v in dct.items()}
