pybliometrics.scopus.CitationOverview
=====================================

`CitationOverview()` implements the `Citation Overview API <https://dev.elsevier.com/documentation/AbstractCitationAPI.wadl>`_.  Your API Key requires manual approval by Elsevier.  Please contact Scopus for approval.  Otherwise each request throws a 403 error.  Ideally you provide the key via `apikey="XXX"` when initiating the class, which will override the ones provided in the :doc:`configuration file <../../configuration>`.

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

The class can download yearly citation counts for up to 25 documents at once.  Simply provide a list of either the Scopus identifiers, the DOIs, the PIIs or the pubmed IDs and specify the identifier type in `id_type`.  By default, Scopus returns citation information for the current and the previous two years.  Use the `date` parameter to select a different range of years in a single string with the start year and the end year joined on a hypen.  Optionally you can exclude citations by books or self-citation via `exclude`.

You initialize the class with a list of identifiers:

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import CitationOverview
    >>> pybliometrics.scopus.init()
    >>> identifier = ["85068268027", "84930616647"]
    >>> co = CitationOverview(identifier, date="2019-2021")


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(co)
    2 document(s) has/have the following total citation count
    as of 2024-07-27:
        115; 21


The key attribute is `cc`, which provides a list of tuples storing year-wise citations to the article.  Each list corresponds to one document, in the order specified when initating the class:

.. code-block:: python

    >>> co.cc
    [[(2019, 0), (2020, 6), (2021, 25)],
	 [(2019, 2), (2020, 2), (2021, 2)]]


The attributes `pcc`, `rangeCount`, `lcc` and `rowTotal` provide citation summaries for each document.  `pcc` is the count of citations before the specified year, `rangeCount` the count of citations for the specified years, and `lcc` the count of citations after the specified year.  For the sum (i.e., the total number of citations by document) use `rowTotal`

.. code-block:: python

    >>> co.pcc
    [0, 6]
    >>> co.rangeCount
    [31, 6]
    >>> co.lcc
    [84, 6]
    >>> co.rowTotal
    [115, 21]


The `columnTotal` attribute represents the total number of yearly citations for all documents combined, which `rangeColumnTotal` summarizes.  Finally `grandTotal` is the total number of citations for all documents combined.

.. code-block:: python

    >>> co.columnTotal
    [2, 8, 27]
    >>> co.rangeColumnTotal
    37
    >>> co.grandTotal
    136


With the `citation` parameter, you can exclude self-citations or citations from books:

.. code-block:: python

    >>> co_self = CitationOverview(identifier, date="2019-2021",
                                   citation="exclude-self")
    >>> print(co_self)
    2 document(s) has/have the following total citation count
    excluding self-citations as of 2024-07-27:
        110; 19
    >>> co_books = CitationOverview(identifier, date="2019-2021",
                                    citation="exclude-books")
    >>> print(co_books)
    2 document(s) has/have the following total citation count
    excluding citations from books as of 2024-07-27:
        115; 21


Author information is also stored as lists of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> co.authors[0]
    [Author(name='Rose M.E.', surname='Rose', initials='M.E.', id='57209617104',
            url='https://api.elsevier.com/content/author/author_id/57209617104'),
     Author(name='Kitchin J.R.', surname='Kitchin', initials='J.R.', id='7004212771',
            url='https://api.elsevier.com/content/author/author_id/7004212771')]
    >>> co.authors[1]
    [Author(name='Kitchin J.R.', surname='Kitchin', initials='J.R.', id='7004212771',
            url='https://api.elsevier.com/content/author/author_id/7004212771')]


Via `co.authors[0][0].id` one can for instance obtain further author information via the :doc:`AuthorRetrieval() <AuthorRetrieval>` class.

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


Using `pandas <https://pandas.pydata.org/>`_, you can convert the citation counts into a DataFrame as follows:

.. code-block:: python

    >>> import pandas as pd
    >>> df = pd.concat([pd.Series(dict(x)) for x in co.cc], axis=1).T
    >>> df.index = co.scopus_id
    >>> print(df)
                 2019  2020  2021
    85068268027     0     6    25
    84930616647     2     2     2


Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.
