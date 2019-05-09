from pbr.version import VersionInfo

_v = VersionInfo('scopus').semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()

__citation__ = 'Rose, Michael E. and John R. Kitchin (2019): "scopus: '\
    'Scriptable bibliometrics using a Python interface to Scopus", Max Planck'\
    'Institute for Innovation and Competition Research Paper No. 19-03.'

from scopus.utils import *

from scopus.abstract_citations import *
from scopus.abstract_retrieval import *
from scopus.affiliation_retrieval import *
from scopus.affiliation_search import *
from scopus.author_retrieval import *
from scopus.author_search import *
from scopus.scopus_search import *
from scopus.serial_title import *
from scopus.deprecated_ import *
