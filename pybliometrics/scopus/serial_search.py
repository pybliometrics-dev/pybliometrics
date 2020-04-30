from collections import namedtuple, OrderedDict

from pybliometrics.scopus.superclasses import Search


class SerialSearch(Search):
    @property
    def serials(self):
        results = self._json['serial-metadata-response'].get('entry', [])
        discard_fields = ['@_fa',
                  'yearly-data',
                  'SNIPList',
                  'SJRList',
                  'link',
                  'subject-area',
                  'citeScoreYearInfoList']
        fields = _form_fields(results, ignore=discard_fields)
        clean_fields = ' '.join(fields).replace(':', '_').replace('-','_')
        serial = namedtuple('Serial', clean_fields)
        out = []
        for i in results:
            obs = OrderedDict.fromkeys(fields)
            for key in i:
                if key not in discard_fields:
                    obs[key] = i[key]
                elif key == 'subject-area':
                    codes = set([j.get('@code') for j in i[key] if j.get('@code')])
                    obs['subject_area_codes'] = ';'.join(codes)
                    abbrevs = set([j.get('@abbrev')
                                   for j in i[key]
                                   if j.get('@abbrev')])
                    obs['subject_area_abbrevs'] = ';'.join(abbrevs)
                    names = set([j.get('$')
                                 for j in i[key]
                                 if j.get('$')])
                    obs['subject_area_names'] = ';'.join(names)
                elif key == 'link':
                    for l in i[key]:
                        if l.get('@ref'):
                            link_name = l['@ref']
                            obs[link_name] = l.get('@href')
                elif key == 'citeScoreYearInfoList':
                    for score in i[key]:
                        obs[score] = i[key][score]
            out.append(serial._make(obs.values()))
        return out or None
    
    @property
    def yearly_data(self):
        out = []
        fields = set(['source_id'])
        for i in self._json['serial-metadata-response'].get('entry', []):
            if i.get('yearly-data'):
                for t in i.get('yearly-data').get('info', []):
                    fields.update(set(t.keys()))
        fields.remove('@_fa')
        fields = list(fields)
        clean_fields = [i.replace('@', '') for i in fields]
        stat = namedtuple('Data', clean_fields)
        for i in self._json['serial-metadata-response'].get('entry', []):
            if i.get('yearly-data'):
                data = i.get('yearly-data', {}).get('info', [])
                for t in data:
                    obs = OrderedDict.fromkeys(fields)
                    obs['source_id'] = i['source-id']
                    for key in t:
                        if key != '@_fa':
                            obs[key] = t[key]
                    out.append(stat._make(obs.values()))
        return out or None
            
                    
            
    def __init__(self, query, refresh=False, download=True, count=200,
                 verbose=False, view='STANDARD'):
        Search.__init__(self, query=query, api='SerialSearch',
                        refresh=refresh, download=download, count=count,
                        verbose=verbose, view=view)
        
    
def _form_fields(results, ignore=[]):
    fields = set()
    for i in results:
        fields.update(set(i.keys()))
        links = [j.get('@ref') for j in i.get('link', []) if j.get('@ref')]
        fields.update(set(links))
        cite_scores = list(i.get('citeScoreYearInfoList', {}).keys())
        fields.update(set(cite_scores))
    fields.difference_update(set(ignore))
    fields = list(fields)
    fields += ['subject_area_codes', 'subject_area_abbrevs', 'subject_area_names']
    return fields

