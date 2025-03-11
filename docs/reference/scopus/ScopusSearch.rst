pybliometrics.scopus.ScopusSearch
=================================

`ScopusSearch()` implements the `Scopus Search API <https://dev.elsevier.com/documentation/SCOPUSSearchAPI.wadl>`_.  It executes a query to search for documents and retrieves the resulting records. Any query that works in the `Advanced Document Search on scopus.com <https://www.scopus.com/search/form.uri?display=advanced>`_ will work (with two exceptions, see below), but with `ScopusSearch()` you achieve this programmatically, faster and without the download size cap.

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

The class is initialized with a search query.  There are but two exceptions to allowed keywords as compared to the Advanced Document Search: "LIMIT-TO()", as this only affects the display of the results on scopus.com, but not the selection of results per se; and "INDEXTERMS()".  An invalid search query will result in some `error <../tips.html#error-messages>`_.  Setting `verbose=True` informs about the download progress.

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import ScopusSearch
    >>> pybliometrics.scopus.init()
    >>> q = "REF(2-s2.0-85068268027)"
    >>> s = ScopusSearch(q, verbose=True)
    Downloading results for query "REF(2-s2.0-85068268027)":
    100%|████████████████████████████████████████████████████████████████████████████████████████████████| 6/6 [00:05<00:00,  1.07s/it]


You can obtain a search summary just by printing the object:

.. code-block:: python

    >>> print(s)
    Search 'REF(2-s2.0-85068268027)' yielded 128 documents as of 2025-02-06:
            2-s2.0-85211039740
            2-s2.0-85214107782
            2-s2.0-85214598506
            2-s2.0-85210715388
            2-s2.0-85204999049
            2-s2.0-85202700133
            2-s2.0-85181227776
            2-s2.0-85206823306
            2-s2.0-85201454159
            2-s2.0-85201597291
            2-s2.0-85194707120
    # output truncated


Non-subscribers must instantiate the class with `subscriber=False`.  They may only get 5,000 results per query, whereas this limit does not exist for subscribers.

Users can determine the number of results programmatically using the `.get_results_size()` method:

.. code-block:: python

    >>> s.get_results_size()
    128


This method works even if one chooses to not download results.  It thus helps subscribers to decide programmatically if one wants to proceed downloading or not:

.. code-block:: python

    >>> other = ScopusSearch('AUTHLASTNAME(Brown)', download=False)
    >>> other.get_results_size()
    316970


