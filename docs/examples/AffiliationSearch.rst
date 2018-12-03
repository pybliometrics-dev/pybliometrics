Affiliation Search
------------------

:doc:`AffiliationSearch <../reference/scopus.AffiliationSearch>` implements the `Affiliation Search API <https://dev.elsevier.com/documentation/AffiliationSearchAPI.wadl>`_.  It performs a query to search for affiliations and then retrieves the records of the query.

The class is initialized with a search query which you can read about in `Affiliation Search Guide <https://dev.elsevier.com/tips/AffiliationSearchTips.htm>`_.  Keep in mind that an invalid search query will result in an error.

.. code-block:: python
   
    >>> from scopus import AffiliationSearch
    >>> query = "AFFIL(Max Planck Institute for Innovation and Competition Munich)"
    >>> s = AffiliationSearch(query, refresh=True)


The class mostly serves to provide a list of namedtuples storing information about the affiliation. One of them is the affiliation ID which you can use for the `ScopusAffiliation <../reference/scopus.ScopusAffiliation.html>`_ class:

.. code-block:: python

    >>> s.affiliations
    [Affiliation(eid='10-s2.0-60105007', name='Max Planck Institute for Innovation and Competition',
    variant='Max Planck Institute For Innovation And Competition',
    documents='376', city='Munich', country='Germany', parent='0')]


It's easy to work with `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_, for example using `pandas <https://pandas.pydata.org/>`_ you can quickly turn the results into a DataFrame:

.. code-block:: python

    >>> import pandas as pd
    >>> print(pd.DataFrame(s.affiliations).T)
                                                                 0
    eid                                           10-s2.0-60105007
    name       Max Planck Institute for Innovation and Competition
    variant    Max Planck Institute for Innovation and Competition
    documents                                                  376
    city                                                    Munich
    country                                                Germany
    parent                                                       0


Often you receive more search results than Scopus allows.  Currently the cap is
at 5000 results.  In this case it helps to narrow down the research, i.e. instead
of "affil('Harvard Medical School')" you search for "affil('Harvard Medical School Boston')".

More on different types of affiliations in section `tips <../tips.html#affiliations>`_.
