from pbr.version import VersionInfo

_v = VersionInfo('scopus').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()

from scopus.utils import *

from scopus.abstract_citations import *
from scopus.abstract_retrieval import *
from scopus.affiliation_retrieval import *
from scopus.affiliation_search import *
from scopus.author_retrieval import *
from scopus.author_search import *
from scopus.scopus_affiliation import *
from scopus.scopus_author import *
from scopus.scopus_reports import *
from scopus.scopus_search import *
