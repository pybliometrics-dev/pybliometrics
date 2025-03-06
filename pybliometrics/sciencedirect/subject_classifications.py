"""Module with the class ScDirSubjectClassifications."""
from typing import Optional, Union

from pybliometrics.scopus import SubjectClassifications


class ScDirSubjectClassifications(SubjectClassifications):
    def __init__(self,
                 query: dict,
                 refresh: Union[bool, int] = False,
                 fields: Optional[Union[list[str], tuple[str, ...]]] = None,
                 **kwds: str
                 ) -> None:
        """Interaction with the ScienceDirect Subject Classifications API.

        :param query: Query parameters and corresponding fields. Allowed keys
                      `'code'`, `'abbrev'`, `'description'`, `'detail'`. For more
                      details on search fields please refer to the `documentation 
                      <https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl#d1e199>`__.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param fields: The fields to return when calling search results.
                       Allowed values: `'code'`, `'abbrev'`, `'description'`,
                       `'detail'`.  For details see the `documentation 
                       <https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl#d1e199>`__.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the `API specification 
                     <https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl>`__.

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
        SubjectClassifications.__init__(self, query=query, refresh=refresh, fields=fields, **kwds)
