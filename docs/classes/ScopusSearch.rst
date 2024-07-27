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
    100%|████████████████████████████████████████████████████████████████████████████████████████████████| 5/5 [00:03<00:00,  1.07s/it]


You can obtain a search summary just by printing the object:

.. code-block:: python

    >>> print(s)
    Search 'REF(2-s2.0-85068268027)' yielded 116 documents as of 2024-07-27:
		2-s2.0-85194707120
		2-s2.0-85184035025
		2-s2.0-85187781098
		2-s2.0-85147940888
		2-s2.0-85197104836
		2-s2.0-85191356593
		2-s2.0-85185298843
		2-s2.0-85176114500
		2-s2.0-85187960595
		2-s2.0-85187507366
		2-s2.0-85187306554
    # output truncated


Non-subscribers must instantiate the class with `subscriber=False`.  They may only get 5,000 results per query, whereas this limit does not exist for subscribers.

Users can determine the number of results programmatically using the `.get_results_size()` method:

.. code-block:: python

    >>> s.get_results_size()
    110


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
    (88, 36)
    >>> pd.set_option('display.max_columns', None)  # just for display
    >>> df.head()
                          eid                           doi                pii  \
    0  2-s2.0-85174697039   10.1016/j.softx.2023.101565  S2352711023002613   
    1  2-s2.0-85169560066  10.1016/j.respol.2023.104874  S0048733323001580   
    2  2-s2.0-85163820321    10.1186/s40537-023-00793-6               None   
    3  2-s2.0-85153853127           10.1162/qss_a_00236               None   
    4  2-s2.0-85174908092          10.3390/jmse11101855               None   

      pubmed_id                                              title subtype  \
    0      None  PyblioNet – Software for the creation, visuali...      ar   
    1      None  The role of gender and coauthors in academic p...      ar   
    2      None  Bibliometric mining of research directions and...      ar   
    3      None  How reliable are unsupervised author disambigu...      ar   
    4      None  Machine Learning Solutions for Offshore Wind F...      re   

      subtypeDescription      creator               afid  \
    0            Article    Müller M.           60018373   
    1            Article  Schmal W.B.  60025310;60006341   
    2            Article  Lundberg L.           60016636   
    3            Article    Abramo G.  60027509;60021199   
    4             Review   Masoumi M.           60017789   

                                               affilname     affiliation_city  \
    0                              Universität Hohenheim            Stuttgart   
    1  Heinrich-Heine-Universität Düsseldorf;Universi...  Dusseldorf;Mannheim   
    2                         Blekinge Tekniska Högskola           Karlskrona   
    3  Università degli Studi di Roma "Tor Vergata";C...            Rome;Rome   
    4                                  Manhattan College             New York   

      affiliation_country author_count  \
    0             Germany            1   
    1     Germany;Germany            3   
    2              Sweden            1   
    3         Italy;Italy            2   
    4       United States            1   

                                         author_names  \
    0                                Müller, Matthias   
    1  Schmal, W. Benedikt;Haucap, Justus;Knoke, Leon   
    2                                  Lundberg, Lars   
    3       Abramo, Giovanni;D’angelo, Ciriaco Andrea   
    4                                 Masoumi, Masoud   

                               author_ids                author_afids   coverDate  \
    0                         58302698300                    60018373  2023-12-01   
    1  57350833800;6602422284;57377238100  60025310;60025310;60006341  2023-12-01   
    2                          7103325657                    60016636  2023-12-01   
    3             22833445200;57219528028  60021199;60021199-60027509  2023-12-01   
    4                         56362456200                    60017789  2023-10-01   

      coverDisplayDate                            publicationName      issn  \
    0    December 2023                                  SoftwareX      None   
    1    December 2023                            Research Policy  00487333   
    2    December 2023                        Journal of Big Data      None   
    3      Winter 2023               Quantitative Science Studies      None   
    4     October 2023  Journal of Marine Science and Engineering      None   

         source_id     eIssn aggregationType volume issueIdentifier  \
    0  21100422153  23527110         Journal     24            None   
    1        22900      None         Journal     52              10   
    2  21100791292  21961115         Journal     10               1   
    3  21101062805  26413337         Journal      4               1   
    4  21100830140  20771312         Journal     11              10   

      article_number pageRange                                        description  \
    0         101565      None  PyblioNet is a software tool for the creation,...   
    1         104874      None  This paper contributes to the literature on di...   
    2            112      None  In this paper a program and methodology for bi...   
    3           None   144-166  Assessing the performance of universities by o...   
    4           1855      None  The continuous advancement within the offshore...   

                                            authkeywords  citedby_count  \
    0  Bibliometrics | Network | Python | Science map...              0   
    1  Academic publishing | DEAL | Elsevier | Gender...              0   
    2  Bibliometrics | Fields of science and technolo...              0   
    3  author name disambiguation | evaluative scient...              1   
    4  offshore energy | offshore wind | wind farm | ...              0   

       openaccess         freetoread freetoreadLabel fund_acr             fund_no  \
    0           1               None            None     None           undefined   
    1           0       repositoryam           Green      MSI  235577387/GRK 1974   
    2           1       repositoryam           Green      BTH           undefined   
    3           1       repositoryam           Green     None           undefined   
    4           1  publisherfullgold            Gold     None           undefined   

                                          fund_sponsor  
    0                                             None  
    1  Ministry of Science and Innovation, New Zealand  
    2                       Blekinge Tekniska Högskola  
    3                              Universiteit Leiden  
    4                                             None 


It's important to note that the search results include no more than 100 authors.

The EIDs of documents can be used for the :doc:`AbstractRetrieval() <../classes/AbstractRetrieval>` class and the Scopus Author IDs in column "authid" for the :doc:`AuthorRetrieval() <../classes/AuthorRetrieval>` class.

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
