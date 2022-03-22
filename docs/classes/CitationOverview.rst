pybliometrics.scopus.CitationOverview
=====================================

`CitationOverview()` implements the `Citation Overview API <https://dev.elsevier.com/documentation/AbstractCitationAPI.wadl>`_.  Your API Key needs to be approved by Elsevier manually.  Please contact Scopus to do so.  Otherwise each request throws a 403 error.  Ideally provide the key via `apikey="XXX"` when initiating the class, which will override the ones provided in the :doc:`configuration file <../configuration>`.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: CitationOverview
   :members:
   :inherited-members:

Examples
--------

The class can download yearly citation counts for up to 25 documents at once.  Simply provide a list of either the Scopus identifiers, the DOIs, the PIIs or the pubmed IDs and specify the identifier type in `id_type`.  The API needs to know for which years you want to retrieve yearly citation counts.  Therefore you need to set the year from which on `CitationOverview()` will return yearly citation counts (e.g., the publication year).  If no ending year is given, `CitationOverview()` will use the current year.  Optionally you can exclude citations by books or self-citation via `exclude`.

You initialize the class with a list of identifiers:

.. code-block:: python

    >>> from pybliometrics.scopus import CitationOverview
    >>> identifier = ["85068268027", "84930616647"]
    >>> co = CitationOverview(identifier, start=2019, end=2021)


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(co)
    2 document(s) has/have the following total citation count
    as of 2021-07-17:
        16; 13


The most important information is stored in attribute `cc`, which is a list of of list of tuples storing year-wise citations to the article.  Each list corresponds to one document, in the order specified when initating the class:

.. code-block:: python

    >>> co.cc
    [[(2019, 0), (2020, 6), (2021, 10)],
     [(2019, 2), (2020, 2), (2021, 1)]]


Attributes `pcc`, `rangeCount`, `lcc` and `rowTotal` give citation summaries by document.  `pcc` is the count of citations before the specified year, `rangeCount` the count of citations for the specified years, and `lcc` the count of citations after the specified year.  For the sum (i.e., the total number of citations by document) use `rowTotal`

.. code-block:: python

    >>> co.pcc
    [0, 8]
    >>> co.rangeCount
    [16, 5]
    >>> co.lcc
    [0, 0]
    >>> co.rowTotal
    [16, 13]


Attribute `columnTotal` gives the total number of yearly citations for all documents combined, which `rangeColumnTotal` summarizes.  Finally `grandTotal` is the total number of citations for all documents combined.

.. code-block:: python

    >>> co.columnTotal
    [2, 8, 11]
    >>> co.rangeColumnTotal
    21
    >>> co.grandTotal
    29


Using parameter `citation`, one can exclude self-citations or citations by books:

.. code-block:: python

    >>> co_self = CitationOverview(identifier, start=2019, end=2021,
                                   citation="exclude-self")
    >>> print(co_self)
    2 document(s) has/have the following total citation count
    excluding self-citations as of 2021-07-17:
        14; 11
    >>> co_books = CitationOverview(identifier, start=2019, end=2021,
                                    citation="exclude-books")
    >>> print(co_books)
    2 document(s) has/have the following total citation count
    excluding citations from books as of 2021-07-17:
        16; 13


There are also author information stored as list of lists of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> co.authors[0]
    [Author(name='Rose M.E.', surname='Rose', initials='M.E.', id='57209617104',
            url='https://api.elsevier.com/content/author/author_id/57209617104'),
     Author(name='Kitchin J.R.', surname='Kitchin', initials='J.R.', id='7004212771',
            url='https://api.elsevier.com/content/author/author_id/7004212771')]
    >>> co.authors[1]
    [Author(name='Kitchin J.R.', surname='Kitchin', initials='J.R.', id='7004212771',
            url='https://api.elsevier.com/content/author/author_id/7004212771')]


Via `co.authors[0][0].id` one can for instance obtain further author information via the :doc:`AuthorRetrieval() <../classes/AuthorRetrieval>` class.

Finally, there are bibliographic information, too:

.. code-block:: python

    >>> co.title
    ['pybliometrics: Scriptable bibliometrics using a Python interface to Scopus',
     'Examples of effective data sharing in scientific publishing']
    >>> co.publicationName
    ['SoftwareX', 'ACS Catalysis']
    >>> co.volume
    ['10', '5']
    >>> co.issueIdentifier
    [None, '6']
    >>> co.citationType_long
    ['Article', 'Review']


Using `pandas <https://pandas.pydata.org/>`_, you can turn the citation counts into a DataFrame like so:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.concat([pd.Series(dict(x)) for x in co.cc], axis=1).T
    >>> df.index = co.scopus_id
    >>> print(df)
                 2019  2020  2021
    85068268027     0     6    10
    84930616647     2     2     1


Downloaded results are cached to speed up subsequent analysis.  This information may become outdated, and will not change if you set certain restrictions (e.g. via the `citation` parameter)!  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `co.get_cache_file_mdate()` to get the date of last modification, and `co.get_cache_file_age()` the number of days since the last modification.
