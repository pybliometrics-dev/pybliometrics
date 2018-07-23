Affiliation Search
------------------

:doc:`AffiliationSearch <../reference/scopus.AffiliationSearch>` implements the `Affiliation Search API <https://dev.elsevier.com/documentation/AffiliationSearchAPI.wadl>`_.  It performs a query to search for authors and then retrieves the records of the query.

The class is initialized with a search query which you can read about in `Affiliation Search Guide <https://dev.elsevier.com/tips/AffiliationSearchTips.htm>`_.  Keep in mind that an invalid search query will result in an error.

.. code-block:: python
   
    >>> from scopus import AffiliationSearch
    >>> s = AuthorSearch('AF-ID(60021784)', refresh=True)


The class mostly serves to provide a list of namedtuples storing information about the affiliation. One of them is the affiliation ID which you can use for the `ScopusAffiliation <../reference/scopus.ScopusAffiliation.html>`_ class:

.. code-block:: python

    >>> s.affiliations
    [Affiliation(eid='10-s2.0-60021784', name='New York University',
                 variant='', documents='97860', city='New York',
                 country='United States', parent='0')]


It's easy to work with `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_, for example using `pandas <https://pandas.pydata.org/>`_ you can quickly turn the results into a DataFrame:

.. code-block:: python

    >>> import pandas as pd
    >>> print(pd.DataFrame(s.affiliations)
                    eid                 name variant documents      city  \
    0  10-s2.0-60021784  New York University             97860  New York   

            country parent  
    0  United States      0


Often you receive more search results than Scopus allows.  Currently the cap is
at 5000 results.  In this case it helps to narrow down the research, i.e. instead
of "affil('Harvard Medical School')" you search for "affil('Harvard Medical School Boston')".
