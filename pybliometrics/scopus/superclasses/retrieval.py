"""Superclass to access all Scopus retrieval APIs and dump the results."""

from os.path import join

from pybliometrics.scopus.superclasses import Base
from pybliometrics.scopus.utils import RETRIEVAL_URL, get_folder


class Retrieval(Base):
    def __init__(self, identifier, api, refresh, view, id_type=None,
                 date=None):
        """Class intended as superclass to perform retrievals.

        Parameters
        ----------
        identifier : str or int
            A string of the query.

        api : str
            The name of the Scopus API to be accessed.  Allowed values:
            AbstractRetrieval, AuthorRetrieval, CitationOverview,
            ContentAffiliationRetrieval.

        refresh : bool or int
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        view : str
            The view of the file that should be downloaded.

        id_type : str (optional, default=None)
            The type of used ID.
            Note: Will only take effect for the AbstractRetrieval API.

        date : str (optional, default=None)
            A string combining two years with a hyphen for which citations
            should be looked up for.
            Note: Will only take effect for the CitationOverview API.

        Raises
        ------
        ValueError
            If the api parameter or view parameter is an invalid entry.
        """
        # Checks
        if api not in RETRIEVAL_URL:
            raise ValueError('api parameter must be one of ' +
                             ', '.join(RETRIEVAL_URL.keys()))

        # Construct parameters
        url = RETRIEVAL_URL[api]
        if api in ("AbstractRetrieval", "PlumXMetrics"):
            url += id_type + "/"
        params = {'view': view}
        if api == 'CitationOverview':
            params.update({'date': date, 'scopus_id': identifier.split('0-')[-1]})
        url += identifier

        # Parse file contents
        qfile = join(get_folder(api, view), identifier.replace('/', '_'))
        Base.__init__(self, qfile, refresh, params=params, url=url)
        # print(self._json)
        self._view = view
