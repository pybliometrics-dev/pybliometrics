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
with open(SCOPUS_API_FILE, "a+") as f:
    f.seek(0)
    exec(f.read(), globals())
    if "MY_API_KEY" not in globals():
        prompt = ("No API key deteced. Please enter a valid API Key "
                  "obtained from http://dev.elsevier.com/myapikey.html: \n")
        if version_info >= (3, 0):
            key = input(prompt)
        else:
            key = raw_input(prompt)
        f.write('MY_API_KEY = "{}"'.format(key))
