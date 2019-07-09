from pbr.version import VersionInfo

_v = VersionInfo('pybliometrics').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()

__citation__ = 'Rose, Michael E. and John R. Kitchin: "pybliometrics: '\
    'Scriptable bibliometrics using a Python interface to Scopus", SoftwareX '\
    '10 (2019) 100263.'

import pybliometrics.scopus
