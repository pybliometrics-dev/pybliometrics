pybliometrics.scopus.SerialTitle
================================

`SerialTitle()` implements the `Serial Title API <https://dev.elsevier.com/documentation/SerialTitleAPI.wadl>`_.  It offers basic information on registered serials (also known as sources), including publisher details, identifiers, and various metrics.

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

    >>> import pybliometrics
    >>> from pybliometrics.scopus import SerialTitle
    >>> pybliometrics.scopus.init()
    >>> source = SerialTitle("00368075")

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(source)
    'Science', journal published by 'American Association for the Advancement of Science', is active in Multidisciplinary
	Metrics as of 2024-05-11:
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


Crucially, it provides three metrics: CiteScore (see `here <https://service.elsevier.com/app/answers/detail/a_id/30562/supporthub/scopus/>`_ for further information), SCImago Journal Rank indicator (see `here <https://www.scimagojr.com/journalrank.php>`_), and Source Normalized Impact Factor (SNIP; see `here <https://blog.scopus.com/posts/journal-metrics-in-scopus-source-normalized-impact-per-paper-snip>`_).  This information is presented in lists of two-element tuples, with the first element indicating the year of metric evaluation.

.. code-block:: python

    >>> source.citescoreyearinfolist
    [Citescoreinfolist(year=2022, citescore=59.0),
     Citescoreinfolist(year=2023, citescore=60.9)]
    >>> source.sjrlist
    [(2022, 13.328)]
    >>> source.sniplist
    [(2022, 7.729)]


The `citescoreyearinfolist` property provides detailed information for all available years when `view="CITESCORE"` is used.  It includes the status of the metric, the document count and citation count (of the previous 4 years), the share of documents actually cited, and the rank and percentile for each related ASJC subject:

.. code-block:: python

    >>> source_full = SerialTitle("00368075", view="CITESCORE")
    >>> info = pd.DataFrame(source_full.citescoreyearinfolist)
    >>> print(info)
        year  citescore       status  documentcount  citationcount  percentcited                             rank
    0   2023       60.9  In-Progress           4969         302467            79                  [(1000, 2, 99)]
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


The `yearly_data` time series includes the number of documents published in a given year.  It contains the number of documents published in this year, the share of review articles thereof, the number and share of not-cited documents, and the number of distinct documents that were cited in this year.


.. code-block:: python

    >>> source.yearly_data[-1]
	Yearlydata(year=2024, publicationcount=473, revpercent=4.02,
			   zerocitessce=400, zerocitespercentsce=84.56659619450318,
			   citecountsce=246787)
    >>> yearly_data = pd.DataFrame(source.yearly_data)
    >>> yearly_data.head()
       year  publicationcount  revpercent  zerocitessce  zerocitespercentsce  citecountsce
	0  1996              2395        4.97           653            27.265136        236672
	1  1997              2833        6.28           899            31.733145        244122
	2  1998              2816        4.69           850            30.184659        254600
	3  1999              2373        6.28           531            22.376738        276110
	4  2000              2401        7.00           457            19.033736        294076


By default, `SerialTitle()` retrieves only the most recent metrics, although yearly data is availble from 1996 onwards.  If you provide a year or a range of years via the optional parameter `years`, `SerialTitle()` will retrieve information for these years (except for the CiteScore):

.. code-block:: python

    >>> source_y = SerialTitle("00368075", years="2017-2019")
    >>> source_y.citescoreyearinfolist
    [Citescoreinfolist(year=2022, citescore=59.0),
     Citescoreinfolist(year=2023, citescore=58.8)]
    >>> source_y.sjrlist
    [(2017, 14.142), (2018, 13.251), (2019, 13.11)]
    >>> source_y.sniplist
    [(2017, 7.409), (2018, 7.584), (2019, 7.535)]


Fields associated with the source are stored as a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> source.subject_area
    [Subjectarea(area='Multidisciplinary', abbreviation='MULT', code=1000)]

Additionally, there is information on Open Access status, which, however, is often empty.

Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.
