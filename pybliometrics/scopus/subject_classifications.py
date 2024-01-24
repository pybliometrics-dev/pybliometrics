from collections import namedtuple
from typing import Dict, List, NamedTuple, Optional, Tuple, Union

from pybliometrics.scopus.superclasses import Search
from pybliometrics.scopus.utils import chained_get, make_search_summary


class SubjectClassifications(Search):
    @property
    def results(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing results of subject
        classifications search in the form `(code, description, detail, abbrev)`.
        """
        out = []
        path = ['subject-classifications', 'subject-classification']
        search_results = chained_get(self._json, path, [])
        subj = namedtuple('Subject', self.fields)
        if isinstance(search_results, dict):
            for field_name in self.fields:
                if field_name not in search_results:
                    search_results[field_name] = None
            out.append(subj(**search_results))
        else:
            for result in search_results:
                missing_fields = set(self.fields).difference(result.keys())
                if missing_fields:
                    for field_name in missing_fields:
                        result[field_name] = None
                out.append(subj(**result))
        return out or None

    def __init__(self,
                 query: Dict,
                 refresh: Union[bool, int] = False,
                 fields: Union[List[str], Tuple[str, ...]] = None,
                 **kwds: str
                 ) -> None:
        """Interaction with the Subject Classifications Scopus API.

        :param query: Query parameters and corresponding fields. Allowed keys
                      `'code'`, `'abbrev'`, `'description'`, `'detail'`. For more
                      details on search fields please refer to
                      https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl#d1e199.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param fields: The fields to return when calling search results.
                       Allowed values: `'code'`, `'abbrev'`, `'description'`,
                       `'detail'`.  For details see
                       https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl#d1e199.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl.

        Raises
        ------
        TypeError
            If returned fields are not passed in an iterable container.

        ValueError
            If any of the parameters `fields`, `refresh` or `query` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/{fname}`,
        where `path` is specified in your configuration file, and `fname` is
        the md5-hashed version of `query` dict turned into string in format
        of `'key=value'` delimited by `'&'`.
        """
        # Checks
        allowed_query_keys = ('code', 'description', 'detail', 'abbrev')
        invalid = [k for k in query.keys() if k not in allowed_query_keys]
        if invalid:
            raise ValueError(f'Query key(s) "{", ".join(invalid)}" invalid.')
        self.fields = fields or allowed_query_keys
        if fields:
            try:
                return_fields = [i for i in fields]
            except TypeError:
                print("Fields must be iterable")
                raise
            if not set(return_fields).issubset(allowed_query_keys):
                raise ValueError("Parameter 'fields' must be one of " +
                                 f"{', '.join(allowed_query_keys)}.")

        # Query
        query['field'] = ','.join(self.fields)
        self._refresh = refresh
        self._query = str(query)
        self._view = ''
        Search.__init__(self, query=query, api='SubjectClassifications', **kwds)
        path = ['subject-classifications', 'subject-classification']
        self._n = len(chained_get(self._json, path, []))

    def __str__(self):
        """Print a summary string."""
        areas = [r.code for r in self.results]
        return make_search_summary(self, "subject area", areas)
