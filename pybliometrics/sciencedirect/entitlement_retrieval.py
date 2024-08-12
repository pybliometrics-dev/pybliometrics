from typing import List, NamedTuple, Optional, Tuple, Union
from pybliometrics.scopus.utils import check_parameter_value, detect_id_type, VIEWS
from pybliometrics.scopus.superclasses import Retrieval


class EntitlementRetrieval(Retrieval):
    def __init__(self,
                 identifier: Union[int, str] = None,
                 refresh: Union[bool, int] = False,
                 view: str = 'FULL',
                 id_type: str = None,
                 **kwds: str
                 ):
        """Interaction with the Article Entitlement API.
        
        :param identifier: The indentifier of an article."""
        identifier = str(identifier)
        check_parameter_value(view, VIEWS['EntitlementRetrieval'], "view")
        if id_type is None:
            id_type = detect_id_type(identifier)
        else:
            allowed_id_types = ('eid', 'pii', 'scopus_id', 'pubmed_id', 'doi', 'pui')
            check_parameter_value(id_type, allowed_id_types, "id_type")

        self._view = view
        self._refresh = refresh

        Retrieval.__init__(
            self,
            identifier=identifier,
            id_type=id_type,
            api="EntitlementRetrieval",
            **kwds
        )

        self._json = self._json['abstracts-retrieval-response']
