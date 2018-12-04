"""Superclass to access all retrieval APIs and dump the results."""

from json import loads
from os.path import join

from scopus import config
from scopus.utils import create_config, get_content

BASE_URL = 'https://api.elsevier.com/content/'
URL = {'AbstractRetrieval': BASE_URL + 'abstract/',
       'AuthorRetrieval': BASE_URL + 'author/author_id/',
       'CitationOverview': BASE_URL + 'abstract/citations/',
       'ContentAffiliationRetrieval': BASE_URL + 'affiliation/affiliation_id/'}


class Retrieval:
    def __init__(self, identifier, api, refresh, id_type=None, view=None,
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

        refresh : bool
            Whether to refresh the cached file if it exists or not.

        id_type : str (optional, default=None)
            The type of used ID.
            Note: Will only take effect for the AbstractRetrieval API.

        view : str (optional, default=None)
            The view of the file that should be downloaded.  Will not take
            effect for already cached files.  Allowed values: STANDARD,
            COMPLETE.
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
        if api not in URL:
            raise ValueError('api parameter must be one of ' +
                             ', '.join(URL.keys()))
        if not config.has_section('Directories'):
            create_config()

        # Construct parameters
        url = URL[api]
        if api == "AbstractRetrieval":
            url += id_type + "/"
        elif api == "AuthorRetrieval":
            view = 'ENHANCED'
        params = {'view': view}
        if api == 'CitationOverview':
            params.update({'date': date, 'scopus_id': identifier.split('0-')[-1]})
        url += identifier

        # Parse file contents
        qfile = join(config.get('Directories', api),
                     identifier.replace('/', '_'))
        res = get_content(qfile, refresh, url=url, accept='json',
                          params=params)
        self._json = loads(res.decode('utf-8'))
