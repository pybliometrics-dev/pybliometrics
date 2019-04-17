Author Search
-------------

:doc:`AuthorSearch <../reference/scopus.AuthorSearch>` implements the `Author Search API <https://dev.elsevier.com/documentation/AuthorSearchAPI.wadl>`_.  It performs a query to search for authors and then retrieves the records of the query.

The class is initialized with a search query which you can read about in `Author Search Guide <https://dev.elsevier.com/tips/AuthorSearchTips.htm>`_.  Keep in mind that an invalid search query will result in an error.

.. code-block:: python
   
    >>> from scopus import AuthorSearch
    >>> s = AuthorSearch('AUTHLAST(Selten) and AUTHFIRST(Reinhard)', refresh=True)


To know the the number of results use the `.get_results_size()` method, even before you download the results:

.. code-block:: python
   
    >>> other = AuthorSearch("AUTHLAST(Selten)", download=False)
    >>> other.get_results_size()
    25


The class mostly serves to provide a list of `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_ storing author EIDs, which you can use for the `ScopusAuthor <../reference/scopus.ScopusAuthor.html>`_ class, and corresponding information:

.. code-block:: python

    >>> s.authors
    [Author(eid='9-s2.0-6602907525', surname='Selten', initials='R.',
    givenname='Reinhard', affiliation='Universitat Bonn', documents='73',
    affiliation_id='60007493', city='Bonn', country='Germany',
    areas='ECON (71); MATH (19); BUSI (15)')]


It's easy to work with namedtuples, for example using `pandas <https://pandas.pydata.org/>`_:

.. code-block:: python

    >>> import pandas as pd
    >>> print(pd.DataFrame(s.authors)
                     eid surname initials givenname       affiliation documents  \
    0  9-s2.0-6602907525  Selten       R.  Reinhard  Universitat Bonn        73   

      affiliation_id  city  country                            areas  
    0       60007493  Bonn  Germany  ECON (71); MATH (19); BUSI (15)
