pybliometrics.scopus.AuthorRetrieval
====================================

`AuthorRetrieval()` implements the `Author Retrieval API <https://dev.elsevier.com/documentation/AuthorRetrievalAPI.wadl>`_. It provides a complete author record according to Scopus.

In addition, the 'ENTITLED' view lets you check you whether you have access to this class.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: AuthorRetrieval
    :members:
    :inherited-members:

Examples
--------

You initiate the class with the author's Scopus ID, which can be either an integer or a string:

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scopus import AuthorRetrieval
    >>> pybliometrics.scopus.init()
    >>> au = AuthorRetrieval(7004212771)


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(au)
    Kitchin J. from Carnegie Mellon University in United States,
	published 126 document(s) since 1995 
	which were cited by 20,897 author(s) in 25,490 document(s) as of 2024-05-11


This object provides access to various data about an author, including the number of papers, h-index, current affiliation, etc.  When a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_ is returned, it can neatly be turned into a `pandas <https://pandas.pydata.org/>`_ DataFrame.

Information regarding the author's names includes:

.. code-block:: python

    >>> au.indexed_name
    'Kitchin J.'
    >>> au.surname
    'Kitchin'
    >>> au.given_name
    'John R.'
    >>> au.initials
    'J.R.'
    >>> au.name_variants
    [Variant(indexed_name='Kitchin J.', initials='J.R.', surname='Kitchin',
     given_name='John R.', doc_count=104),
     Variant(indexed_name='Kitchin J.', initials='J.', surname='Kitchin',
     given_name='John', doc_count=13),
     Variant(indexed_name='Kitchin J.', initials='J.R.', surname='Kitchin',
     given_name='J. R.', doc_count=8)]
    >>> au.eid
    '9-s2.0-7004212771'


Bibliometric information includes:

.. code-block:: python

    >>> au.citation_count
    25490
    >>> au.document_count
    126
    >>> au.h_index
    40
    >>> au.orcid
    '0000-0003-2625-9232'
    >>> au.publication_range
    (1995, 2021)
    >>> import pandas as pd
    >>> areas = pd.DataFrame(au.subject_areas)
    >>> areas.shape
    (55, 3)
    >>> areas.head()
        area abbreviation  code
	0              Analytical Chemistry         CHEM  1602
	1                   Safety Research         SOCI  3311
	2  Process Chemistry and Technology         CENG  1508
	3           Materials Science (all)         MATE  2500
	4           Modeling and Simulation         MATH  2611
    >>> au.classificationgroup
    [(1602, 1), (3311, 4), (1508, 6),  (2500, 13),
	 (2611, 6), (1505, 1), (1605, 7), (1303, 2),
	 (1501, 2), (1706, 4), (2504, 13), (1500, 42),
	 (1503, 33), (2105, 1), (3100, 13), (2209, 11),
     (1712, 3), (1709, 2), (1504, 2), (1702, 2),
	 (3309, 3), (2310, 3), (1507, 2), (2508, 17),
	 (2300, 2), (3107, 3), (2102, 6), (3110, 9),
	 (1000, 1), (1600, 40), (1601, 3), (2213, 7),
	 (2505, 6), (1906, 1), (1305, 8), (2700, 6),
	 (2304, 2), (1604, 3), (1909, 1), (2207, 2),
	 (2200, 2), (1607, 1), (1606, 36), (2308, 3),
	 (3104, 23), (2103, 6), (1311, 1), (1603, 3),
	 (2503, 1), (2305, 7), (2208, 1), (2100, 16),
	 (1502, 2), (1710, 6), (2104, 2)]


If you request data of a merged author profile, Scopus provides information corresponding to the new, merged profile.  The cache file's name uses the provided, i.e., old, ID.  With property `.identifer` you can verify the validity of the provided Author ID.  When the provided ID belongs to a profile that has been merged, pybliometrics will throw a UserWarning (upon accessing the property `.identifer`) pointing to the ID of the new main profile.

Detailed information on current and former affiliations is also provided in the form of namedtuple:

