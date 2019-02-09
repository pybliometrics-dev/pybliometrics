Citation Overview
-----------------

:doc:`CitationOverview <../reference/scopus.CitationOverview>` implements the `Citations Overview API <https://api.elsevier.com/documentation/AbstractCitationAPI.wadl>`_.  Your API Key needs to be approved by Elsevier manually.  Please contact Scopus to do so.

It takes a `Scopus EID <http://kitchingroup.cheme.cmu.edu/blog/2015/06/07/Getting-a-Scopus-EID-from-a-DOI/>`_ as argument and additionally a starting year and an ending year for which yearly citations will be retrieved.  If no ending year is given, `CitationOverview` will use the current year.  Retrieving these results is not fast, so we cache them to speed up subsequent uses of the code.  Sometimes you may want new results, e.g. to update citation counts, and then you set `refresh=True`.

You initalize the class with Scopus' Electronic Identifier (EID):

.. code-block:: python
   
    >>> from scopus import CitationOverview
    >>> co = CitationOverview("2-s2.0-84930616647", start=2015, end=2017)

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

Object `auth_id` can for example be used with :doc:`AuthorRetrieval <../reference/scopus.AuthorRetrieval>`.


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
