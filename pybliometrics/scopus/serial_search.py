from collections import namedtuple, OrderedDict

from pybliometrics.scopus.superclasses import Search


class SerialSearch(Search):
    @property
    def results(self):
        """A list of namedtuples representing results of serial search. The
        number of fields may vary from one search query to another depending
        on the length of yearly data Note: can be empty.
        """
        out = []
        search_results = self._json['serial-metadata-response'].get('entry')
        if search_results:
            # Namedtuple fields from union of keys of each dictionary in result list
            fields = [_clean_field_name(i) for i in _form_fields(search_results)]
            serial = namedtuple('Serial', fields)
            for i in search_results:
                # OrderedDict to populate with individual serial data
                obs = OrderedDict.fromkeys(fields)
                for key in i:
                    if key != '@_fa' and i[key]:
                        if key == 'subject-area':
                            subject_data = _merge_subject_data(i[key])
                            obs['subject_area_codes'] = subject_data[0]
                            obs['subject_area_abbrevs'] = subject_data[1]
                            obs['subject_area_names'] = subject_data[2]
                        elif key == 'SNIPList' or key == 'SJRList':
                            for j in _retrieve_source_rankings(i[key]):
                                obs[j[0]] = j[1]
                        elif key == 'citeScoreYearInfoList':
                            for j in _retrieve_cite_scores(i[key]):
                                obs[j[0]] = j[1]
                        elif key == 'link':
                            for j in _retrieve_links(i['link']):
                                obs[_clean_field_name(j[0])] = j[1]
                        elif key == 'yearly-data':
                            if i['yearly-data'].get('info'):
                                time_data = _retrieve_yearly_data(i['yearly-data']['info'])
                                for j in time_data:
                                    obs[j[0]] = j[1]
                        else:
                            obs[_clean_field_name(key)] = i[key]
                # Make namedtuple from OrderedDict
                out.append(serial._make(obs.values())) or None
        return out or None

    def __init__(self, query, refresh=False, count=200, verbose=False,
                 view='ENHANCED'):
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
        'key value' deliminated by '&'.
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


def _form_fields(results):
    """Auxiliary function that returns tuple represiting union of keys
    of all dictionaries inside search result list including keys of nested
    dictionaries. Nested dictionaries correspond to links data, citescore
    metric data from last available year, subject area data and other data
    varying by year (e.g.  SNIP and SJR yearly data). Keys of periodic data
    and citescore metrics data are treated by merging stat name and period with
    underscore. If subject area data is present, keys corresponding to area
    code, names and abbreviations are created. Keys of links data are
    created corresponding to link names given by data.
    """
    special_keys = ['@_fa',
                    'subject-area',
                    'SNIPList',
                    'SJRList',
                    'citeScoreYearInfoList',
                    'link',
                    'yearly-data']
    base_fields = set() # Subject area keys, links keys and keys with non-nested dictionaries
    time_fields = set() # SJR, SNIP, citescore and yearly data keys
    for i in results:
        base_fields.update(set(key for key in i if key not in special_keys))
        # Keys from dictionaries of yearly data
        if i.get('yearly-data'):
            yearly_fields = set()
            for t in i['yearly-data'].get('info', []):
                period_fields = set(key
                                    + '_'
                                    + str(t.get('@year'))
                                    for key in t.keys()
                                    if key not in ('@year', '@_fa'))
                yearly_fields.update(period_fields)
            time_fields.update(yearly_fields)
        # Link names
        links = [j['@ref'] for j in i.get('link', []) if j.get('@ref')]
        base_fields.update(set(links))
        if i.get('citeScoreYearInfoList'):
            cite = i['citeScoreYearInfoList']
            if cite.get('citeScoreCurrentMetric'):
                metric = ('citeScoreCurrentMetric'
                          + '_'
                          + str(cite.get('citeScoreCurrentMetricYear')))
                time_fields.add(metric)
            if cite.get('citeScoreTracker'):
                tracker = ('citeScoreTracker'
                           + '_'
                           + str(cite.get('citeScoreTrackerYear')))
                time_fields.add(tracker)
        if i.get('SNIPList'):
            for key in i['SNIPList']:
                snip = i['SNIPList'][key]
                for t in snip:
                    time_fields.add(key + '_' + str(t.get('@year')))
        if i.get('SJRList'):
            for key in i['SJRList']:
                sjr = i['SJRList'][key]
                for t in sjr:
                    time_fields.add(key + '_' + str(t.get('@year')))
        if i.get('subject-area'):
            subject_fields = set(['subject_area_codes',
                                  'subject_area_abbrevs',
                                  'subject_area_names'])
            base_fields.update(subject_fields)
    # Sort time and base fields alphabetically
    return sorted(list(base_fields)) + sorted(list(time_fields))


def _clean_field_name(fieldname):
    """Cleans string for use as namedtuple field"""
    return fieldname.replace(':', '_').replace('-','_').replace('@','')


def _merge_subject_data(subject_area_data):
    """Collects and concatenates data on subject area into string.
    Returns tuple of strings for subject area names, codes and abbreviations
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
    """Collects data on links. Returns list of lists in the form of
    [linkname, link]
    """
    out = []
    for l in link_data:
        if l.get('@ref'):
            out.append([l['@ref'], l.get('@href')])
    return out or None


def _retrieve_yearly_data(yearly_data):
    """Collects yearly data. Returns list of lists in the form 
    [mergedstatname, stat], where mergedstatname - dictionary key joined with
    associated period
    """
    out = []
    for t in yearly_data:
        for key in t:
            if key not in ('@year', '@_fa'):
                out.append([key + '_' + str(t.get('@year')), t[key]])
    return out or None


def _retrieve_cite_scores(cite_score_data):
    """Collects citescore data. Returns list of lists in the form 
    [mergedstatname, stat], where mergedstatname - dictionary key joined with
    associated period
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
    """Collects SNIP and SJR data. Returns list of lists in the form 
    [mergedstatname, stat], where mergedstatname - dictionary key joined with
    associated period
    """
    out = []
    for key in source_data:
        stats = source_data[key]
        for t in stats:
            stat_name = str(key + '_' + t.get('@year'))
            stat_val = t.get('$')
            out.append([stat_name, stat_val])
    return out or None
            