from collections import OrderedDict

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import make_search_summary


class SerialSearch(Search):
    @property
    def results(self):
        """A list of OrderedDicts representing results of serial search. The
        number of keys may vary from one search result to another depending
        on the length of yearly data. Note: can be empty.
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

    def __init__(self, query, refresh=False, view='ENHANCED'):
        """Interaction with the Serial Title API.

        Parameters
        ----------
        query: dict
            Query parameters and corresponding fields. Allowed keys 'title',
            'issn', 'pub', 'subj', 'subjCode', 'content', 'oa'.  For
            examples on possible values, please refer to
            https://dev.elsevier.com/documentation/SerialTitleAPI.wadl#d1e22.
        
        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        view : str (optional, default="ENHANCED")
            The view of the file that should be downloaded.  Allowed values:
            STANDARD, ENHANCED, CITESCORE.  For details see
            https://dev.elsevier.com/guides/SerialTitleViews.htm.

        Raises
        ------
        Scopus400Error
            If provided value for a query key is invalid or if for
            non-subscribers the number of search results exceeds 5000.

        ValueError
            If view parameter is not one of allowed ones or if query contains
            invalid fields.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/SerialSearch.html.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{fname}`,
        where `path` is specified in `~/.scopus/config.ini` and fname is
        the md5-hashed version of `query` dict turned into string in format
        of 'key=value' delimited by '&'.
        """
        # Checks
        allowed_query_keys = ('title', 'issn', 'date', 'pub', 'subj',
                              'subjCode', 'content', 'oa')
        invalid = [k for k in query.keys() if k not in allowed_query_keys]
        if invalid:
            raise ValueError(f'Query key(s) "{", ".join(invalid)}" invalid')
        allowed_views = ('STANDARD', 'ENHANCED', 'CITESCORE')
        if view not in allowed_views:
            raise ValueError('view parameter must be one of ' +
                             ', '.join(allowed_views))

        # Query
        self.query = str(query)
        Search.__init__(self, query=query, api='SerialSearch',
                        refresh=refresh, view=view)
        self._n = len(self._json['serial-metadata-response'].get('entry', []))

    def __str__(self):
        """Print a summary string."""
        titles = [d['title'] for d in self.results]
        return make_search_summary(self, "source", titles)


def _merge_subject_data(subject_area_data):
    """Auxiliary function to collect and concatenate subject area data into string.
    
    Returns tuple of strings for subject area names, subject area codes and
    subject area abbreviations deliminated by ';'.
    """
    codes = set([j.get('@code') for j in subject_area_data if j.get('@code')])
    abbrevs = set([j.get('@abbrev')
                   for j in subject_area_data
                   if j.get('@abbrev')])
    names = set([j.get('$')
                 for j in subject_area_data
                 if j.get('$')])
    return (';'.join(codes), ';'.join(abbrevs), ';'.join(names))


def _retrieve_links(link_data):
    """Auxiliary function to collect data on links.
    
    Returns list of lists in the form of [linkname, link].
    """
    out = []
    for l in link_data:
        if l.get('@ref'):
            out.append([l['@ref'], l.get('@href')])
    return out or None


def _retrieve_yearly_data(yearly_data):
    """Auxiliary function to collect yearly data.
    
    Returns list of lists in the form [mergedstatname, stat], where
    mergedstatname - dictionary key joined with associated period.
    """
    out = []
    for t in yearly_data:
        for key in t:
            if key not in ('@year', '@_fa'):
                out.append([key + '_' + str(t.get('@year')), t[key]])
    return out or None


def _retrieve_cite_scores(cite_score_data):
    """Auxiliary function to collect citescore data.
    
    Returns list of lists in the form [mergedstatname, stat], where
    mergedstatname - dictionary key joined with associated period.
    """
    out = []
    if cite_score_data.get('citeScoreTracker'):
        tracker_year = ('citeScoreTracker'
                        + '_'
                        + str(cite_score_data.get('citeScoreTrackerYear')))
        tracker_val = cite_score_data['citeScoreTracker']
        out.append([tracker_year, tracker_val])
    if cite_score_data.get('citeScoreCurrentMetric'):
        metric_year = ('citeScoreCurrentMetric'
                       + '_'
                       + str(cite_score_data.get('citeScoreCurrentMetricYear')))
        metric_val = cite_score_data.get('citeScoreCurrentMetric')
        out.append([metric_year, metric_val])
    return out or None


def _retrieve_source_rankings(source_data):
    """Auxiliary function to collect SNIP and SJR data.
    
    Returns list of lists in the form [mergedstatname, stat],
    where mergedstatname - dictionary key joined with associated period
    """
    out = []
    for key in source_data:
        stats = source_data[key]
        for t in stats:
            stat_name = str(key + '_' + t.get('@year'))
            stat_val = t.get('$')
            out.append([stat_name, stat_val])
    return out or None