The main attribute of the class, `results`, returns a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_.  They can be efficiently converted into DataFrames using `pandas <https://pandas.pydata.org/>`_:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.DataFrame(s.results)
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
    (128, 36)
    >>> pd.set_option('display.max_columns', None)  # just for display
    >>> df.head()
                      eid                               doi                pii  \
    0  2-s2.0-85211039740  10.1016/j.scriptamat.2024.116486  S1359646224005219
    1  2-s2.0-85214107782        10.1016/j.tacc.2024.101515  S2210844024001849
    2  2-s2.0-85214598506                              None               None
    3  2-s2.0-85210715388      10.1371/journal.pone.0312945               None
    4  2-s2.0-85204999049       10.1016/j.softx.2024.101907  S2352711024002772

      pubmed_id                                              title subtype  \
    0      None  Data-driven compositional optimization of La(F...      ar
    1      None  Identifying and analyzing extremely productive...      ar
    2      None       Problem Structuring: Methodology in Practice      bk
    3  39621723  Instant prediction of scientific paper cited p...      ar
    4      None  core_api_client: An API for the CORE aggregati...      ar

      subtypeDescription          creator                         afid  \
    0            Article    Srinithi A.K.            60014256;60002414
    1            Article  Zarantonello F.            60027298;60000481
    2               Book     Yearworth M.                         None
    3            Article           Zhu H.  60023932;60021182;126223799
    4            Article          Vake D.  60030129;60006286;126197686

                                               affilname  \
    0  University of Tsukuba;National Institute for M...
    1  Azienda Ospedale Università Padova;Università ...
    2                                               None
    3  University of Technology Sydney;Sun Yat-Sen Un...
    4  Znanstvenoraziskovalni Center Slovenske Akadem...

                 affiliation_city         affiliation_country author_count  \
    0             Tsukuba;Tsukuba                 Japan;Japan            8
    1                 Padua;Padua                 Italy;Italy            8
    2                        None                        None            1
    3  Sydney;Guangzhou;Guangzhou       Australia;China;China            2
    4       Ljubljana;Koper;Izola  Slovenia;Slovenia;Slovenia            4

                                            author_names  \
    0  Srinithi, A. K.;Bolyachkin, A.;Tang, Xin;Sepeh...
    1  Zarantonello, Francesco;Sella, Nicolò;De Cassa...
    2                                    Yearworth, Mike
    3                               Zhu, Hou;Shuhuai, Li
    4  Vake, Domen;Hrovatin, Niki;Tošić, Aleksandar;V...

                                              author_ids  \
    0  57202111701;56418506200;55613058100;3497743530...
    1  57041172900;57218452414;57200001548;5934273760...
    2                                         6602655577
    3                            56359276400;59451089800
    4    58718905200;57225191729;55559996100;24484099500

                                            author_afids   coverDate  \
    0  60002414-60014256;60002414;60002414;60002414-6...  2025-03-15
    1  60027298;60027298;60027298-60000481;60000481;6...  2025-02-01
    2                                               None  2025-01-01
    3               60021182-60023932;60021182-126223799  2024-12-01
    4  60006286;60006286-126197686;60006286-126197686...  2024-12-01

      coverDisplayDate                               publicationName      issn  \
    0    15 March 2025                            Scripta Materialia  13596462
    1    February 2025       Trends in Anaesthesia and Critical Care  22108440
    2   1 January 2025  Problem Structuring: Methodology in Practice      None
    3    December 2024                                      PLoS ONE      None
    4    December 2024                                     SoftwareX      None

         source_id     eIssn aggregationType volume issueIdentifier  \
    0        28379      None         Journal    258            None
    1  19700200839  22108467         Journal     60            None
    2  21101268725      None            Book   None            None
    3  10600153309  19326203         Journal     19              12
    4  21100422153  23527110         Journal     28            None

      article_number pageRange                                        description  \
    0         116486      None  Magnetocaloric liquefaction of industrial and ...
    1         101515      None  Introduction: Clinical progress relies heavily...
    2           None     1-337  Current perspectives on approaches to problem ...
    3       e0312945      None  With the continuous increase in the number of ...
    4         101907      None  Recent efforts to make research publications p...

                                            authkeywords  citedby_count  \
    0  Gas liquefaction | La(Fe,Si) -based compounds ...              0
    1  Academics | H-index | Hyperprolific | Metrics ...              0
    2                                               None              0
    3                                               None              0
    4  API | Data analysis | Scientific publication |...              0

       openaccess               freetoread              freetoreadLabel fund_acr  \
    0           0                     None                         None     MEXT
    1           1  all publisherhybridgold  All Open Access Hybrid Gold     None
    2           0                     None                         None     None
    3           1    all publisherfullgold         All Open Access Gold     NSFC
    4           1                     None                         None       EC

               fund_no                                       fund_sponsor
    0  JPMXP1122715503  Ministry of Education, Culture, Sports, Scienc...
    1             None                                               None
    2             None                                               None
    3  2021A1515011805   Natural Science Foundation of Guangdong Province
    4           739574                                European Commission


It's important to note that the search results include no more than 100 authors.

The EIDs of documents can be used for the :doc:`AbstractRetrieval() <AbstractRetrieval>` class and the Scopus Author IDs in column "authid" for the :doc:`AuthorRetrieval() <AuthorRetrieval>` class.

Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.

Occasionally, some fields may be missing in the returned results, even though they exist in the Scopus database.  For example, the EID may be missing, even though every element always has an EID.  This is not a bug of `pybliometrics`.  Instead it is somehow related to a problem in the download process from the Scopus database.  For completeness checks of specific fields, use the `integrity_fields` parameter, which accepts any iterable.  Using parameter `integrity_action` you can choose between two actions if the integrity check fails: Set `integrity_action="warn"` to issue a UserWarning, or set `integrity_action="raise"` to raise an AttributeError.

.. code-block:: python

    >>> s = ScopusSearch(q, integrity_fields=["eid"],
                         integrity_action="warn")


If you care about integrity of specific fields, you can attempt to refresh the downloaded file:

.. code-block:: python

    def robust_query(q, refresh=False, fields=["eid"]):
        """Wrapper function for individual ScopusSearch query."""
        try:
            return ScopusSearch(q, refresh=refresh, integrity_fields=fields).results
        except AttributeError:
            return ScopusSearch(q, refresh=True, integrity_fields=fields).results


The Scopus Search API offers varying depths of information through
`views <https://dev.elsevier.com/guides/ScopusSearchViews.htm>`_.  The view 'COMPLETE' is the highest unrestricted view and contains all information also included in the 'STANDARD' view.  It is therefore the default view.  However, when speed is an issue, choose the STANDARD view.

For convenience, the `s.get_eids()` method returns the list of EIDs:

.. code-block:: python

    >>> s.get_eids()
    ['2-s2.0-85184035025', '2-s2.0-85187781098', '2-s2.0-85191356593',
     '2-s2.0-85185298843', '2-s2.0-85176114500', '2-s2.0-85187960595',
	 '2-s2.0-85187507366', '2-s2.0-85187306554', '2-s2.0-85181899797',
    #...
    '2-s2.0-85087770000', '2-s2.0-85086243347', '2-s2.0-85084027658']
