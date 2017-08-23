from pbr.version import VersionInfo

_v = VersionInfo('scopus').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()

from scopus.utils import *

from scopus.scopus_affiliation import *
from scopus.scopus_affiliation import *
from scopus.scopus_author import *
from scopus.scopus_reports import *
from scopus.scopus_search import *
