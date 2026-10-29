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
    100%|████████████████████████████████████████████████████████████████████████████████████████████████| 8/8 [00:07<00:00,  1.07s/it]


You can obtain a search summary just by printing the object:

.. code-block:: python

    >>> print(s)
    Search 'REF(2-s2.0-85068268027)' yielded 198 documents as of 2026-10-02:
            2-s2.0-105049335505
            2-s2.0-105039514301
            2-s2.0-105035584672
            2-s2.0-105029768595
            2-s2.0-105047159917
            2-s2.0-105045229691
            2-s2.0-105047717043
            2-s2.0-105046638449
            2-s2.0-105044794764
            2-s2.0-105036644817
            2-s2.0-105034620396
    # output truncated


Non-subscribers must instantiate the class with `subscriber=False`.  They may only get 5,000 results per query, whereas this limit does not exist for subscribers.

Users can determine the number of results programmatically using the `.get_results_size()` method:

.. code-block:: python

    >>> s.get_results_size()
    198


This method works even if one chooses to not download results.  It thus helps subscribers to decide programmatically if one wants to proceed downloading or not:

.. code-block:: python

    >>> other = ScopusSearch('AUTHLASTNAME(Brown)', download=False)
    >>> other.get_results_size()
    347009


The main attribute of the class, `results`, returns a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_.  They can be efficiently converted into DataFrames using `pandas <https://pandas.pydata.org/>`_:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.DataFrame(s.results)
    >>> df.columns
    Index(['eid', 'doi', 'pii', 'pubmed_id', 'title', 'subtype',
           'subtypeDescription', 'creator', 'afid', 'affilname',
           'affiliation_city', 'affiliation_country', 'author_count',
           'author_names', 'author_ids', 'author_afids', 'coverDate',
           'coverDisplayDate', 'publicationName', 'issn', 'source_id', 'eIssn',
           'aggregationType', 'volume', 'issueIdentifier', 'article_number',
           'pageRange', 'description', 'authkeywords', 'citedby_count',
           'openaccess', 'freetoread', 'freetoreadLabel', 'fund_acr', 'fund_no',
           'fund_sponsor'],
          dtype='str')
    >>> df.shape
    (198, 36)
    >>> pd.set_option('display.max_columns', None)  # just for display
    >>> df.head()
                       eid                             doi                pii  \
    0  2-s2.0-105049335505  10.1016/j.apenergy.2026.128709  S0306261926013656
    1  2-s2.0-105039514301      10.1038/s41597-026-07083-9                NaN
    2  2-s2.0-105035584672      10.1057/s41599-026-06490-y                NaN
    3  2-s2.0-105029768595      10.1007/s11846-026-00994-2                NaN
    4  2-s2.0-105047159917     10.1016/j.softx.2026.102932  S2352711026004231

      pubmed_id                                              title subtype  \
    0       NaN  A review of key economic indicators for assess...      re
    1  41876552  EKHI: an open database of optical and thermal ...      dp
    2       NaN  Deepening and broadening knowledge after the P...      ar
    3       NaN  Designing, managing and sustaining coopetition...      ar
    4       NaN  BiblioSelect: A graphical tool for paper scree...      ar

      subtypeDescription              creator  \
    0             Review        Bonini V.R.B.
    1         Data Paper   Gabirondo-López J.
    2            Article           Baker D.P.
    3            Article     Konyalıoğlu A.K.
    4            Article  Cavalcante E.M.d.S.

                                      afid  \
    0                             60017609
    1                             60027856
    2  60016849;60001439;60012392;60072562
    3                    60022002;60113247
    4                             60008088

                                               affilname  \
    0             Universidade Federal de Santa Catarina
    1                         Universidad del Pais Vasco
    2  University of Toronto;Pennsylvania State Unive...
    3  İstanbul Teknik Üniversitesi;Strathclyde Busin...
    4                          Universidade de São Paulo

                                      affiliation_city  \
    0                                    Florianopolis
    1                                            Leioa
    2  Toronto;University Park;Taipei;Esch-sur-Alzette
    3                                 Istanbul;Glasgow
    4                                        Sao Paulo

                          affiliation_country author_count  \
    0                                  Brazil            4
    1                                   Spain           11
    2  Canada;United States;Taiwan;Luxembourg            9
    3                   Turkey;United Kingdom            3
    4                                  Brazil            8

                                            author_names  \
    0  Bonini, Vinicius R.B.;de Sousa, Rosângela A.;S...
    1  Gabirondo-López, Jon;Sainz-Menchón, Mireia;Tol...
    2  Baker, David P.;Adeel, Abdul Basit;Moradel-Vás...
    3   Konyalıoğlu, Aziz Kemal;Ates, Aylin;Paton, Steve
    4  Cavalcante, Edson Magrine de Souza;Silva dos S...

                                              author_ids  \
    0     57681132200;60826413300;57190933365;7402942472
    1  57226765695;57923448600;60641571300;5718906399...
    2  35329313500;57221311634;58102000200;5810182220...
    3                57210103956;36927494600;18438052200
    4  60787619600;60711976500;60788006600;3510361000...

                                            author_afids   coverDate  \
    0                60017609;60017609;60017609;60017609  2026-12-01
    1  60027856;60027856;60027856;60027856;60027856;6...  2026-12-01
    2  60001439;60001439;60072562;60072562;60072562;6...  2026-12-01
    3                60113247-60022002;60113247;60113247  2026-10-01
    4  60008088;60008088;60008088;60008088;60008088;6...  2026-09-01

      coverDisplayDate                                publicationName      issn  \
    0    December 2026                                 Applied Energy  03062619
    1    December 2026                                Scientific Data       NaN
    2    December 2026  Humanities and Social Sciences Communications       NaN
    3     October 2026                   Review of Managerial Science  18636683
    4   September 2026                                      Softwarex       NaN

         source_id     eIssn aggregationType volume issueIdentifier  \
    0        28801       NaN         Journal    426             NaN
    1  21100451321  20524463         Journal     13               1
    2  21101018925  26629992         Journal     13               1
    3  17400154830  18636691         Journal     20              10
    4  21100422153  23527110         Journal     35             NaN

      article_number  pageRange  \
    0         128709        NaN
    1            740        NaN
    2            381        NaN
    3            NaN  3811-3850
    4         102932        NaN

                                             description  \
    0  Hydrogen has been considered a promising solut...
    1  We present a curated and openly accessible dat...
    2  The intensification of science as a social ins...
    3  This study integrates insights from a large-sc...
    4  BiblioSelect is a graphical, client-side tool ...

                                            authkeywords  citedby_count  \
    0  Economic assessment | Fuel-cell vehicles | Hyd...              0
    1                                                NaN              1
    2                                                NaN              0
    3  Coopetition | Ecosystem | Innovation | Machine...              1
    4  Bibliometrics | Literature screening | Open sc...              0

       openaccess                                       freetoread  \
    0           1                          all publisherhybridgold
    1           1    all publisherfullgold repository repositoryam
    2           1    all publisherfullgold repository repositoryam
    3           1  all publisherhybridgold repository repositoryam
    4           1    all publisherfullgold repository repositoryam

                         freetoreadLabel fund_acr          fund_no  \
    0        All Open Access Hybrid Gold     CNPq    405859/2022-8
    1         All Open Access Gold Green      EHU  PRE-2022-1-0086
    2         All Open Access Gold Green      NaN              NaN
    3  All Open Access Hybrid Gold Green      NaN              NaN
    4         All Open Access Gold Green      NaN              NaN

                                            fund_sponsor
    0  Conselho Nacional de Desenvolvimento Científic...
    1                                  Eusko Jaurlaritza
    2                                                NaN
    3                                                NaN
    4                                                NaN


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
    ['2-s2.0-105049335505', '2-s2.0-105039514301', '2-s2.0-105035584672',
     '2-s2.0-105029768595', '2-s2.0-105047159917', '2-s2.0-105045229691',
     '2-s2.0-105047717043', '2-s2.0-105046638449', '2-s2.0-105044794764',
    #...
     '2-s2.0-85087770000', '2-s2.0-85086243347', '2-s2.0-85084027658']
