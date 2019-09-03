Scopus Search
-------------

:doc:`ScopusSearch <../reference/pybliometrics.ScopusSearch>` implements the `Scopus Search API <https://api.elsevier.com/documentation/SCOPUSSearchAPI.wadl>`_.  It performs a query to search for articles and then retrieves the records of the query.

The class is initialized with a search query.  Any query that works in the `Advanced Search on scopus.com <https://www.scopus.com/search/form.uri?display=advanced>`_ will work.  An invalid search query will result in an error.

.. code-block:: python
   
    >>> from pybliometrics.scopus import ScopusSearch
    >>> s = ScopusSearch('FIRSTAUTH ( kitchin  j.r. )')


Non-subscribers must instantiate the class with `subscriber=False`.  They may only get 5000 results per query, whereas this limit does not exist for subscribers.

Users can recieve the number of results programmatically via `.get_results_size()`:

.. code-block:: python

    >>> s.get_results_size()
    12


This method works even if one chooses to not download results.  It thus helps subscribers to decide programmatically if one wants to proceed downloading or not:

.. code-block:: python
   
    >>> from pybliometrics.scopus import ScopusSearch
    >>> other = ScopusSearch('AUTHLASTNAME(Brown)', download=False)
    >>> other.get_results_size()
    259526


The class' main attribute `results` returns a list of `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_.  They can be used neatly with `pandas <https://pandas.pydata.org/>`_ to form DataFrames:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.DataFrame(pd.DataFrame(s.results))
    >>> df.columns
    Index(['eid', 'doi', 'pii', 'pubmed_id', 'title', 'subtype', 'subtypeDescription', 'creator',
       'afid', 'affilname', 'affiliation_city', 'affiliation_country', 'author_count',
       'author_names', 'author_ids', 'author_afids', 'coverDate',
       'coverDisplayDate', 'publicationName', 'issn', 'source_id', 'eIssn',
       'aggregationType', 'volume', 'issueIdentifier', 'article_number',
       'pageRange', 'description', 'authkeywords', 'citedby_count',
       'openaccess', 'fund_acr', 'fund_no', 'fund_sponsor'],
      dtype='object')
    >>> df.shape
    (12, 33)
    >>> pd.set_option('display.max_columns', None)
    >>> df.head()
                      eid                         doi                pii  \
    0  2-s2.0-85019169906   10.1007/s00799-016-0173-7               None   
    1  2-s2.0-84971324241           10.1002/aic.15294               None   
    2  2-s2.0-84930349644  10.1016/j.susc.2015.05.007  S0039602815001326   
    3  2-s2.0-84930616647    10.1021/acscatal.5b00538               None   
    4  2-s2.0-67449106405  10.1103/PhysRevB.79.205412               None   

      pubmed_id                                              title subtype  \
    0      None    Automating data sharing through authoring tools      ar   
    1      None  High-throughput methods using composition and ...      ar   
    2      None                    Data sharing in Surface Science      ar   
    3      None  Examples of effective data sharing in scientif...      re   
    4      None  Correlations in coverage-dependent atomic adso...      ar   

          creator                        afid  \
    0  Kitchin J.  60027950;60027950;60027950   
    1  Kitchin J.                    60027950   
    2  Kitchin J.                    60027950   
    3  Kitchin J.                    60027950   
    4  Kitchin J.                    60027950   

                                               affilname  \
    0  Carnegie Mellon University;Carnegie Mellon Uni...   
    1                         Carnegie Mellon University   
    2                         Carnegie Mellon University   
    3                         Carnegie Mellon University   
    4                         Carnegie Mellon University   

                       affiliation_city  \
    0  Pittsburgh;Pittsburgh;Pittsburgh   
    1                        Pittsburgh   
    2                        Pittsburgh   
    3                        Pittsburgh   
    4                        Pittsburgh   

                             affiliation_country author_count  \
    0  United States;United States;United States            4   
    1                              United States            2   
    2                              United States            1   
    3                              United States            1   
    4                              United States            1   

                                            author_names  \
    0  Kitchin, John R.;Van Gulick, Ana E.;Zilinski, ...   
    1                Kitchin, John R.;Gellman, Andrew J.   
    2                                   Kitchin, John R.   
    3                                   Kitchin, John R.   
    4                                   Kitchin, John R.   

                               author_ids                author_afids   coverDate  \
    0  7004212771;50761335600;55755405700  60027950;60027950;60027950  2017-06-01   
    1              7004212771;35514271900           60027950;60027950  2016-11-01   
    2                          7004212771                    60027950  2016-05-01   
    3                          7004212771                    60027950  2015-06-05   
    4                          7004212771                    60027950  2009-05-01   

      coverDisplayDate                                    publicationName  \
    0      1 June 2017         International Journal on Digital Libraries   
    1  1 November 2016                                      AIChE Journal   
    2       1 May 2016                                    Surface Science   
    3      5 June 2015                                      ACS Catalysis   
    4       1 May 2009  Physical Review B - Condensed Matter and Mater...   

           issn    source_id     eIssn aggregationType volume issueIdentifier  \
    0  14325012       145200  14321300         Journal     18               2   
    1  00011541        16275  15475905         Journal     62              11   
    2  00396028        12284      None         Journal    647            None   
    3  21555435  19700188320      None         Journal      5               6   
    4  10980121  11000153773  1550235X         Journal     79              20   

      article_number  pageRange  \
    0           None      93-98   
    1           None  3826-3835   
    2           None    103-107   
    3           None  3894-3899   
    4         205412       None   

                                             description  \
    0  © 2016, Springer-Verlag Berlin Heidelberg. In ...   
    1                                               None   
    2  © 2015 Elsevier B.V. All rights reserved. Surf...   
    3  © 2015 American Chemical Society. We present a...   
    4  The adsorption energy of an adsorbate can depe...   

                                          authkeywords citedby_count openaccess  \
    0  Authoring | Data sharing | Embedding | Org-mode             1          0   
    1                                             None             3          0   
    2                                     Data sharing             2          1   
    3                                             None             8          1   
    4                                             None            50          0   

      fund_acr       fund_no                 fund_sponsor  
    0     None     undefined                         None  
    1      NSF  DE-SC0004031  National Science Foundation  
    2      CMU  DE-SC0004031   Carnegie Mellon University  
    3     None     undefined                         None  
    4     None     undefined                         None


