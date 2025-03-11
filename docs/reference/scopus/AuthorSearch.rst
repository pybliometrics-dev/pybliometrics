pybliometrics.scopus.AuthorSearch
=================================

`AuthorSearch()` implements the `Author Search API <https://dev.elsevier.com/documentation/AuthorSearchAPI.wadl>`_.  It executes a query to search for authors and retrieves the corresponding records.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: AuthorSearch
    :members:
    :inherited-members:

Examples
--------

The class is initialized using a search query, details of which can be found in `Author Search Guide <https://dev.elsevier.com/tips/AuthorSearchTips.htm>`_.  An invalid search query will result in an error.

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import AuthorSearch
    >>> pybliometrics.scopus.init()
    >>> s = AuthorSearch('AUTHLAST(Selten) and AUTHFIRST(Reinhard)')


You can obtain a search summary just by printing the object:

.. code-block:: python

    >>> print(s)
    Search 'AUTHLAST(Selten) and AUTHFIRST(Reinhard)' yielded 2 authors as of 2024-05-11:
		Selten, Reinhard; AUTHOR_ID:6602907525 (74 document(s))
		Selten, Reinhard; AUTHOR_ID:57213632570 (1 document(s))


To determine the the number of results use the `.get_results_size()` method, even before you download the results:

.. code-block:: python

    >>> other = AuthorSearch("AUTHLAST(Selten)", download=False)
    >>> other.get_results_size()
    27


Primarily, the class provides a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_ storing author EIDs, which you can use for the :doc:`AuthorRetrieval <AuthorRetrieval>` class, and corresponding information:

.. code-block:: python

    >>> s.authors[0]
    [Author(eid='9-s2.0-6602907525', orcid=None, surname='Selten', initials='R.',
     givenname='Reinhard', affiliation='Universitat Bonn', documents=74,
     affiliation_id='60007493', city='Bonn', country='Germany',
     areas='ECON (73); MATH (19); BUSI (16)')]


Working with namedtuples is straightforward: Using `pandas <https://pandas.pydata.org/>`_, you can quickly convert the results set into a DataFrame:

.. code-block:: python

    >>> import pandas as pd
    >>> pd.set_option('display.max_columns', None)
    >>> print(pd.DataFrame(s.authors))
                      eid orcid surname initials givenname  \
    0   9-s2.0-6602907525  None Selten       R.  Reinhard
    1  9-s2.0-57213632570  None Selten       R.  Reinhard

                         affiliation  documents affiliation_id     city  country  \
    0               Universität Bonn         74       60007493     Bonn  Germany   
    1  Southwest Jiaotong University          1       60010421  Chengdu    China   

                                 areas  
    0  ECON (73); MATH (19); BUSI (16)  
    1                         COMP (3)


Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.

Occasionally, some information that exists in the Scopus database may be missing in the returned results.  For example, the EID may be missing, even though every element always has an EID.  This is not a bug of `pybliometrics`.  Instead it is somehow related to a problem in the download process from the Scopus database.  To check for completeness of specific fields, use parameter `integrity_fields`, which accepts any iterable.  With the `integrity_action` parameter you can choose between two actions if the integrity check fails: Set `integrity_action="warn"` to issue a UserWarning, or set `integrity_action="raise"` to raise an AttributeError.

.. code-block:: python

    >>> s = AuthorSearch("AUTHLAST(Selten)", integrity_fields=["eid"], integrity_action="warn")


When searching for authors by institution, it's important to note that searching by affiliation profile ID and affiliation name yields different results.  Search by affiliation name, i.e. `AFFIL(Max Planck Institute for Innovation and Competition)`), finds all authors *ever* affiliated with the Max Planck Institute for Innovation and Competition, whereas search by affiliation profile ID, i.e. `AF-ID(60105007)`, finds researchers whose latest affiliation includes the Max Planck Institute for Innovation and Competition.
