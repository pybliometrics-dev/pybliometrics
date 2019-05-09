Serial Title
------------

:doc:`Serial Title <../reference/scopus.SerialTitle>` implements the `Serial Title API <https://api.elsevier.com/documentation/SerialTitleAPI.wadl>`_. It provides basic information on registered serials (also called sources), like publisher and identifers, but also metrics.

You initialize the class with an ISSN or an E-ISSN (works with and without hyphen, but leading zeros are important):

.. code-block:: python
   
    >>> from scopus import SerialTitle
    >>> source = SerialTitle("00368075")


The object has a number of attributes but no methods.  For example, information regarding the source itself:

.. code-block:: python

    >>> source.title
    'Science'
    >>> source.publisher
    'American Association for the Advancement of Science'
    >>> source.issn
    '0036-8075'
    >>> source.eissn
    '1095-9203'
    >>> source.source_id
    '23571'


Perhaps most importantly the SCImago Journal Rank indicator and the Source-normalized Impact per Paper.  The information is stored in tuples with the first element indicating the year the metric was evaluated:

.. code-block:: python

    >>> source.sjrlist
    ('2017', '14.142')
    >>> source.sniplist
    ('2017', '7.154')


The fields associated with the source are stored as a list of `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> source.subject_area
    [Subjectarea(area='Multidisciplinary', abbreviation='MULT', code='1000')]


Additionally there are many bits of information on Open Access status which are often empty however.
