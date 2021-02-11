Serial Search
-------------

:doc:`SerialSearch() <../reference/pybliometrics.SerialSearch>` implements the search of the `Serial Title API <https://dev.elsevier.com/documentation/SerialTitleAPI.wadl>`_.  It performs a search for serial sources (journal, tradejournal, conferenceproceeding, bookseries) by title, ISSN, publisher, subject or source type.

The class is initialized with a search query dictionary.  Its keys are limited to the following set: "title", "issn", "pub", "subj", "subjCode", "content", and "oa".  No more than 200 results can be returned.

.. code-block:: python

    >>> from pybliometrics.scopus import SerialSearch
    >>> s = SerialSearch(query={"title": "SoftwareX"})


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(s)
    Search '{'title': 'SoftwareX'}' yielded 1 source as of 2020-07-07:
        SoftwareX


Users can receive the number of results programmatically via `.get_results_size()`:

.. code-block:: python

    >>> s.get_results_size()
    1


The class' main attribute `results` returns a list of `OrderedDict <https://docs.python.org/3/library/collections.html#collections.OrderedDict>`_.  Provided information can differ greatly between results and depending on the view (see below) they can be numerous.  (Lists of )OrderedDict can be used neatly with `pandas <https://pandas.pydata.org/>`_ to form DataFrames:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.DataFrame(pd.DataFrame(s.results))
    >>> df.columns
    Index(['title', 'publisher', 'coverageStartYear', 'coverageEndYear',
           'aggregationType', 'source-id', 'eIssn', 'openaccess',
           'openaccessArticle', 'subject_area_codes',
           ...
           'publicationCount_2019', 'citeCountSCE_2019', 'zeroCitesSCE_2019',
           'zeroCitesPercentSCE_2019', 'revPercent_2019', 'publicationCount_2020',
           'citeCountSCE_2020', 'zeroCitesSCE_2020', 'zeroCitesPercentSCE_2020',
           'revPercent_2020'],
          dtype='object', length=142)
    >>> pd.set_option('display.max_columns', None)
    >>> df.iloc[:,:16]
       title    publisher coverageStartYear coverageEndYear aggregationType  \
    0  SoftwareX  Elsevier BV              2015            2020         journal   

         source-id      eIssn openaccess  openaccessArticle subject_area_codes  \
    0  21100422153  2352-7110          1               True          1712;1706   

      subject_area_abbrevs                      subject_area_names SNIP_2018  \
    0                 COMP  Software;Computer Science Applications     4.905   

      SJR_2018 citeScoreTracker_2019 citeScoreCurrentMetric_2018  
    0    4.539                  2.18                       11.56 


Information beyond the first 16 columns refer to journal metrics: publication counts, citation counts, not-cited documents, share of not-cited documents, and the share of review article documents, for each year since indexation.

Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `s.get_cache_file_mdate()` to get the date of last modification, and `s.get_cache_file_age()` the number of days since the last modification.

The Serial Title API allows a differing information depth via
`views <https://dev.elsevier.com/guides/SerialTitleViews.htm>`_.  While all views are restricted, view 'ENHANCED' is the highest among them. In addition to the information contained in 'STANDARD' it contains yearly journal metrics.  If you are not interested in this information, or when speed is an issue, choose the 'STANDARD' view.
