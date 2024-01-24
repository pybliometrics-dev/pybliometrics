from collections import OrderedDict
from typing import Dict, List, Optional, Union

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import check_parameter_value, make_search_summary, VIEWS


class SerialSearch(Search):
    @property
    def results(self) -> Optional[List[Dict[str, str]]]:
        """A list of OrderedDicts representing results of serial search. The
        number of keys may vary from one search result to another depending
        on the length of yearly data.
        """
        out = []
        search_results = self._json['serial-metadata-response'].get('entry', [])
        for result in search_results:
            # OrderedDict to populate with individual serial data
            obs = OrderedDict()
            for key, value in result.items():
                if not value:
                    continue
                key = key.split(":", 1)[-1]
                if key == '@_fa':
                    continue
                elif key == 'subject-area':
                    subject_data = _merge_subject_data(value)
                    obs['subject_area_codes'] = subject_data[0]
                    obs['subject_area_abbrevs'] = subject_data[1]
                    obs['subject_area_names'] = subject_data[2]
                elif key == 'SNIPList' or key == 'SJRList':
                    for j in _retrieve_source_rankings(value):
                        obs[j[0]] = j[1]
                elif key == 'citeScoreYearInfoList':
                    for j in _retrieve_cite_scores(value):
                        obs[j[0]] = j[1]
                elif key == 'link':
                    for j in _retrieve_links(value):
                        obs[j[0]] = j[1]
                elif key == 'yearly-data':
                    time_data = _retrieve_yearly_data(value.get('info', []))
                    for j in time_data:
                        obs[j[0]] = j[1]
                else:
                    obs[key] = value
            if obs:
                out.append(obs)
        return out or None

    def __init__(self,
                 query: Dict,
                 refresh: Union[bool, int] = False,
                 view: str = 'ENHANCED',
                 **kwds: str
                 ) -> None:
        """Interaction with the Serial Title API.

        :param query:  Query parameters and corresponding fields. Allowed keys
                      'title', 'issn', 'pub', 'subj', 'subjCode', 'content',
                      'oa'.  For examples on possible values, please refer to
                      https://dev.elsevier.com/documentation/SerialTitleAPI.wadl#d1e22.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: The view of the file that should be downloaded.  Allowed
                     values: `STANDARD`, `ENHANCED`, `CITESCORE`.  For details see
                     https://dev.elsevier.com/sc_serial_title_views.html.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values listed in the API specification at
                     https://dev.elsevier.com/documentation/SerialTitleAPI.wadl.

        Raises
        ------
        Scopus400Error
            If provided value for a query key is invalid or if for
            non-subscribers the number of search results exceeds 5000.

        ValueError
            If any of the parameters `refresh` or `view` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{fname}`,
        where `path` is specified in your configuration file, and `fname` is
        the md5-hashed version of `query` dict turned into string in format
        of `'key=value'` delimited by `'&'`.
        """
        # Checks
        allowed_query_keys = ('title', 'issn', 'date', 'pub', 'subj',
                              'subjCode', 'content', 'oa')
        invalid = [k for k in query.keys() if k not in allowed_query_keys]
        if invalid:
            raise ValueError(f'Query key(s) "{", ".join(invalid)}" invalid')
        check_parameter_value(view, VIEWS['SerialSearch'], "view")

        # Query
        self._query = str(query)
        self._refresh = refresh
        self._view = view
        Search.__init__(self, query=query, api='SerialSearch', **kwds)
        self._n = len(self._json['serial-metadata-response'].get('entry', []))

    def __str__(self):
        """Print a summary string."""
        titles = [d['title'] for d in self.results]
        return make_search_summary(self, "source", titles)


def _merge_subject_data(subject_area_data):
    """Auxiliary function to collect and concatenate subject area data into string.

    Returns tuple of strings for subject area names, subject area codes and
    subject area abbreviations deliminated by `';'`.
    """
    codes = set([j.get('@code') for j in subject_area_data])
    abbrevs = set([j.get('@abbrev') for j in subject_area_data])
    names = set([j.get('$') for j in subject_area_data])
    return (';'.join(filter(None, codes)),
            ';'.join(filter(None, abbrevs)),
            ';'.join(filter(None, names)))


def _retrieve_links(link_data):
    """Auxiliary function to collect data on links.

    Returns list of lists in the form of `[linkname, link]`.
    """
    out = []
    for sl in link_data:
        try:
            out.append([sl['@ref'], sl.get('@href')])
        except KeyError:
            continue
    return out or None


def _retrieve_yearly_data(yearly_data):
    """Auxiliary function to collect yearly data.

    Returns list of lists in the form `[mergedstatname, stat]`, where
    `mergedstatname` - dictionary key joined with associated period.
    """
    out = []
    for t in yearly_data:
        for key in t:
            if key not in ('@year', '@_fa'):
                out.append([f"{key}_{t['@year']}", t[key]])
    return out or None


def _retrieve_cite_scores(cite_score_data):
    """Auxiliary function to collect citescore data.

    Returns list of lists in the form `[mergedstatname, stat]`, where
    `mergedstatname` - dictionary key joined with associated period.
    """
    out = []
    for key in ("citeScoreTracker", "citeScoreCurrentMetric"):
        try:
            year = f"{key}_{cite_score_data[key + 'Year']}"
            val = cite_score_data[key]
            out.append([year, val])
        except KeyError:
            pass
    return out or None


def _retrieve_source_rankings(source_data):
    """Auxiliary function to collect SNIP and SJR data.

    Returns list of lists in the form `[mergedstatname, stat]`,
    where `mergedstatname` - dictionary key joined with associated period
    """
    out = []
    for key in source_data:
        stats = source_data[key]
        for t in stats:
            out.append([f"{key}_['@year']", t['$']])
    return out or None
