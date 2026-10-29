pybliometrics.scopus.SerialTitleSearch
======================================

`SerialTitleSearch()` implements the search of the `Serial Title API <https://dev.elsevier.com/documentation/SerialTitleAPI.wadl>`_.  This class performs searches for serial sources (journals, trade journals, conference proceedings, book series) based on title, ISSN, publisher, subject, or source type.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: SerialTitleSearch
    :members:
    :inherited-members:

Examples
--------

The class is initialized with a search query dictionary.  Its keys are limited to the following set: "title", "issn", "pub", "subj", "subjCode", "content", and "oa".  No more than 200 results can be returned.

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import SerialTitleSearch
    >>> pybliometrics.scopus.init()
    >>> s = SerialTitleSearch(query={"title": "SoftwareX"})


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(s)
    Search '{'title': 'SoftwareX'}' yielded 1 source as of 2026-10-02:
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
    (1, 172)
    >>> df.columns
    Index(['title', 'publisher', 'coverageStartYear', 'coverageEndYear',
           'aggregationType', 'source-id', 'eIssn', 'openaccess',
           'openaccessArticle', 'subject_area_codes',
           ...
           'publicationCount_2025', 'citeCountSCE_2025', 'zeroCitesSCE_2025',
           'zeroCitesPercentSCE_2025', 'revPercent_2025', 'publicationCount_2026',
           'citeCountSCE_2026', 'zeroCitesSCE_2026', 'zeroCitesPercentSCE_2026',
           'revPercent_2026'],
          dtype='str', length=172)
    >>> pd.set_option('display.max_columns', None)
    >>> df.iloc[:,:16]
           title      publisher coverageStartYear coverageEndYear aggregationType  \
    0  SoftwareX  Elsevier B.V.              2015            2026         journal

         source-id      eIssn openaccess  openaccessArticle subject_area_codes  \
    0  21100422153  2352-7110          1               True          1712;1706

      subject_area_abbrevs                      subject_area_names SNIP_['@year']  \
    0                 COMP  Software;Computer Science Applications          0.977

      SJR_['@year'] citeScoreTracker_2026 citeScoreCurrentMetric_2025
    0         0.499                   3.0                         3.9


The information in columns beyond the first 16 pertains to journal metrics: publication counts, citation counts, not-cited documents, share of not-cited documents, and the share of review article documents, for each year since indexation.

Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.

The Serial Title API offers varying depths of information through
`views <https://dev.elsevier.com/guides/SerialTitleViews.htm>`_.  While all views are restricted, view 'ENHANCED' is the highest among them. In addition to the information contained in 'STANDARD' it contains yearly journal metrics.  If you are not interested in this information, or when speed is an issue, choose the 'STANDARD' view.
