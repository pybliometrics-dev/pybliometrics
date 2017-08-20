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


SCOPUS_API_FILE = os.path.expanduser("~/.scopus/my_scopus.py")
try:
    with open(SCOPUS_API_FILE) as f:
        exec(f.read(), globals())
except:
    raise Exception('No API key found. Please create {} it and define '
                    'variable MY_API_KEY in it.'.format(SCOPUS_API_FILE))
