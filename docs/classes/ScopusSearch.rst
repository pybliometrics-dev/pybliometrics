pybliometrics.scopus.ScopusSearch
=================================

`ScopusSearch()` implements the `Scopus Search API <https://dev.elsevier.com/documentation/SCOPUSSearchAPI.wadl>`_.  It performs a query to search for documents and then retrieves the records of the query.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: ScopusSearch
   :members:
   :inherited-members:

Examples
--------

The class is initialized with a search query.  Any query that works in the `Advanced Search on scopus.com <https://www.scopus.com/search/form.uri?display=advanced>`_ will work.  There are but two exceptions to allowed keywords: "LIMIT-TO()", as this only affects the display of the results on scopus.com, but not the selection of results per se; and "INDEXTERMS()".  An invalid search query will result in some `error <../tips.html#error-messages>`_.

.. code-block:: python

    >>> from pybliometrics.scopus import ScopusSearch
    >>> s = ScopusSearch('FIRSTAUTH ( kitchin  j.r. )')


You can obtain a search summary just by printing the object:

.. code-block:: python

    >>> print(s)
    Search 'FIRSTAUTH ( kitchin  j.r. )' yielded 13 documents of 2020-04-15:
        2-s2.0-85048443766
        2-s2.0-85019169906
        2-s2.0-84971324241
        2-s2.0-84930349644
        2-s2.0-84930616647
        2-s2.0-67449106405
        2-s2.0-40949100780
        2-s2.0-37349101648
        2-s2.0-20544467859
        2-s2.0-13444307808
        2-s2.0-2942640180
        2-s2.0-0141924604
        2-s2.0-0037368024


Non-subscribers must instantiate the class with `subscriber=False`.  They may only get 5000 results per query, whereas this limit does not exist for subscribers.

Users can receive the number of results programmatically via `.get_results_size()`:

.. code-block:: python

    >>> s.get_results_size()
    13


This method works even if one chooses to not download results.  It thus helps subscribers to decide programmatically if one wants to proceed downloading or not:

.. code-block:: python

    >>> from pybliometrics.scopus import ScopusSearch
    >>> other = ScopusSearch('AUTHLASTNAME(Brown)', download=False)
    >>> other.get_results_size()
    259526


The class' main attribute `results` returns a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_.  They can be used neatly with `pandas <https://pandas.pydata.org/>`_ to form DataFrames:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.DataFrame(pd.DataFrame(s.results))
    >>> df.columns
    Index(['eid', 'doi', 'pii', 'pubmed_id', 'title', 'subtype', 'subtypeDescription',
           'creator', 'afid', 'affilname', 'affiliation_city', 'affiliation_country',
           'author_count', 'author_names', 'author_ids', 'author_afids', 'coverDate',
           'coverDisplayDate', 'publicationName', 'issn', 'source_id', 'eIssn',
           'aggregationType', 'volume', 'issueIdentifier', 'article_number',
           'pageRange', 'description', 'authkeywords', 'citedby_count',
           'openaccess', 'freetoread', 'freetoreadLabel' 'fund_acr', 'fund_no', 'fund_sponsor'],
          dtype='object')
    >>> df.shape
    (12, 33)
    >>> pd.set_option('display.max_columns', None)
    >>> df.head()
                      eid                         doi                pii  \
    0  2-s2.0-85048443766   10.1038/s41929-018-0056-y               None
    1  2-s2.0-85019169906   10.1007/s00799-016-0173-7               None
    2  2-s2.0-84971324241           10.1002/aic.15294               None
    3  2-s2.0-84930349644  10.1016/j.susc.2015.05.007  S0039602815001326
    4  2-s2.0-84930616647    10.1021/acscatal.5b00538               None

      pubmed_id                                              title subtype  \
    0      None                      Machine learning in catalysis      no
    1      None    Automating data sharing through authoring tools      ar
    2      None  High-throughput methods using composition and ...      ar
    3      None                    Data sharing in Surface Science      ar
    4      None  Examples of effective data sharing in scientif...      re

      subtypeDescription       creator      afid                   affilname  \
    0               Note    Kitchin J.  60027950  Carnegie Mellon University
    1            Article  Kitchin J.R.  60027950  Carnegie Mellon University
    2            Article    Kitchin J.  60027950  Carnegie Mellon University
    3            Article    Kitchin J.  60027950  Carnegie Mellon University
    4             Review    Kitchin J.  60027950  Carnegie Mellon University

      affiliation_city affiliation_country author_count  \
    0       Pittsburgh       United States            1
    1       Pittsburgh       United States            3
    2       Pittsburgh       United States            2
    3       Pittsburgh       United States            1
    4       Pittsburgh       United States            1

                                            author_names  \
    0                                   Kitchin, John R.
    1  Kitchin, John R.;Van Gulick, Ana E.;Zilinski, ...
    2                Kitchin, John R.;Gellman, Andrew J.
    3                                   Kitchin, John R.
    4                                   Kitchin, John R.

                               author_ids                author_afids   coverDate  \
    0                          7004212771                    60027950  2018-04-01
    1  7004212771;50761335600;55755405700  60027950;60027950;60027950  2017-06-01
    2              7004212771;35514271900           60027950;60027950  2016-11-01
    3                          7004212771                    60027950  2016-05-01
    4                          7004212771                    60027950  2015-06-05

      coverDisplayDate                             publicationName      issn  \
    0     1 April 2018                            Nature Catalysis      None
    1      1 June 2017  International Journal on Digital Libraries  14325012
    2  1 November 2016                               AIChE Journal  00011541
    3       1 May 2016                             Surface Science  00396028
    4      5 June 2015                               ACS Catalysis  21555435

         source_id     eIssn aggregationType volume issueIdentifier  \
    0  21100862548  25201158         Journal      1               4
    1       145200  14321300         Journal     18               2
    2        16275  15475905         Journal     62              11
    3        12284      None         Journal    647            None
    4  19700188320      None         Journal      5               6

      article_number  pageRange  \
    0           None    230-232
    1           None      93-98
    2           None  3826-3835
    3           None    103-107
    4           None  3894-3899

                                             description  \
    0                                               None
    1  In the current scientific publishing landscape...
    2                                               None
    3  Surface Science has an editorial policy that a...
    4  We present a perspective on an approach to dat...

                                          authkeywords  citedby_count  openaccess  \
    0                                             None            149           0
    1  Authoring | Data sharing | Embedding | Org-mode              1           0
    2                                             None              9           1
    3                                     Data sharing              2           1
    4                                             None             14           1

               freetoread freetoreadLabel fund_acr       fund_no  \
    0                None            None     None     undefined
    1                None            None     None     undefined
    2  publisherfree2read          Bronze      NSF  DE-SC0004031
    3  publisherfree2read          Bronze       SC  DE-SC0004031
    4  publisherfree2read          Bronze     None     undefined

                      fund_sponsor
    0                         None
    1                         None
    2  National Science Foundation
    3            Office of Science
    4                         None


