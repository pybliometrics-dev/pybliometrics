from importlib.metadata import version

__version__ = version("pybliometrics")

__citation__ = 'Rose, Michael E. and John R. Kitchin: "pybliometrics: '\
    'Scriptable bibliometrics using a Python interface to Scopus", SoftwareX '\
    '10 (2019) 100263.'

import pybliometrics.scopus
import pybliometrics.sciencedirect
from pybliometrics.utils.startup import init
