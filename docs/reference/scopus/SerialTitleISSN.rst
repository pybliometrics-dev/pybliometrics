pybliometrics.scopus.SerialTitleISSN
====================================

`SerialTitleISSN()` implements the `issn` endpoint of the `Serial Title API <https://dev.elsevier.com/documentation/SerialTitleAPI.wadl>`_.  It offers basic information on registered serials (also known as sources), including publisher details, identifiers, and various metrics.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: SerialTitleISSN
    :members:
    :inherited-members:

Examples
--------

You initialize the class with an ISSN or an E-ISSN (works with and without hyphen, but leading zeros are mandatory):

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import SerialTitleISSN
    >>> pybliometrics.scopus.init()
    >>> source = SerialTitleISSN("00368075")

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(source)
    'Science', journal published by 'American Association for the Advancement of Science', is active in Multidisciplinary
    Metrics as of 2026-10-02:
        SJR:  year value
              2025 10.948
        SNIP: year value
              2025 6.984
        ISSN: 0036-8075, E-ISSN: 1095-9203, Scopus ID: 23571

The object has a number of attributes but no methods.  For example, information regarding the source itself:

.. code-block:: python

    >>> source.title
    'Science'
    >>> source.publisher
    'American Association for the Advancement of Science'
    >>> source.issn
    '0036-8075'
    >>> source.eissn
    '1095-9203'
    >>> source.source_id
    23571


Crucially, it provides three metrics: `CiteScore <https://service.elsevier.com/app/answers/detail/a_id/30562/supporthub/scopus/>`_, `SCImago Journal Rank indicator <https://www.scimagojr.com/journalrank.php>`_), and Source Normalized Impact Factor (`SNIP <https://blog.scopus.com/posts/journal-metrics-in-scopus-source-normalized-impact-per-paper-snip>`_).  This information is presented in lists of two-element tuples, with the first element indicating the year of metric evaluation.

.. code-block:: python

    >>> source.citescoreyearinfolist
    [Citescoreinfolist(year=2025, citescore=44.6, status=None, documentcount=None,
                       citationcount=None, percentcited=None, rank=None),
     Citescoreinfolist(year=2026, citescore=39.5, status=None, documentcount=None,
                       citationcount=None, percentcited=None, rank=None)]
    >>> source.sjrlist
    [(2025, 10.948)]
    >>> source.sniplist
    [(2025, 6.984)]


The `citescoreyearinfolist` property provides detailed information for all available years when `view="CITESCORE"` is used.  It includes the status of the metric, the document count and citation count (of the previous 4 years), the share of documents actually cited, and the rank and percentile for each related ASJC subject:

.. code-block:: python

    >>> import pandas as pd
    >>> source_full = SerialTitleISSN("00368075", view="CITESCORE")
    >>> info = pd.DataFrame(source_full.citescoreyearinfolist)
    >>> print(info)
        year  citescore       status  documentcount  citationcount  percentcited                             rank
    0   2026       39.5  In-Progress           4646         183562            77                  [(1000, 2, 99)]
    1   2025       44.6     Complete           5021         223874            80                  [(1000, 2, 99)]
    2   2024       48.4     Complete           4865         235433            80                  [(1000, 3, 98)]
    3   2023       61.1     Complete           4969         303378            79                  [(1000, 2, 99)]
    4   2022       59.0     Complete           4895         288748            82                  [(1000, 2, 98)]
    5   2021       57.8     Complete           4823         278545            84                  [(1000, 2, 98)]
    6   2020       46.8     Complete           4833         226134            82                  [(1000, 2, 98)]
    7   2019       45.3     Complete           4799         217261            81                  [(1000, 2, 98)]
    8   2018       47.1     Complete           4681         220642            82                  [(1000, 2, 98)]
    9   2017       49.4     Complete           4215         208286            90                  [(1000, 2, 98)]
    10  2016       49.5     Complete           4176         206665            89                  [(1000, 1, 99)]
    11  2015       46.6     Complete           4016         187040            89  [(2700, 18, 99), (1000, 2, 98)]
    12  2014       46.0     Complete           3923         180376            90  [(2700, 18, 99), (1000, 2, 98)]
    13  2013       46.9     Complete           3839         179860            92  [(2700, 16, 99), (1000, 2, 98)]
    14  2012       46.3     Complete           3861         178780            92  [(2700, 11, 99), (1000, 2, 98)]
    15  2011       44.7     Complete           3843         171898            91  [(2700, 12, 99), (1000, 2, 98)]


The `yearly_data` time series includes the number of documents published in a given year.  It contains the number of documents published in this year, the share of review articles thereof, the number and share of not-cited documents, and the number of distinct documents that were cited in this year.


.. code-block:: python

    >>> source.yearly_data[-1]
    Yearlydata(year=2026, publicationcount=1340, revpercent=1.27,
               zerocitessce=857, zerocitespercentsce=63.95522388059702,
               citecountsce=659341)
    >>> yearly_data = pd.DataFrame(source.yearly_data)
    >>> yearly_data.head()
       year  publicationcount  revpercent  zerocitessce  zerocitespercentsce  citecountsce
    0  1996              2393        4.97           645            26.953615        237425
    1  1997              2834        6.28           887            31.298518        244923
    2  1998              2816        4.69           836            29.687500        255425
    3  1999              2373        6.24           521            21.955331        277194
    4  2000              2400        7.00           447            18.625000        295312


By default, `SerialTitleISSN()` retrieves only the most recent metrics, although yearly data is availble from 1996 onwards.  If you provide a year or a range of years via the optional parameter `years`, `SerialTitleISSN()` will retrieve information for these years (except for the CiteScore):

.. code-block:: python

    >>> source_y = SerialTitleISSN("00368075", years="2017-2019")
    >>> source_y.citescoreyearinfolist
    [Citescoreinfolist(year=2025, citescore=44.6, status=None, documentcount=None,
                       citationcount=None, percentcited=None, rank=None),
     Citescoreinfolist(year=2026, citescore=39.5, status=None, documentcount=None,
                       citationcount=None, percentcited=None, rank=None)]
    >>> source_y.sjrlist
    [(2017, 14.142), (2018, 13.251), (2019, 13.11)]
    >>> source_y.sniplist
    [(2017, 7.617), (2018, 7.802), (2019, 7.806)]


Fields associated with the source are stored as a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> source.subject_area
    [Subjectarea(area='Multidisciplinary', abbreviation='MULT', code=1000)]

Additionally, there is information on Open Access status, which, however, is often empty.

Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.
