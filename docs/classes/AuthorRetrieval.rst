pybliometrics.scopus.AuthorRetrieval
====================================

`AuthorRetrieval()` implements the `Author Retrieval API <https://dev.elsevier.com/documentation/AuthorRetrievalAPI.wadl>`_. It contains an entire author record as per Scopus.

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

You initiate the class with the author's Scopus ID, which can be passed as either an integer or a string:

.. code-block:: python

    >>> from pybliometrics.scopus import AuthorRetrieval
    >>> au = AuthorRetrieval(7004212771)


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(au)
    Kitchin J. from Department of Chemical Engineering in United States,
    published 108 document(s) since 1995
    which were cited by 11,980 author(s) in 14,861 document(s) as of 2021-07-14


The object can access many bits of data about an author, including the number of papers, h-index, current affiliation, etc.  When a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_ is returned, it can neatly be turned into a `pandas <https://pandas.pydata.org/>`_ DataFrame.

Information on names:

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
     given_name='John R.', doc_count=90),
     Variant(indexed_name='Kitchin J.', initials='J.', surname='Kitchin',
     given_name='John', doc_count=11),
     Variant(indexed_name='Kitchin J.', initials='J.R.', surname='Kitchin',
     given_name='J. R.', doc_count=8)]
    >>> au.eid
    '9-s2.0-7004212771'


Bibliometric information:

.. code-block:: python

    >>> au.citation_count
    14861
    >>> au.document_count
    108
    >>> au.h_index
    34
    >>> au.orcid
    '0000-0003-2625-9232'
    >>> au.publication_range
    (1995, 2021)
    >>> import pandas as pd
    >>> areas = pd.DataFrame(au.subject_areas)
    >>> areas.shape
    (49, 3)
    >>> areas.head()
                                area abbreviation  code
    0                Safety Research         SOCI  3311
    1           Analytical Chemistry         CHEM  1602
    2        Modeling and Simulation         MATH  2611
    3        Materials Science (all)         MATE  2500
    4  Colloid and Surface Chemistry         CENG  1505
    >>> au.classificationgroup
    [('3311', '4'), ('1602', '1'), ('2611', '5'), ('2500', '11'),
     ('1505', '1'), ('1605', '4'), ('1303', '2'), ('2504', '10'),
     ('1508', '3'), ('1706', '2'), ('1712', '1'), ('2209', '5'),
     ('2105', '1'), ('1504', '2'), ('1500', '26'), ('3309', '1'),
     ('1600', '28'), ('2508', '14'), ('2310', '2'), ('1503', '22'),
     ('2300', '1'), ('2102', '3'), ('3107', '3'), ('1000', '1'),
     ('3110', '9'), ('2213', '7'), ('2505', '6'), ('3100', '9'),
     ('1906', '1'), ('1305', '3'), ('2304', '1'), ('1604', '2'),
     ('1909', '1'), ('2207', '2'), ('2200', '2'), ('1607', '1'),
     ('2103', '3'), ('2308', '2'), ('3104', '21'), ('1311', '1'),
     ('1603', '3'), ('2305', '2'), ('1606', '24'), ('2503', '1'),
     ('2100', '11'), ('2208', '1'), ('1502', '2'), ('2104', '2'),
     ('1710', '5')]


If you request data of a merged author profile, Scopus returns information belonging to that new profile.  pybliometrics however caches information using the old ID.  With property `.identifer` you can verify the validity of the provided Author ID.  When the provided ID belongs to a profile that has been merged, pybliometrics will throw a UserWarning (upon accessing the property `.identifer`) pointing to the ID of the new main profile.

Extensive information on current and former affiliations is provided as namedtuples as well:

.. code-block:: python

    >>> au.affiliation_current
    [Affiliation(id=110785688, parent=60027950, type='dept', relationship='author',
     afdispname=None, preferred_name='Department of Chemical Engineering',
     parent_preferred_name='Carnegie Mellon University', country_code='usa',
     country='United States', address_part='5000 Forbes Avenue', city='Pittsburgh',
     state='PA', postal_code='15213-3890', org_domain='cmu.edu', org_URL='https://www.cmu.edu/')]
    >>> len(au.affiliation_history)
    16
    >>> au.affiliation_history[10]
    Affiliation(id=60008644, parent=None, type='parent', relationship='author',
    afdispname=None, preferred_name='Fritz Haber Institute of the Max Planck Society',
    parent_preferred_name=None, country_code='deu', country='Germany',
    address_part='Faradayweg 4-6', city='Berlin', state=None, postal_code='14195',
    org_domain='fhi.mpg.de', org_URL='https://www.fhi.mpg.de/')


The affiliation ID to be used for the :doc:`AffiliationRetrieval <../classes/AffiliationRetrieval>` class.

`pybliometrics` caches results to speed up subsequent analysis.  This information eventually becomes outdated.  To refresh the cached results if they exist, use the refresh parameter when initiating the class.  Set `refresh=True` or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `au.get_cache_file_mdate()` to get the date of last modification, and `au.get_cache_file_age()` the number of days since the last modification.

There are a number of getter methods for convenience.  For example, you can obtain some basic information on co-authors as a list of namedtuples (query will not be cached and is always up-to-date):

.. code-block:: python

    >>> coauthors = pd.DataFrame(au.get_coauthors())
    >>> coauthors.shape
    (160, 8)
    >>> coauthors.columns
    Index(['surname', 'given_name', 'id', 'areas', 'affiliation_id',
           'name', 'city', 'country'],
          dtype='object')


Method `get_documents()` is another convenience method to search for the author's publications via :doc:`ScopusSearch <../classes/ScopusSearch>` (information will be cached):

.. code-block:: python

    >>> docs = pd.DataFrame(au.get_documents(refresh=10))
    >>> docs.shape
    (108, 34)
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


With some additional lines of code you can get the number of journal articles where the author is listed first:

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
    2011    10
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
    Name: year, dtype: int64


If you're just interested in the EIDs of the documents, use `au.get_document_eids()`.  This method makes use of the same data available for/through `au.get_documents()`.
