Scopus Search
-------------

:doc:`ScopusSearch <../reference/scopus.ScopusSearch>` implements the `Scopus Search API <https://api.elsevier.com/documentation/SCOPUSSearchAPI.wadl>`_.  It performs a query to search for articles and then retrieves the records of the query.

The class is initialized with a search query on which you can read about in `Scopus Search Guide <https://dev.elsevier.com/tips/ScopusSearchTips.htm>`_.  Keep in mind that an invalid search query will result in an error.

.. code-block:: python
   
    >>> from scopus import ScopusSearch
    >>> s = ScopusSearch('FIRSTAUTH ( kitchin  j.r. )', refresh=True)


The class' main attribute `results` returns a list of `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_.  They can be used neatly with `pandas <https://pandas.pydata.org/>`_ to form DataFrames:

.. code-block:: python

    >>> import pandas as pd
    >>> res.columns
    Index(['eid', 'doi', 'pii', 'title', 'subtype', 'creator', 'authname',
           'authid', 'afid', 'coverDate', 'coverDisplayDate', 'publicationName',
           'issn', 'source_id', 'aggregationType', 'volume', 'issueIdentifier',
           'pageRange', 'citedby_count', 'openaccess'],
          dtype='object')
    >>> res.shape
    (12, 19)
    >>> res.head()
                      eid                         doi                pii    ...      pageRange citedby_count openaccess
    0  2-s2.0-85019169906   10.1007/s00799-016-0173-7               None    ...          93-98             1          0
    1  2-s2.0-84971324241           10.1002/aic.15294               None    ...      3826-3835             2          0
    2  2-s2.0-84930349644  10.1016/j.susc.2015.05.007  S0039602815001326    ...        103-107             2          0
    3  2-s2.0-84930616647    10.1021/acscatal.5b00538               None    ...      3894-3899             7          1
    4  2-s2.0-67449106405  10.1103/PhysRevB.79.205412               None    ...           None            48          0


The EIDs can be used for the `AbstractRetrieval <../reference/scopus.AbstractRetrieval.html>`_ class and the Scopus Author IDs in column "authid" for the `AuthorRetrieval <../reference/scopus.AuthorRetrieval.html>`_ class.

For convenience, method `s.get_eids()` returns the list of EIDs (similar to attribute `EIDS` in scopus 0.x):

.. code-block:: python

    >>> s.get_eids()
