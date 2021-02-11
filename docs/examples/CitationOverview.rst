Citation Overview
-----------------

:doc:`CitationOverview() <../reference/pybliometrics.CitationOverview>` implements the `Citations Overview API <https://dev.elsevier.com/documentation/AbstractCitationAPI.wadl>`_.  Your API Key needs to be approved by Elsevier manually.  Please contact Scopus to do so.  Otherwise each request throws 403 errors.

It takes a `Scopus EID <http://kitchingroup.cheme.cmu.edu/blog/2015/06/07/Getting-a-Scopus-EID-from-a-DOI/>`_ as argument, an optional citation argument to allow exclusion of books or self-citation and additionally a starting year and an ending year for which yearly citations will be retrieved.  If no ending year is given, `CitationOverview()` will use the current year.  Retrieving these results is not fast, so we cache them to speed up subsequent uses of the data.

You initialize the class with Scopus' Electronic Identifier (EID):

.. code-block:: python

    >>> from pybliometrics.scopus import CitationOverview
    >>> co = CitationOverview("2-s2.0-85068268027", start=2019, end=2021)


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(co)
    Document 'pybliometrics: Scriptable bibliometrics using a Python interface to Scopus'
    by Rose M.E., Rose M.E. and Kitchin J.R.
    published in 'SoftwareX' has the following citation trajectory as
    of 2021-01-04:
        Before 2019 0; 2019: 0; 2020: 6; 2021: 1; After 2021: 0 times



The most important information is stored in attribute `cc`, which is a list of tuples storing year-wise citations to the article:

.. code-block:: python

    >>> co.cc
    [(2019, '0'), (2020, '6'), (2021, '1')]


Sometimes there are citations outside the specified year range, which you can get with `pcc` and `lcc`:

.. code-block:: python

    >>> co.pcc
    0
    >>> co.lcc
    0


Attributes `rangeCount` and `rowTotal` give summaries.  `rangeCount` is the number of citations received within the specified years, while `rowTotal` additionally includes omitted years (hence it is the total number of citations).

.. code-block:: python

    >>> co.rangeCount
    '7'
    >>> co.rowTotal
    '7'

Using parameter `citation`, one can exclude self-citations or citations by books. However, if the data has been downloaded and cached, these counts will not take effect! Therefore make wise use of `refresh=True`!

.. code-block:: python

    >>> co_self = CitationOverview("2-s2.0-85068268027", start=2019, end=2021,
                                   citation="exclude-self", refresh=True)
    >>> print(co_self)
    Document 'pybliometrics: Scriptable bibliometrics using a Python interface to Scopus'
    by Rose M.E., Rose M.E. and Kitchin J.R.
    published in 'SoftwareX' has the following citation trajectory
    excluding self-citations as of 2021-02-10:
        Before 2019 0; 2019: 0; 2020: 6; 2021: 1; After 2021: 0 times

    >>> co_books = CitationOverview("2-s2.0-85068268027", start=2019, end=2021,
                                    citation="exclude-books", refresh=True)
    >>> print(co_books)
    Document 'pybliometrics: Scriptable bibliometrics using a Python interface to Scopus'
    by Rose M.E., Rose M.E. and Kitchin J.R.
    published in 'SoftwareX' has the following citation trajectory
    excluding citations from books as of 2021-02-10:
        Before 2019 0; 2019: 0; 2020: 6; 2021: 1; After 2021: 0 times


There are also author information stored as list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> co.authors
    [Author(name='Rose M.E.', surname='Rose', initials='M.E.', id='57209617104',
     url='https://api.elsevier.com/content/author/author_id/57209617104'),
     Author(name='Kitchin J.R.', surname='Kitchin', initials='J.R.', id='7004212771',
     url='https://api.elsevier.com/content/author/author_id/7004212771')]
    >>> auth_id = co.authors[0].id
    >>> auth_id
    '7004212771'

Object `auth_id` can for example be used with :doc:`AuthorRetrieval() <../reference/pybliometrics.AuthorRetrieval>`.

Finally, there are bibliographic information, too:

.. code-block:: python

    >>> co.title
    'pybliometrics: Scriptable bibliometrics using a Python interface to Scopus'
    >>> co.publicationName
    'SoftwareX'
    >>> co.volume
    '10'
    >>> co.issueIdentifier
    None
    >>> co.startingPage
    None
    >>> co.endingPage
    None
    >>> co.citationType_long
    'Article'
    >>> co.doi
    '10.1016/j.softx.2019.100263'

Downloaded results are cached to speed up subsequent analysis.  This information may become outdated, and will not change if you set certain restrictions (e.g. via the `citation` parameter)!  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `co.get_cache_file_mdate()` to get the date of last modification, and `co.get_cache_file_age()` the number of days since the last modification.
