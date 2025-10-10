"""Superclass to access all Scopus retrieval APIs and dump the results."""

import hashlib
from pathlib import Path

from pybliometrics.superclasses import Base
from pybliometrics.utils import APIS_NO_ID_IN_URL, APIS_WITH_ID_TYPE, get_config, URLS


class Retrieval(Base):
    def __init__(self,
                 identifier: int | str | None = None,
                 id_type: str | None = None,
                 **kwds: str
                 ) -> None:
        """Class intended as superclass to perform retrievals.

        :param identifier: The ID to look for.
        :param id_type: The type of the used ID.  Will only take effect for
                        the Abstract Retrieval API.
        :param kwds: Keywords passed on to requests header.  Must contain
                     fields and values specified in the respective
                     API specification.

        Raises
        ------
        KeyError
            If parameter `api` is not one of the allowed values.
        """
        api = self.__class__.__name__
        # Construct URL and cache file name
        url = URLS[api]
        if api in APIS_WITH_ID_TYPE:
            url += id_type + "/"
        if api == 'CitationOverview':
            stem = identifier.replace("/", "")
            if self._citation:
                stem += "-" + self._citation
            if self._date:
                stem += "-" + self._date
        # For APIs that don't use ID in URL, hash the parameters for unique cache filename
        elif api in APIS_NO_ID_IN_URL:
            params_str = str(sorted(kwds.items()))
            stem = hashlib.md5(params_str.encode()).hexdigest()
        else:
            url += str(identifier)
            stem = str(identifier).replace('/', '_')
        # Get cache file path
        config = get_config()
        parent = Path(config.get('Directories', api))
        self._cache_file_path = parent/self._view/stem

        # Parse file contents
        params = {'view': self._view, **kwds}
        Base.__init__(self, params=params, url=url)
