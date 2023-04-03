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
    'Science', journal published by 'American Association for the Advancement of Science', is active in Multidisciplinary and Medicine (all)
    Metrics as of 2023-04-03:
        SJR:  year value
              2021 14.589
        SNIP: year value
              2021 9.116
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
    [(2021, 57.8), (2022, 57.3)]
    >>> source.sjrlist
    [(2021, 14.589)]
    >>> source.sniplist
    [(2021, 9.116)]


The only longer time series is provide in paramter `yearly_data`. It contains the number of documents published in this year, the share of review articles thereof, the number and share of not-cited documents, and the number of distinct documents that were cited in this year.


.. code-block:: python

    >>> source.yearly_data[-1]
    Yearlydata(year=2023, publicationcount=0, revpercent=0.0,
               zerocitessce=0, zerocitespercentsce=None, citecountsce=30145)
    >>> yearly_data = pd.DataFrame(source.yearly_data)
    >>> yearly_data.head()
       year  publicationcount  revpercent  zerocitessce  zerocitespercentsce  citecountsce
    0  1996              2395        4.97           661            27.599165        235971
    1  1997              2833        6.28           905            31.944935        243521
    2  1998              2816        4.69           855            30.362216        253994
    3  1999              2373        6.28           534            22.503161        275590
    4  2000              2401        7.00           462            19.241983        293442



By default, `SerialTitle()` retrieves only the most recent metrics while yearly data is availble from 1996 onwards.  If you provide a year or a range of years via the optional parameter `years`, `SerialTitle()` will retrieve information for these years (except for the CiteScore):

.. code-block:: python

    >>> source_y = SerialTitle("00368075", years="2017-2019")
    >>> source_y.citescoreyearinfolist
    [(2020, 46.8), (2021, 51.9)]
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
