from collections import namedtuple, OrderedDict

from pybliometrics.scopus.superclasses import Search


class SerialSearch(Search):
    @property
    def results(self):
        out = []
        search_results = self._json['serial-metadata-response'].get('entry')   
        if search_results:
            fields = [_clean_field_name(i) for i in _form_fields(search_results)]
            serial = namedtuple('Serial', fields)
            for i in search_results:
                obs = OrderedDict.fromkeys(fields)
                for key in i:
                    if key != '@_fa' and i[key]:
                        if key == 'subject-area':
                            subject_data = _merge_subject_data(i[key])
                            obs['subject_area_codes'] = subject_data[0] or None
                            obs['subject_area_abbrevs'] = subject_data[1] or None
                            obs['subject_area_names'] = subject_data[2] or None
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
                out.append(serial._make(obs.values()))
        return out or None
            
    def __init__(self, query, refresh=False, download=True, count=200,
                 verbose=False, view='STANDARD'):
        Search.__init__(self, query=query, api='SerialSearch',
                        refresh=refresh, download=download, count=count,
                        verbose=verbose, view=view)


def _form_fields(results):
    special_keys = ['@_fa',
                    'subject-area',
                    'SNIPList',
                    'SJRList',
                    'citeScoreYearInfoList',
                    'link',
                    'yearly-data']
    base_fields = set()
    time_fields = set()
    for i in results:
        base_fields.update(set(key for key in i if key not in special_keys))
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
    subject_fields = set(['subject_area_codes',
                          'subject_area_abbrevs',
                          'subject_area_names'])
    base_fields.update(subject_fields)
    return sorted(list(base_fields)) + sorted(list(time_fields))


def _clean_field_name(fieldname):
    return fieldname.replace(':', '_').replace('-','_').replace('@','')


def _merge_subject_data(subject_area_data):
    codes = set([j.get('@code') for j in subject_area_data if j.get('@code')])
    abbrevs = set([j.get('@abbrev')
                   for j in subject_area_data
                   if j.get('@abbrev')])
    names = set([j.get('$')
                 for j in subject_area_data
                 if j.get('$')])
    return (';'.join(codes), ';'.join(abbrevs), ';'.join(names))


def _retrieve_links(link_data):
    out = []
    for l in link_data:
        if l.get('@ref'):
            out.append([l['@ref'], l.get('@href')])
    return out or None


def _retrieve_yearly_data(yearly_data):
    out = []
    for t in yearly_data:
        for key in t:
            if key not in ('@year', '@_fa'):
                out.append([key + '_' + str(t.get('@year')), t[key]])
    return out


def _retrieve_cite_scores(cite_score_data):
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
    out = []
    for key in source_data:
        stats = source_data[key]
        for t in stats:
            stat_name = str(key + '_' + t.get('@year'))
            stat_val = t.get('$')
            out.append([stat_name, stat_val])
    return out or None
            