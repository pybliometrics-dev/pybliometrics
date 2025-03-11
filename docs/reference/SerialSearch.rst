pybliometrics.scopus.SerialSearch
=================================

`SerialSearch()` implements the search of the `Serial Title API <https://dev.elsevier.com/documentation/SerialTitleAPI.wadl>`_.  This class performs searches for serial sources (journals, trade journals, conference proceedings, book series) based on title, ISSN, publisher, subject, or source type.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: SerialSearch
    :members:
    :inherited-members:

Examples
--------

The class is initialized with a search query dictionary.  Its keys are limited to the following set: "title", "issn", "pub", "subj", "subjCode", "content", and "oa".  No more than 200 results can be returned.

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import SerialSearch
    >>> pybliometrics.scopus.init()
    >>> s = SerialSearch(query={"title": "SoftwareX"})


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(s)
    Search '{'title': 'SoftwareX'}' yielded 1 source as of 2024-05-11:
        SoftwareX


Users can determine the number of results programmatically using the `.get_results_size()` method:

.. code-block:: python

    >>> s.get_results_size()
    1


The main attribute of the class, `results`, returns a list of `OrderedDict <https://docs.python.org/3/library/collections.html#collections.OrderedDict>`_ objects.  Provided information can differ greatly between results and depending on the view (see below) they can be numerous.  Lists of OrderedDict objects can be efficiently converted into DataFrames using `pandas <https://pandas.pydata.org/>`_:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.DataFrame(pd.DataFrame(s.results))
    >>> df.shape
    (1, 162)
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
    0  SoftwareX  Elsevier BV              2015            2024         journal   

         source-id      eIssn openaccess  openaccessArticle subject_area_codes  \
    0  21100422153  2352-7110          1               True          1712;1706   

      subject_area_abbrevs                      subject_area_names SNIP_['@year']  \
    0                 COMP  Software;Computer Science Applications          1.426

      SJR_['@year'] citeScoreTracker_2023 citeScoreCurrentMetric_2022
    0         0.574                   5.4                         5.1


The information in columns beyond the first 16 pertains to journal metrics: publication counts, citation counts, not-cited documents, share of not-cited documents, and the share of review article documents, for each year since indexation.

Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.

The Serial Title API offers varying depths of information through
`views <https://dev.elsevier.com/guides/SerialTitleViews.htm>`_.  While all views are restricted, view 'ENHANCED' is the highest among them. In addition to the information contained in 'STANDARD' it contains yearly journal metrics.  If you are not interested in this information, or when speed is an issue, choose the 'STANDARD' view.