Keep in mind that no more than 100 authors are included in the search results.

The EIDs of documents can be used for the :doc:`AbstractRetrieval() <../classes/AbstractRetrieval>` class and the Scopus Author IDs in column "authid" for the :doc:`AuthorRetrieval() <../classes/AuthorRetrieval>` class.

Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `s.get_cache_file_mdate()` to get the date of last modification, and `s.get_cache_file_age()` the number of days since the last modification.

There are sometimes missing fields in the returned results although it exists in the Scopus database.  For example, the EID may be missing, even though every element always has an EID.  This is not a bug of `pybliometrics`.  Instead it is somehow related to a problem in the download process from the Scopus database.  To check for completeness of specific fields, use parameter `integrity_fields`, which accepts any iterable.  Using parameter `integrity_action` you can choose between two actions on what to do if the integrity check fails: Set `integrity_action="warn"` to issue a UserWarning, or set `integrity_action="raise"` to raise an AttributeError.

.. code-block:: python

    >>> s = ScopusSearch('FIRSTAUTH ( kitchin  j.r. )',
                         integrity_fields=["eid"], integrity_action="warn")


If you care about integrity of specific fields, you can attempt to refresh the downloaded file:

.. code-block:: python

    def robust_query(q, refresh=False, fields=["eid"]):
        """Wrapper function for individual ScopusSearch query."""
        try:
            return ScopusSearch(q, refresh=refresh, integrity_fields=fields).results
        except AttributeError:
            return ScopusSearch(q, refresh=True, integrity_fields=fields).results


The Scopus Search API allows a differing information depth via
`views <https://dev.elsevier.com/guides/ScopusSearchViews.htm>`_.  The view 'COMPLETE' is the highest unrestricted view and contains all information also included in the 'STANDARD' view.  It is therefore the default view.  However, when speed is an issue, choose the STANDARD view.

For convenience, method `s.get_eids()` returns the list of EIDs:

.. code-block:: python

    >>> s.get_eids()
    ['2-s2.0-85019169906', '2-s2.0-84971324241', '2-s2.0-84930349644',
    '2-s2.0-84930616647', '2-s2.0-67449106405', '2-s2.0-40949100780',
    '2-s2.0-37349101648', '2-s2.0-20544467859', '2-s2.0-13444307808',
    '2-s2.0-2942640180', '2-s2.0-0141924604', '2-s2.0-0037368024']
