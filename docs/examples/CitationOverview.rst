Citation Overview
-----------------

:doc:`CitationOverview() <../reference/pybliometrics.CitationOverview>` implements the `Citations Overview API <https://api.elsevier.com/documentation/AbstractCitationAPI.wadl>`_.  Your API Key needs to be approved by Elsevier manually.  Please contact Scopus to do so.  Otherwise each request throws 403 errors.

It takes a `Scopus EID <http://kitchingroup.cheme.cmu.edu/blog/2015/06/07/Getting-a-Scopus-EID-from-a-DOI/>`_ as argument and additionally a starting year and an ending year for which yearly citations will be retrieved.  If no ending year is given, `CitationOverview()` will use the current year.  Retrieving these results is not fast, so we cache them to speed up subsequent uses of the data.

You initialize the class with Scopus' Electronic Identifier (EID):

.. code-block:: python
   
    >>> from pybliometrics.scopus import CitationOverview
    >>> co = CitationOverview("2-s2.0-84930616647", start=2015, end=2017)


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(co)
    Document 'Examples of effective data sharing in scientific publishing' by Kitchin J.R.
    published in 'ACS Catalysis' has the following citation trajectory as of 2020-07-07:
        Before 2015 0; 2015: 0; 2016: 4; 2017: 2; After 2017: 3 times



The most important information is stored in attribute `cc`, which is a list of tuples storing year-wise citations to the article:

.. code-block:: python

    >>> co.cc
    [(2015, '0'), (2016, '4'), (2017, '2')]


Sometimes there are citations outside the specified year range, which you can get with `pcc` and `lcc`:

.. code-block:: python

    >>> co.pcc
    0
    >>> co.lcc
    0


Attributes `rangeCount` and `rowTotal` give summaries.  `rangeCount` is the number of citations received within the specified years, while `rowTotal` additionally includes omitted years (hence it is the total number of citations).

.. code-block:: python

    >>> co.rangeCount
    '6'
    >>> co.rowTotal
    '6'


There are also author information stored as list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> co.authors
    [Author(name='Kitchin J.R.', surname='Kitchin', initials='J.R.',
    id='7004212771', url='http://api.elsevier.com/content/author/author_id/7004212771')]
    >>> auth_id = co.authors[0].id
    >>> auth_id
    '7004212771'

Object `auth_id` can for example be used with :doc:`AuthorRetrieval() <../reference/pybliometrics.AuthorRetrieval>`.

Apart from that, there are bibliographic information, too:

.. code-block:: python

    >>> co.title
    'Examples of effective data sharing in scientific publishing'
    >>> co.publicationName
    'ACS Catalysis'
    >>> co.volume
    '5'
    >>> co.issueIdentifier
    '6'
    >>> co.startingPage
    '3894'
    >>> co.endingPage
    '3899'
    >>> co.citationType_long
    'Review'
    >>> co.doi
    '10.1021/acscatal.5b00538'

Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `co.get_cache_file_mdate()` to get the date of last modification, and `co.get_cache_file_age()` the number of days since the last modification.
