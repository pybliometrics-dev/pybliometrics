Author Retrieval
----------------

:doc:`AuthorRetrieval <../reference/scopus.AuthorRetrieval>` implements the `Author Retrieval API <https://api.elsevier.com/documentation/AuthorRetrievalAPI.wadl>`_.

This class is to interact with the entire author record in Scopus, using the author's Scopus ID (which can be passed as either an integer or a string):

.. code-block:: python
   
    >>> from scopus import AuthorRetrieval
    >>> au = AuthorRetrieval(7004212771)


The object can access many bits of data about an author, including the number of papers, h-index, current affiliation, etc.  When a list of `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_ is returned, the can neatly be turned into `pandas <https://pandas.pydata.org/>`_ DataFrames.

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
    [Variant(indexed_name='Kitchin J.', initials='J.R.', surname='Kitchin', given_name='John R.', doc_count='81'),
    Variant(indexed_name='Kitchin J.', initials='J.', surname='Kitchin', given_name='John', doc_count='10'),
    Variant(indexed_name='Kitchin J.', initials='J.R.', surname='Kitchin', given_name='J. R.', doc_count='8')]
    >>> au.eid
    '9-s2.0-7004212771'


Bibliometric information:

.. code-block:: python

    >>> au.citation_count
    '7587'
    >>> au.document_count
    '99'
    >>> au.h_index
    '27'
    >>> au.orcid
    '0000-0003-2625-9232'
    >>> au.publication_range
    ('1995', '2018')
    >>> import pandas as pd
    >>> journals = pd.DataFrame(au.journal_history)
    >>> journals.shape
    (50, 4)
    >>> journals.head()
                                  sourcetitle           abbreviation type      issn
    0         Journal of Physical Chemistry B          J Phys Chem B    j  15206106
    1                        Energy and Fuels           Energy Fuels    j  15205029
    2     Journal of Physics Condensed Matter  J Phys Condens Matter    j  1361648X
    3                    Molecular Simulation            Mol. Simul.    j  10290435
    4  Journal of the Electrochemical Society      J Electrochem Soc    j  00134651
    >>> areas = pd.DataFrame(au.subject_areas)
    >>> areas.shape
    (47, 3)
    >>> areas.head()
                             area abbreviation  code
    0  Geochemistry and Petrology         EART  1906
    1        Analytical Chemistry         CHEM  1602
    2     Modeling and Simulation         MATH  2611
    3             Safety Research         SOCI  3311
    4               Biotechnology         BIOC  1305
    >>> au.classificationgroup
    [('1906', '1'), ('1602', '1'), ('2611', '5'), ('3311', '2'), ('1305', '4'), ('2304', '1'), ('2500', '11'), ('1604', '2'), ('1505', '1'), ('1909', '1'), ('2207', '2'), ('2200', '2'), ('1605', '4'), ('1706', '1'), ('1607', '1'), ('2504', '9'), ('1303', '1'), ('2103', '3'), ('1508', '2'), ('3104', '20'), ('2308', '2'), ('2209', '5'), ('2105', '1'), ('1311', '1'), ('1606', '22'), ('1603', '3'), ('2305', '3'), ('2503', '1'), ('3309', '1'), ('1500', '27'), ('2508', '13'), ('2100', '10'), ('1600', '26'), ('2310', '2'), ('2208', '1'), ('2300', '1'), ('1503', '20'), ('2102', '3'), ('1000', '1'), ('3110', '9'), ('3107', '2'), ('2104', '2'), ('2505', '6'), ('1710', '5'), ('2213', '5'), ('1502', '1'), ('3100', '9')]


Information on current and former affiliation(s) to be used for the `ContentAffiliationRetrieval <../reference/scopus.ContentAffiliationRetrieval>`_ class:

.. code-block:: python

    >>> au.affiliation_current
    '110785688'
    >>> au.affiliation_history
    ['60026531', '60030926', '60090776', '60027757', '60008644']


There are a number of getter methods for convenience.  For example, you can obtain some basic information on co-authors as a list of namedtuples (query will not be cached):

.. code-block:: python

    >>> coauthors = pd.DataFrame(au.get_coauthors())
    >>> coauthors.shape
    (160, 8)
    >>> coauthors.columns
    Index(['surname', 'given_name', 'id', 'areas', 'affiliation_id', 'name',
           'city', 'country'],
      dtype='object')


Method `get_document_eids()` performs a search for the author's publications with `ScopusSearch <../reference/scopus.ScopusSearch>`_ to ease interoperationability with other APIs:

.. code-block:: python

    >>> eids = pd.DataFrame(au.get_document_eids(refresh=False))
    >>> eids.shape
    (99, 19)
    >>> eids.columns
    Index(['eid', 'doi', 'pii', 'title', 'subtype', 'creator', 'authname',
           'authid', 'coverDate', 'coverDisplayDate', 'publicationName', 'issn',
           'source_id', 'aggregationType', 'volume', 'issueIdentifier',
           'pageRange', 'citedby_count', 'openaccess'],
          dtype='object')
    >>> eids.head()
                      eid                            doi    ...     citedby_count openaccess
    0  2-s2.0-85044777111   10.1016/j.cattod.2018.03.045    ...                 0          0
    1  2-s2.0-85041118154  10.1080/08927022.2017.1420185    ...                 1          0
    2  2-s2.0-85040934644      10.1007/s11244-018-0899-0    ...                 4          0
    3  2-s2.0-85031781417    10.1021/acs.jpclett.7b01974    ...                 1          0
    4  2-s2.0-85021887490        10.1021/acs.cgd.7b00569    ...                 3          0

    [5 rows x 19 columns]


With some additional lines of code you can get the number of journal articles where the author is listed first:

.. code-block:: python

    >>> articles = eids[eids['aggregationType'] == 'Journal']
    >>> first = articles[articles['authid'].str.startswith('7004212771')]
    >>> list(first['eid'])
    ['2-s2.0-85019169906', '2-s2.0-84971324241', '2-s2.0-84930349644',
    '2-s2.0-84930616647', '2-s2.0-84866142469', '2-s2.0-67449106405',
    '2-s2.0-40949100780', '2-s2.0-20544467859', '2-s2.0-13444307808',
    '2-s2.0-2942640180', '2-s2.0-0141924604', '2-s2.0-0037368024']


or you might be interested in the yearly number of publications:

.. code-block:: python

    >>> articles['year'] = articles['coverDate'].str[:4]
    >>> articles['year'].value_counts()
    2015    12
    2017     8
    2016     8
    2012     7
    2009     7
    2014     7
    2010     5
    2004     4
    2011     4
    2013     4
    2003     3
    2018     3
    2005     2
    2006     1
    2002     1
    2008     1
    1995     1
    Name: year, dtype: int64

