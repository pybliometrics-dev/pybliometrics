pybliometrics.scopus.AffiliationRetrieval
=========================================

`AffiliationRetrieval()` implements the `Affiliation Retrieval API <https://dev.elsevier.com/documentation/AffiliationRetrievalAPI.wadl>`_. It provides basic information on registered affiliations, such as city, country, its members, and more.

In addition, the 'ENTITLED' view lets you check you whether you have access to this class.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: AffiliationRetrieval
    :members:
    :inherited-members:

Examples
--------

You initialize the class using Scopus' Affiliation ID:

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import AffiliationRetrieval
    >>> pybliometrics.scopus.init()
    >>> aff = AffiliationRetrieval(60000356)


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(aff)
    University of Cape Town in Cape Town in South Africa,
    has 13,895 associated author(s) and 0 associated document(s) as of 2026-10-02


The object has several of attributes but no methods.  For example, information regarding the affiliation itself:

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


There are meta-information, too:

.. code-block:: python

    >>> aff.author_count
    13895
    >>> aff.document_count
    0


Scopus also collects information on different names affiliated authors use for this affiliation, which `pybliometrics` returns as list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> aff.name_variants
    [Variant(name='University of Cape Town', doc_count=None),
     Variant(name='Universiteit van Kaapstad', doc_count=None),
     Variant(name='IYunivesithi Yasekapa', doc_count=None)]


Using `pandas <https://pandas.pydata.org/>`_, you can easily convert this into a DataFrame:

.. code-block:: python

    >>> import pandas as pd
    >>> print(pd.DataFrame(aff.name_variants))
                            name doc_count
    0    University of Cape Town      None
    1  Universiteit van Kaapstad      None
    2      IYunivesithi Yasekapa      None


More on different types of affiliations in section `tips <../tips.html#affiliations>`_.

Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.
