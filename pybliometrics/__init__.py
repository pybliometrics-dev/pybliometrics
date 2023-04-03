import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import version
else:
    from importlib_metadata import version

__version__ = version("pybliometrics")

__citation__ = 'Rose, Michael E. and John R. Kitchin: "pybliometrics: '\
    'Scriptable bibliometrics using a Python interface to Scopus", SoftwareX '\
    '10 (2019) 100263.'

import pybliometrics.scopus
