pybliometrics.scopus.SubjectClassifications
===========================================

`SubjectClassifications()` implements the `Subject Classifications API <https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl>`_.  It allows for retrieval-like query for All Science Journal Classification (ASJC) subjects/areas.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: SubjectClassifications
   :members:
   :inherited-members:

Examples
--------

You initialize the class with a query `dict`.  It contains the "description" (general classification of the subject), "code" (the ASJC code), "detail" (detailed name of the subject), "abbrev" (abbreviation of general classification of subject) or a combination of those:

.. code-block:: python

    >>> from pybliometrics.scopus import SubjectClassifications
    >>> sub = SubjectClassifications({'description': 'Mathematics'})


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(sub)
    Search '{'description': 'Mathematics', 'field': 'code,description,detail,abbrev'}'
    yielded 15 subject areas as of 2021-02-11:
        2600
        2601
        2602
        2603
        2604
        2605
        2606
        2607
        2608
        2609
        2610
        2611
        2612
        2613
        2614


The class has only one method - `SubjectClass.results` - which returns a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_.  By default, the API returns description, code, detail and abbreviation of each found subject, which is also reflected in the fields of `namedtuples` of `SubjectClass().results`.  You can specify the fields to be returned in the search results (e.g. only codes of subjects).

.. code-block:: python

    >>> sub.results
    [Subject(code='2600', description='Mathematics', detail='Mathematics (all)', abbrev='MATH'),
     Subject(code='2601', description='Mathematics', detail='Mathematics (miscellaneous)', abbrev='MATH'),
     Subject(code='2602', description='Mathematics', detail='Algebra and Number Theory', abbrev='MATH'),
     Subject(code='2603', description='Mathematics', detail='Analysis', abbrev='MATH'),
     Subject(code='2604', description='Mathematics', detail='Applied Mathematics', abbrev='MATH'),
     Subject(code='2605', description='Mathematics', detail='Computational Mathematics', abbrev='MATH'),
     Subject(code='2606', description='Mathematics', detail='Control and Optimization', abbrev='MATH'),
     Subject(code='2607', description='Mathematics', detail='Discrete Mathematics and Combinatorics', abbrev='MATH'),
     Subject(code='2608', description='Mathematics', detail='Geometry and Topology', abbrev='MATH'),
     Subject(code='2609', description='Mathematics', detail='Logic', abbrev='MATH'),
     Subject(code='2610', description='Mathematics', detail='Mathematical Physics', abbrev='MATH'),
     Subject(code='2611', description='Mathematics', detail='Modeling and Simulation', abbrev='MATH'),
     Subject(code='2612', description='Mathematics', detail='Numerical Analysis', abbrev='MATH'),
     Subject(code='2613', description='Mathematics', detail='Statistics and Probability', abbrev='MATH'),
     Subject(code='2614', description='Mathematics', detail='Theoretical Computer Science', abbrev='MATH')]


Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.

Use `source.get_cache_file_mdate()` to get the date of last modification, and `source.get_cache_file_age()` the number of days since the last modification.
