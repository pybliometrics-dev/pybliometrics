from collections import OrderedDict

from pybliometrics.scopus.superclasses import Search


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

    def __init__(self, query, refresh=False, count=200, view='ENHANCED'):
        """Interaction with the Serial Title API.

        Parameters
        ----------
        query: dict
            Query parameters. Allowed keys are:
                'date'
                     Represents the date range for filtering info entries in
                     ENHANCED view, with the lowest granularity being year
                     (e.g. '2007-2010' or '2010').
                'field'
                    Represents the name of specific fields that
                    should be returned. One or more fields can
                    be provided, deliminated by comma. The list of fields
                    include all of the fields returned in search results.
                'issn'
                    Represents the source identifier filter. Can be either ISSN
                    or e-ISSN. One or more identifiers can be provided,
                    deliminated by comma.
                'oa'
                    Filter used to specify whether the source titles returned
                    should include Open Access types. It will limit the results
                    based upon Open Access status. Values should be one of:
                        - 'all' - all source titles, regardless of Open Access status.
                        - 'full' - include only FULL Open Access titles.
                        - 'partial' - include only PARTIAL Open Access titles.
                        - 'none' - no FULL or PARTIAL Open Access titles.
                'subj'
                     Represents the SCOPUS subject area abbreviation associated
                     with the content category desired. Values should be one of:
                         - 'AGRI' - Agricultural and Biological Sciences
                         - 'ARTS' - Arts and Humanities
                         - 'BIOC' - Biochemistry, Genetics and Molecular Biology
                         - 'BUSI' - Business, Management and Accounting
                         - 'CENG' - Chemical Engineering
                         - 'CHEM' - Chemistry
                         - 'COMP' - Computer Science
                         - 'DECI' - Decision Sciences
                         - 'DENT' - Dentistry
                         - 'EART' - Earth and Planetary Sciences
                         - 'ECON' - Economics, Econometrics and Finance
                         - 'ENER' - Energy
                         - 'ENGI' - Engineering
                         - 'ENVI' - Environmental Science
                         - 'HEAL' - Health Professions
                         - 'IMMU' - Immunology and Microbiology
                         - 'MATE' - Materials Science
                         - 'MATH' - Mathematics
                         - 'MEDI' - Medicine
                         - 'NEUR' - Neuroscience
                         - 'NURS' - Nursing
                         - 'PHAR' - Pharmacology, Toxicology and Pharmaceutics
                         - 'PHYS' - Physics and Astronomy
                         - 'PSYC' - Psychology
                         - 'SOCI' - Social Sciences
                         - 'VETE' - Veterinary
                         - 'MULT' - Multidisciplinary
                'subjCode'
                    Represents the SCOPUS subject area code associated with the
                    content category desired. One or more subject codes can be
                    provided, deliminated by comma. For full list of possible
                    values see
                    https://api.elsevier.com/content/subject/scopus?httpAccept=text/xml
                'title'
                     Represents a partial or complete serial title. Will
                     match the pattern provided anywhere within the title -
                     no wildcard support is provided.
        
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
            If provided value for a query key is invalid or for non-subscribers,
            if the number of search results exceeds 5000.

        ValueError
            If provided query key is invalid.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{fname}`,
        where `path` is specified in `~/.scopus/config.ini` and fname is
        the md5-hashed version of `query` dict turned into string in format of
        'key=value' deliminated by '&'.
        """
        allowed_query_keys = set(['date', 'field', 'issn',
                                  'oa', 'subj','subjCode',
                                  'title'])
        allowed_views = ('STANDARD', 'ENHANCED', 'CITESCORE')
        if not set(query.keys()).issubset(allowed_query_keys):
            raise ValueError('allowed query keys are: ' + 
                             ', '.join(allowed_query_keys))
        if view not in allowed_views:
            raise ValueError('view parameter must be one of ' +
                             ', '.join(allowed_views))
        Search.__init__(self, query=query, api='SerialSearch',
                        refresh=refresh, count=count, view=view)


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
