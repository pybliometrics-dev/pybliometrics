pybliometrics.sciencedirect.SubjectClassifications
==================================================

`SubjectClassifications()` implements the `ScienceDirect Subject Classifications API <https://dev.elsevier.com/documentation/SubjectClassificationsAPI.wadl>`_.  It enables retrieval-like queries for All Science Journal Classification (ASJC) subjects/areas.

.. currentmodule:: pybliometrics.sciencedirect
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

    >>> from pybliometrics.sciencedirect import SubjectClassifications, init
    >>> init()
    >>> # Retrieve subject areas with 'Chemistry' in the description
    >>> sc = SubjectClassifications({'description': 'Chemistry'}, refresh=30)
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

The `results` can be cast into a pandas DataFrame:

    >>> import pandas as pd
    >>> # Cast results to a pandas DataFrame
    >>> df = pd.DataFrame(sc.results)
    >>> # Display available fields
    >>> df.columns
    Index(['code', 'description', 'detail', 'abbrev'], dtype='str')
    >>> # Get shape of the DataFrame (rows x columns)
    >>> df.shape
    (16, 4)
    >>> # Display the first 5 rows
    >>> df.head(5)

.. raw:: html

    <div style="overflow-x:auto; border:1px solid #ddd; padding:10px;">
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
        .dataframe{
            font-size: 12px;
        }
    </style>
    <table border="1" class="dataframe">
    <thead>
        <tr style="text-align: right;">
        <th></th>
        <th>code</th>
        <th>description</th>
        <th>detail</th>
        <th>abbrev</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>18</td>
        <td>Biochemistry, Genetics and Molecular Biology</td>
        <td>Biochemistry, Genetics and Molecular Biology</td>
        <td>biochemgenmolbiol</td>
        </tr>
        <tr>
        <th>1</th>
        <td>399</td>
        <td>Biochemistry</td>
        <td>Biochemistry, Genetics and Molecular Biology::...</td>
        <td>biochem</td>
        </tr>
        <tr>
        <th>2</th>
        <td>400</td>
        <td>Biochemistry, Genetics and Molecular Biology (...</td>
        <td>Biochemistry, Genetics and Molecular Biology::...</td>
        <td>biogen</td>
        </tr>
        <tr>
        <th>3</th>
        <td>405</td>
        <td>Clinical Biochemistry</td>
        <td>Biochemistry, Genetics and Molecular Biology::...</td>
        <td>clinicalbio</td>
        </tr>
        <tr>
        <th>4</th>
        <td>416</td>
        <td>Colloid and Surface Chemistry</td>
        <td>Chemical Engineering::Colloid and Surface Chem...</td>
        <td>colloid</td>
        </tr>
    </tbody>
    </table>
    <p>5 rows × 4 columns</p>
    </div>

