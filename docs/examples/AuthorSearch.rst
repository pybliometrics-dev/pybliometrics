Author Search
-------------

:doc:`AuthorSearch() <../reference/pybliometrics.AuthorSearch>` implements the `Author Search API <https://dev.elsevier.com/documentation/AuthorSearchAPI.wadl>`_.  It performs a query to search for authors and then retrieves the records of the query.

The class is initialized with a search query which you can read about in `Author Search Guide <https://dev.elsevier.com/tips/AuthorSearchTips.htm>`_.  An invalid search query will result in an error.

.. code-block:: python

    >>> from pybliometrics.scopus import AuthorSearch
    >>> s = AuthorSearch('AUTHLAST(Selten) and AUTHFIRST(Reinhard)')


You can obtain a search summary just by printing the object:

.. code-block:: python

    >>> print(s)
    Search 'AUTHLAST(Selten) and AUTHFIRST(Reinhard)' yielded 2 authors as of 2020-04-15:
        Selten, Reinhard
        Selten, Reinhard


To know the the number of results use the `.get_results_size()` method, even before you download the results:

.. code-block:: python

    >>> other = AuthorSearch("AUTHLAST(Selten)", download=False)
    >>> other.get_results_size()
    25


The class mostly serves to provide a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_ storing author EIDs, which you can use for the :doc:`AuthorRetrieval <../reference/pybliometrics.AuthorRetrieval>` class, and corresponding information:

.. code-block:: python

    >>> s.authors
    [Author(eid='9-s2.0-6602907525', surname='Selten', initials='R.',
     givenname='Reinhard', affiliation='Universitat Bonn', documents='73',
     affiliation_id='60007493', city='Bonn', country='Germany',
     areas='ECON (71); MATH (19); BUSI (15)')]


It's easy to work with namedtuples: Using `pandas <https://pandas.pydata.org/>`_, you can quickly turn the results set into a DataFrame:

.. code-block:: python

    >>> import pandas as pd
    >>> print(pd.DataFrame(s.authors))
                     eid surname initials givenname       affiliation documents  \
    0  9-s2.0-6602907525  Selten       R.  Reinhard  Universitat Bonn        73

      affiliation_id  city  country                            areas
    0       60007493  Bonn  Germany  ECON (71); MATH (19); BUSI (15)


Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `s.get_cache_file_mdate()` to get the date of last modification, and `s.get_cache_file_age()` the number of days since the last modification.

There are sometimes missing information in the returned results although it exists in the Scopus database.  For example, the EID may be missing, even though every element always has an EID.  This is not a bug of `pybliometrics`.  Instead it is somehow related to a problem in the download process from the Scopus database.  To check for completeness of specific fields, use parameter `integrity_fields`, which accepts any iterable.  Using parameter `integrity_action` you can choose between two actions on what to do if the integrity check fails: Set `integrity_action="warn"` to issue a UserWarning, or set `integrity_action="raise"` to raise an AttributeError.

.. code-block:: python

    >>> s = AuthorSearch("AUTHLAST(Selten)", integrity_fields=["eid"], integrity_action="warn")
