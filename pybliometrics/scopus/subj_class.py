from collections import namedtuple

from pybliometrics.scopus.superclasses import Search


class SubjectClass(Search):
    @property
    def results(self):
        """A list of namedtuples representing results of subject classifications
        search. The number of fields of namedtuples are specified during class
        initialization. Note: can be empty if no results are found.
        """
        out = []
        subj = namedtuple('Subject', self.fields)
        search_results = self._json['subject-classifications'].get(
                'subject-classification', []
                )
        if isinstance(search_results, dict):
            for field_name in self.fields:
                if not field_name in search_results:
                    search_results[field_name] = None
            out.append(subj(**search_results))                
        else:            
            for result in search_results:
                missing_fields = set(self.fields).difference(set(result.keys()))
                if missing_fields:
                    for field_name in missing_fields:
                        result[field_name] = None
                out.append(subj(**result))
        return out or None
        
    def __init__(self, query, fields=None, refresh=False):
        """Interaction with the Subject Classifications Scopus API.

        Parameters
        ----------
        query: dict
            Query parameters and corresponding fields. Allowed keys 'code',
            'abbrev', 'description', 'detail'. For more details on search fields
            please refer to
            https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl#d1e199.
        
        fields : iterable (optional, default=None)
            The fields to return when calling search results. Allowed values:
            'code', 'abbrev', 'description', 'detail'.  For details see
            https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl#d1e199.
        
        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        Raises
        ------
        ValueError
            If query or return fields contain invalid fields.
        
        TypeError
            If returned fields are not passed in an iterable container.     

        Notes
        -----
        The directory for cached results is `{path}/STANDARD/{fname}`,
        where `path` is specified in `~/.scopus/config.ini` and fname is
        the md5-hashed version of `query` dict turned into string in format
        of 'key=value' delimited by '&'.
        """
        # Checks
        allowed_query_keys = ('code', 'description', 'detail', 'abbrev')
        invalid = [k for k in query.keys() if k not in allowed_query_keys]
        if invalid:
            raise ValueError(f'Query key(s) "{", ".join(invalid)}" invalid')
        self.fields = allowed_query_keys
        if fields:
            try:
                return_fields = [i for i in fields]
            except TypeError:
                print("Fields must be iterable")
                raise
            if not set(return_fields).issubset(set(allowed_query_keys)):
                raise ValueError('Returned fields can only be '
                                 + str(allowed_query_keys))
            self.fields = fields
        
        # Query
        query['field'] = ','.join(self.fields)
        self.query = str(query)
        Search.__init__(self, query=query, api='SubjectClass', refresh=refresh)
