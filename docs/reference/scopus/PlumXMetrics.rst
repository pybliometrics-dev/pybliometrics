pybliometrics.scopus.PlumXMetrics
=================================

`PlumXMetrics()` implements the `PlumX Metrics API <https://dev.elsevier.com/documentation/PlumXMetricsAPI.wadl>`_.  It offers metrics across five categories: captures, citations, usage, mentions, and social media -- see `here <https://plumanalytics.com/learn/about-metrics/>`_ for background information.  It works for many different types of media.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: PlumXMetrics
    :members:
    :inherited-members:

Examples
--------

You initialize the class with the identifier of a document and its type:

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import PlumXMetrics
    >>> pybliometrics.scopus.init()
    >>> plum = PlumXMetrics("2-s2.0-85054706190", id_type='elsevierId')


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(plum)
    Document with elsevierId 2-s2.0-85054706190 received:
	- 469 citation(s) in category 'capture'
	- 248 citation(s) in category 'citation'
	- 2 citation(s) in category 'mention'
	- 185,819 citation(s) in category 'socialMedia'
	as of 2024-05-11


For each of the five categories, there is a corresponding property that stores the number and origin of the metrics in `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_.  If a category has no entries, the corresponding property will be `None`:

.. code-block:: python

    >>> plum.capture
    [Metric(name='READER_COUNT', total=469)]
    >>> plum.citation
    [Metric(name='Scopus', total=247),
	 Metric(name='CrossRef', total=80),
     Metric(name='Policy Citation', total=1)]
    >>> plum.mention
    [Metric(name='NEWS_COUNT', total=2)]
    >>> plum.social_media
    [Metric(name='FACEBOOK_COUNT', total=185819)]
    >>> plum.usage
    


Finally, there is a property that totals all metrics at an aggregated level:

.. code-block:: python

    >>> plum.category_totals
    [Category(name='capture', total=469),
	 Category(name='citation', total=248),
	 Category(name='mention', total=2),
	 Category(name='socialMedia', total=185819)]


There are no bibliometric information such as title or author.

Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.