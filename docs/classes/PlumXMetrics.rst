pybliometrics.scopus.PlumXMetrics
=================================

`PlumXMetrics()` implements the `PlumX Metrics API <https://dev.elsevier.com/documentation/PlumXMetricsAPI.wadl>`_.  It provides metrics in five categories: captures, citations, usage, mentions, and social media (`background information <https://plumanalytics.com/learn/about-metrics/>`_).  It works for 32 different types of media.

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

    >>> from pybliometrics.scopus import PlumXMetrics
    >>> plum = PlumXMetrics("2-s2.0-85054706190", id_type='elsevierId')


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(plum)
    Document with elsevierId 2-s2.0-85054706190 received:
    - 460 citation(s) in category 'capture'
    - 232 citation(s) in category 'citation'
    - 2 citation(s) in category 'mention'
    - 42 citation(s) in category 'socialMedia'
    - 216 citation(s) in category 'usage'
    as of 2023-10-20


To each of the five categories, there is one property storing number and origin of the metrics in `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_.  If in a category there are no entries the property is simply `None`:

.. code-block:: python

    >>> >>> plum.capture
    [Metric(name='READER_COUNT', total=459),
     Metric(name='EXPORTS_SAVES', total=1)]
    >>> plum.citation
    [Metric(name='Scopus', total=231),
     Metric(name='CrossRef', total=80),
     Metric(name='Policy Citation', total=1)]
    >>> plum.mention
    [[Metric(name='NEWS_COUNT', total=2)]
    >>> plum.social_media
    [Metric(name='FACEBOOK_COUNT', total=42)]
    >>> plum.usage
    [Metric(name='ABSTRACT_VIEWS', total=205),
     Metric(name='LINK_OUTS', total=11)]


Finally there is a property to total all metrics on an aggregated level:

.. code-block:: python

    >>> plum.category_totals
    [Category(name='capture', total=460),
     Category(name='citation', total=232),
     Category(name='mention', total=2),
     Category(name='socialMedia', total=42),
     Category(name='usage', total=216)]


There are no bibliometric information such as title or author.

Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `source.get_cache_file_mdate()` to get the date of last modification, and `source.get_cache_file_age()` the number of days since the last modification.
