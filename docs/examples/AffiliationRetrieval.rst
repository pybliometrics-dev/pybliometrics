Affiliation Retrieval
---------------------

:doc:`AffiliationRetrieval() <../reference/pybliometrics.AffiliationRetrieval>` implements the `Affiliation Retrieval API <https://dev.elsevier.com/documentation/AffiliationRetrievalAPI.wadl>`_. It provides basic information on registered affiliations, like city, country, its members, and more.

You initialize the class with Scopus' Affiliation ID:

.. code-block:: python

    >>> from pybliometrics.scopus import AffiliationRetrieval
    >>> aff = AffiliationRetrieval("60000356")


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(aff)
    University of Cape Town in Cape Town in South Africa,
    has 12,463 associated author(s) and 68,181 associated document(s) as of 2020-07-11


The object has a number of attributes but no methods.  For example, information regarding the affiliation itself:

.. code-block:: python

    >>> aff.affiliation_name
    'University of Cape Town'
    >>> aff.sort_name
    'Cape Town, University of'
    >>> aff.org_type
    'univ'
    >>> aff.postal_code
    '7701'
    >>> aff.city
    'Cape Town'
    >>> aff.state
    'Western Cape'
    >>> aff.country
    'South Africa'
    >>> aff.org_domain
    'uct.ac.za'
    >>> aff.org_URL
    'http://www.uct.ac.za'


There are meta information, too:

.. code-block:: python

    >>> aff.author_count
    '10951'
    >>> aff.document_count
    '53312'


Scopus also collects information on different names affiliated authors use for this affiliation, which `pybliometrics` returns as list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> aff.name_variants
    [Variant(name='University Of Cape Town', doc_count='60095'),
     Variant(name='Univ. Cape Town', doc_count='1659'),
     Variant(name='Univ Of Cape Town', doc_count='772'),
     Variant(name='Univ. Of Cape Town', doc_count='392')]


Using `pandas <https://pandas.pydata.org/>`_ you can easily turn this into a DataFrame:

.. code-block:: python

    >>> import pandas as pd
    >>> print(pd.DataFrame(aff.name_variants))
                          name doc_count
    0  University Of Cape Town     60095
    1          Univ. Cape Town      1659
    2        Univ Of Cape Town       772
    3       Univ. Of Cape Town       392


More on different types of affiliations in section `tips <../tips.html#affiliations>`_.

Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `aff.get_cache_file_mdate()` to get the date of last modification, and `aff.get_cache_file_age()` the number of days since the last modification.
