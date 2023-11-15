pybliometrics.scopus.SerialTitle
================================

`SerialTitle()` implements the `Serial Title API <https://dev.elsevier.com/documentation/SerialTitleAPI.wadl>`_.  It provides basic information on registered serials (also called sources), like publisher and identifiers, but also metrics.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: SerialTitle
   :members:
   :inherited-members:

Examples
--------

You initialize the class with an ISSN or an E-ISSN (works with and without hyphen, but leading zeros are mandatory):

.. code-block:: python

    >>> from pybliometrics.scopus import SerialTitle
    >>> source = SerialTitle("00368075")

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(source)
    'Science', journal published by 'American Association for the Advancement
    of Science', is active in Multidisciplinary
    Metrics as of 2023-11-15:
        SJR:  year value
              2022 13.328
        SNIP: year value
              2022 7.729
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


Most importantly, it provides three metrics: the CiteScore (see `here <https://service.elsevier.com/app/answers/detail/a_id/30562/supporthub/scopus/>`_ for further information), the SCImago Journal Rank indicator (see `here <https://www.scimagojr.com/journalrank.php>`_), and the Source Normalized Impact Factor (SNIP; see `here <https://blog.scopus.com/posts/journal-metrics-in-scopus-source-normalized-impact-per-paper-snip>`_).  The information is stored in lists of 2-element tuples with the first element indicating the year the metric was evaluated.

.. code-block:: python

    >>> source.citescoreyearinfolist
    [Citescoreinfolist(year=2022, citescore=59.0),
     Citescoreinfolist(year=2023, citescore=58.8)]
    >>> source.sjrlist
    [(2022, 13.328)]
    >>> source.sniplist
    [(2022, 7.729)]


Property `citescoreyearinfolist` can return detailed information for all available years with `view="CITESCORE"`. It includes the status of the metric, the document count and citation count (of the previous 4 years), the share of documents actually cited, and the rank and percentile for each related ASJC subject:

.. code-block:: python

    >>> source_full = SerialTitle("00368075", view="CITESCORE")
    >>> info = pd.DataFrame(source_full.citescoreyearinfolist)
    >>> print(info)
        year  citescore       status  documentcount  citationcount  percentcited                             rank
    0   2023       58.8  In-Progress           4730         278199            79                  [(1000, 2, 99)]
    1   2022       59.0     Complete           4895         288748            82                  [(1000, 2, 98)]
    2   2021       57.8     Complete           4823         278545            84                  [(1000, 2, 98)]
    3   2020       46.8     Complete           4833         226134            82                  [(1000, 2, 98)]
    4   2019       45.3     Complete           4799         217261            81                  [(1000, 2, 98)]
    5   2018       47.1     Complete           4681         220642            82                  [(1000, 2, 98)]
    6   2017       49.4     Complete           4215         208286            90                  [(1000, 2, 98)]
    7   2016       49.5     Complete           4176         206665            89                  [(1000, 1, 99)]
    8   2015       46.6     Complete           4016         187040            89  [(2700, 18, 99), (1000, 2, 98)]
    9   2014       46.0     Complete           3923         180376            90  [(2700, 18, 99), (1000, 2, 98)]
    10  2013       46.9     Complete           3839         179860            92  [(2700, 16, 99), (1000, 2, 98)]
    11  2012       46.3     Complete           3861         178780            92  [(2700, 11, 99), (1000, 2, 98)]
    12  2011       44.7     Complete           3843         171898            91  [(2700, 12, 99), (1000, 2, 98)]


Another time series is `yearly_data`. It contains the number of documents published in this year, the share of review articles thereof, the number and share of not-cited documents, and the number of distinct documents that were cited in this year.


.. code-block:: python

    >>> source.yearly_data[-1]
    Yearlydata(year=2023, publicationcount=1800, revpercent=2.94,
               zerocitessce=1201, zerocitespercentsce=66.72222222222223,
               citecountsce=726948)
    >>> yearly_data = pd.DataFrame(source.yearly_data)
    >>> yearly_data.head()
       year  publicationcount  revpercent  zerocitessce  zerocitespercentsce  citecountsce
    0  1996              2395        4.97           655            27.348643        236545
    1  1997              2833        6.28           904            31.909636        244078
    2  1998              2816        4.69           854            30.326705        254500
    3  1999              2373        6.28           532            22.418879        276054
    4  2000              2402        6.99           459            19.109076        293867


By default, `SerialTitle()` retrieves only the most recent metrics while yearly data is availble from 1996 onwards.  If you provide a year or a range of years via the optional parameter `years`, `SerialTitle()` will retrieve information for these years (except for the CiteScore):

.. code-block:: python

    >>> source_y = SerialTitle("00368075", years="2017-2019")
    >>> source_y.citescoreyearinfolist
    [Citescoreinfolist(year=2022, citescore=59.0),
     Citescoreinfolist(year=2023, citescore=58.8)]
    >>> source_y.sjrlist
    [(2017, 14.142), (2018, 13.251), (2019, 13.11)]
    >>> source_y.sniplist
    [(2017, 7.409), (2018, 7.584), (2019, 7.535)]


The fields associated with the source are stored as a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> source.subject_area
    [Subjectarea(area='Multidisciplinary', abbreviation='MULT', code=1000)]

Additionally there are many bits of information on Open Access status which are often empty however.

Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  If `years` is provided, `SerialSearch()` will always refresh.

Use `source.get_cache_file_mdate()` to get the date of last modification, and `source.get_cache_file_age()` the number of days since the last modification.