.. code-block:: python

    >>> au.affiliation_current
    [Affiliation(id=110785688, parent=60027950, type='dept', relationship='author',
     afdispname=None, preferred_name='Department of Chemical Engineering',
     parent_preferred_name='Carnegie Mellon University', country_code='usa',
     country='United States', address_part='5000 Forbes Avenue', city='Pittsburgh',
     state='PA', postal_code='15213-3890', org_domain='cmu.edu', org_URL='https://www.cmu.edu/')]
    >>> len(au.affiliation_history)
    16
    >>> au.affiliation_history[6]
    Affiliation(id=60008644, parent=None, type='parent', relationship='author',
    afdispname=None, preferred_name='Fritz Haber Institute of the Max Planck Society',
    parent_preferred_name=None, country_code='deu', country='Germany',
    address_part='Faradayweg 4-6', city='Berlin', state=None, postal_code='14195',
    org_domain='fhi.mpg.de', org_URL='https://www.fhi.mpg.de/')


The affiliation ID to be used for the :doc:`AffiliationRetrieval <AffiliationRetrieval>` class.

Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.

Several getter methods are available for convenience.  For example, you can obtain some basic information on co-authors as a list of namedtuples (query will not be cached and is always up-to-date):

.. code-block:: python

    >>> coauthors = pd.DataFrame(au.get_coauthors())
    >>> coauthors.shape
    (160, 8)
    >>> coauthors.columns
    Index(['surname', 'given_name', 'id', 'areas', 'affiliation_id',
           'name', 'city', 'country'],
          dtype='object')


The `get_documents()` method is another convenient option for searching the author's publications via :doc:`ScopusSearch <ScopusSearch>` (information will be cached):

.. code-block:: python

    >>> docs = pd.DataFrame(au.get_documents(refresh=10))
    >>> docs.shape
    (126, 36)
    >>> docs.columns
    Index(['eid', 'doi', 'pii', 'pubmed_id', 'title', 'subtype',
           'subtypeDescription', 'creator', 'afid', 'affilname',
           'affiliation_city', 'affiliation_country', 'author_count',
           'author_names', 'author_ids', 'author_afids', 'coverDate',
           'coverDisplayDate', 'publicationName', 'issn', 'source_id', 'eIssn',
           'aggregationType', 'volume', 'issueIdentifier', 'article_number',
           'pageRange', 'description', 'authkeywords', 'citedby_count',
           'openaccess', 'fund_acr', 'fund_no', 'fund_sponsor'],
          dtype='object')


WWith a few additional code lines, you can determine the number of journal articles where the author is listed first:

.. code-block:: python

    >>> articles = docs[docs['aggregationType'] == 'Journal']
    >>> first = articles[articles['author_ids'].str.startswith('7004212771')]
    >>> first["eid"].tolist()
    ['2-s2.0-85048443766', '2-s2.0-85019169906', '2-s2.0-84971324241',
     '2-s2.0-84930349644', '2-s2.0-84930616647', '2-s2.0-84866142469',
     '2-s2.0-67449106405', '2-s2.0-40949100780', '2-s2.0-20544467859',
     '2-s2.0-13444307808', '2-s2.0-2942640180', '2-s2.0-0141924604',
     '2-s2.0-0037368024']


or you might be interested in the yearly number of publications:

.. code-block:: python

    >>> docs['year'] = docs['coverDate'].str[:4]
    >>> docs['year'].value_counts().sort_index()
    1995     1
	2002     1
	2003     3
	2004     4
	2005     3
	2006     1
	2007     2
	2008     7
	2009    10
	2010     6
	2011     8
	2012     8
	2013     4
	2014    10
	2015    12
	2016     7
	2017     8
	2018     4
	2019     2
	2020     2
	2021     3
	2022     9
	2023     8
	2024     3
    Name: year, dtype: int64


If you're just interested in the EIDs of the documents, use `au.get_document_eids()`.  This method makes use of the same data available for/through `au.get_documents()`.
