pybliometrics.scopus.ScDirSubjectClassifications
===========================================

`ScDirSubjectClassifications()` implements the `ScienceDirect Subject Classifications API <https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl>`_.  It enables retrieval-like queries for All Science Journal Classification (ASJC) subjects/areas.

.. currentmodule:: pybliometrics.sciencedirect
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: ScDirSubjectClassifications
   :members:
   :inherited-members:

Examples
--------

You initialize the class with a query `dict`.  It contains the "description" (general classification of the subject), "code" (the ASJC code), "detail" (detailed name of the subject), "abbrev" (abbreviation of general classification of subject) or a combination of those:

.. code-block:: python

    >>> from pybliometrics.sciencedirect import ScDirSubjectClassifications, init
    >>> init()
    >>> # Retrieve subject areas with 'Chemistry' in the description
    >>> sc = ScDirSubjectClassifications({'description': 'Chemistry'}, refresh=30)
    >>> # Access the results
    >>> sc.results
    [Subject(code='18', description='Biochemistry, Genetics and Molecular Biology', detail='Biochemistry, Genetics and Molecular Biology', abbrev='biochemgenmolbiol'),
    Subject(code='399', description='Biochemistry', detail='Biochemistry, Genetics and Molecular Biology::Biochemistry', abbrev='biochem'),
    Subject(code='400', description='Biochemistry, Genetics and Molecular Biology (General)', detail='Biochemistry, Genetics and Molecular Biology::Biochemistry, Genetics and Molecular Biology (General)', abbrev='biogen'),
    ...]
 
The results are stored in a named tuple. We can access the individual fields, like the ASJC code as follows:

.. code-block:: python

    >>> # Access the first result and get the ASJC code
    >>> first_result = sc.results[0]
    >>> first_result.code
    '18'