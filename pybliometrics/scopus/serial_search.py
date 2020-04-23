from collections import namedtuple

from pybliometrics.scopus.superclasses import Search


class SerialSearch(Search):
    def __init__(self, query, refresh=False, download=True, count=200,
                 verbose=False, view='STANDARD'):
        Search.__init__(self, query=query, api='SerialSearch',
                        refresh=refresh, download=download, count=count,
                        verbose=verbose, view=view)