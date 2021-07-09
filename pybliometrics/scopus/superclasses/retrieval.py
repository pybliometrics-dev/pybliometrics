"""Superclass to access all Scopus retrieval APIs and dump the results."""

from pybliometrics.scopus.superclasses import Base
from pybliometrics.scopus.utils import get_folder, URLS


class Retrieval(Base):
    def __init__(self, identifier, api, id_type=None, date=None, **kwds):
        """Class intended as superclass to perform retrievals.

        Parameters
        ----------
        identifier : str or int
            A string of the query.

        api : str
            The name of the Scopus API to be accessed.  Allowed values:
            AbstractRetrieval, AuthorRetrieval, CitationOverview,
            AffiliationRetrieval.

        id_type : str (optional, default=None)
            The type of used ID.
            Note: Will only take effect for the AbstractRetrieval API.

        date : str (optional, default=None)
            A string specifying a year or range of years (combining two
            years with a hyphen) for which either citations or yearly
            metric data (SJR, SNIP, yearly-data) should be looked up for.
            Note: Will only take effect for the CitationOverview and
            SerialTitle APIs.

        kwds : key-value parings, optional
            Keywords passed on to requests header.  Must contain fields
            and values specified in the respective API specification.

        Raises
        ------
        KeyError
            If the api parameter is an invalid entry.
        """
        # Construct parameters
        url = URLS[api]
        stem = identifier.replace('/', '_')
        if api in ("AbstractRetrieval", "PlumXMetrics"):
            url += id_type + "/"
        params = {'view': self._view, **kwds}
        if api == 'CitationOverview':
            params.update({'date': date, 'citation': self._citation,
                           'scopus_id': identifier.split('0-')[-1]})
            stem += self._citation or ""
        if api == 'SerialTitle':
            params.update({'date': date})
        url += identifier

        # Parse file contents
        self._cache_file_path = get_folder(api, self._view)/stem
        Base.__init__(self, params=params, url=url, api=api)
