pybliometrics.scopus.AffiliationSearch
======================================

`AffiliationSearch()` implements the `Affiliation Search API <https://dev.elsevier.com/documentation/AffiliationSearchAPI.wadl>`_.  It performs a query to search for affiliations and then retrieves the records of the query.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: AffiliationSearch
   :members:
   :inherited-members:

Examples
--------

The class is initialized with a search query which you can read about in `Affiliation Search Guide <https://dev.elsevier.com/tips/AffiliationSearchTips.htm>`_.  An invalid search query will result in an error.

.. code-block:: python

    >>> from pybliometrics.scopus import AffiliationSearch
    >>> query = "AFFIL(Max Planck Institute for Innovation and Competition Munich)"
    >>> s = AffiliationSearch(query)


You can obtain a search summary just by printing the object:

.. code-block:: python

    >>> print(s)
    Search 'AFFIL(Max Planck Institute for Innovation and Competition Munich)' yielded
    2 affiliations as of 2021-01-15:
        Max Planck Institute for Innovation and Competition
        Max Planck Institute for Competition and Innovation


The class mostly serves to provide a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_ storing information about the affiliation.  One of them is the affiliation ID which you can use for the :doc:`AffiliationRetrieval <../classes/AffiliationRetrieval>` class:

.. code-block:: python

    >>> s.affiliations
    [Affiliation(eid='10-s2.0-60105007', name='Max Planck Institute for Innovation and Competition',
                 variant='Max Planck Institute For Innovation And Competition', documents=380,
                 city='Munich', country='Germany', parent='0'),
     Affiliation(eid='10-s2.0-117495104', name='Max Planck Institute for Competition and Innovation',
                 variant='Max-plank Institut', documents=3, city='Munich', country='Germany',
                 parent='0')]


It's easy to work with namedtuples: using `pandas <https://pandas.pydata.org/>`_ for example you can quickly turn the results into a DataFrame:

.. code-block:: python

    >>> import pandas as pd
    >>> pd.set_option('display.max_columns', None)
    >>> print(pd.DataFrame(s.affiliations))
                     eid                                               name  \
    0   10-s2.0-60105007  Max Planck Institute for Innovation and Compet...   
    1  10-s2.0-117495104  Max Planck Institute for Competition and Innov...   

                                                 variant  documents    city  \
    0  Max Planck Institute For Innovation And Compet...        380  Munich   
    1                                 Max-plank Institut          3  Munich   

       country parent  
    0  Germany      0  
    1  Germany      0 


As you can see from comparison of the EIDs, the first affiliation starts with 10-s2.0-6, the other with 10-s2.0-1.  The latter denotes a non-org affiliation type.  
More on different types of affiliations in section `tips <../tips.html#affiliations>`_.

Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `s.get_cache_file_mdate()` to get the date of last modification, and `s.get_cache_file_age()` the number of days since the last modification.

You can get the number of results using the `.get_results_size()` method, even before you download the results:

.. code-block:: python

    >>> query = "AFFIL(Max Planck Institute)"
    >>> s = AffiliationSearch(query, download=False)
    >>> s.get_results_size()
    398


There are sometimes missing information in the returned results although it exists in the Scopus database.  For example, the EID may be missing, even though every element always has an EID.  This is not a bug of `pybliometrics`.  Instead it is somehow related to a problem in the download process from the Scopus database.  To check for completeness of specific fields, use parameter `integrity_fields`, which accepts any iterable.  Using parameter `integrity_action` you can choose between two actions on what to do if the integrity check fails: Set `integrity_action="warn"` to issue a UserWarning, or set `integrity_action="raise"` to raise an AttributeError.

.. code-block:: python

    >>> s = AffiliationSearch(query, integrity_fields=["eid"], integrity_action="warn")


Often you receive more search results than Scopus allows.  Currently the cap is at 5000 results.  In this case the only solution is to narrow down the research, i.e. instead of "affil('Harvard Medical School')" you search for "affil('Harvard Medical School Boston')".