The EIDs can be used for the `AbstractRetrieval <../reference/pybliometrics.AbstractRetrieval.html>`_ class and the Scopus Author IDs in column "authid" for the `AuthorRetrieval <../reference/pybliometrics.AuthorRetrieval.html>`_ class.

There are sometimes missing fields in the returned results although it exists in the Scopus database.  For example, the EID may be missing, even though every element always has an EID.  This is not a bug of `pybliometrics`.  Instead it is somehow related to a problem in the download process from the Scopus database.  To check for completeness of specific fields, use parameter `integrity_fields`, which accepts any iterable.  Using parameter `integrity_action` you can choose between two actions on what to do if the integrity check fails: Set `integrity_action="warn"` to issue a UserWarning, or set `integrity_action="raise"` to raise an AttributeError.

.. code-block:: python
   
    >>> s = ScopusSearch('FIRSTAUTH ( kitchin  j.r. )', integrity_fields=["eid"], integrity_action="warn")


If you care about integrity of specific fields, you can attempt to refresh the downloaded file:

.. code-block:: python
   
    def robust_query(q, refresh=False):
        """Wrapper function for individual ScopusSearch query."""
        try:
            return ScopusSearch(q, refresh=refresh).results
        except AttributeError:
            return ScopusSearch(q, refresh=True).results


The Scopus Search API allows a differing information depth via
`views <https://dev.elsevier.com/guides/ScopusSearchViews.htm>`_.  The view 'COMPLETE' is the highest unrestricted view and contains all information also included in the 'STANDARD' view.  It is therefore the default view.  However, when speed is an issue, choose the STANDARD view.

For convenience, method `s.get_eids()` returns the list of EIDs:

.. code-block:: python

    >>> s.get_eids()
    ['2-s2.0-85019169906', '2-s2.0-84971324241', '2-s2.0-84930349644',
    '2-s2.0-84930616647', '2-s2.0-67449106405', '2-s2.0-40949100780',
    '2-s2.0-37349101648', '2-s2.0-20544467859', '2-s2.0-13444307808',
    '2-s2.0-2942640180', '2-s2.0-0141924604', '2-s2.0-0037368024']
