pybliometrics.sciencedirect.ScienceDirectSearch
===============================================

`ScienceDirectSearch()` implements the `ScienceDirect Search API <https://nonprod-devportal.elsevier.com/documentation/ScienceDirectSearchAPI.wadl>`_ using the `PUT` method.  It executes a query to search for documents and retrieves the resulting records.
The class takes a `query` dictionary as input which has to follow this schema:

.. code-block:: text

    {
        authors: string,
        date: string,
        display: {
            highlights: boolean,
            offset: integer,
            show: integer,
            sortBy: string
        },
        filters: {
            openAccess: boolean
        },
        issue: string,
        loadedAfter: string,
        page: string,
        pub: string,
        qs: string,
        title: string,
        volume: string
    }

For a more detailed description of the parameters, please refer to the `ScienceDirect Search API migration documentation <https://dev.elsevier.com/tecdoc_sdsearch_migration.html>`_.

.. currentmodule:: pybliometrics.sciencedirect
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: ScienceDirectSearch
    :members:
    :inherited-members:

Examples
--------

The class is initialized with a search query.
We can pass the field `qs`` to search for specific keywords.
Using `verbose=True` will print the progress of the download.

.. code-block:: python

    >>> from pybliometrics.sciencedirect import ScienceDirectSearch, init
    >>> init()
    >>> # Retrieve documents based on the search query  
    >>> query = query = {'qs': '"neural radiance fields" AND "3D rendering"', 'date': '2024'}
    >>> sds = ScienceDirectSearch(query, verbose=True)
    Downloading results for query "{'qs': '"neural radiance fields" AND "3D rendering"', 'date': '2024', 'display': {'offset': 0, 'show': 100, 'sortBy': 'date'}, 'cursor': '*'}":
    100%|██████████| 1/1 [00:00<00:00,  3.23it/s]


To check the number of results, use the method `get_results_size()`.

.. code-block:: python

    >>> # Check the number of results
    >>> sds.get_results_size()
    10


To access the results, use the attribute `results` which contains a list of `Document` namedtuples.

.. code-block:: python

    >>> # Access the results
    >>> results = sds.results
    [Document(authors='Geontae Kim; Youngjin Cha', doi='10.1016/j.autcon.2024.105878', loadDate='2024-11-19T00:00:00.000Z', openAccess=True, first_page=105878, last_page=None, pii='S0926580524006149', publicationDate='2024-12-15', sourceTitle='Automation in Construction', title='3D Pixelwise damage mapping using a deep attention based modified Nerfacto', uri='https://www.sciencedirect.com/science/article/pii/S0926580524006149?dgcid=api_sd_search-api-endpoint', volumeIssue='Volume 168, Part B'),
     Document(authors='Akram Akbar; Chun Liu; Zeran Xu', doi='10.1016/j.aei.2024.102913', loadDate='2024-11-16T00:00:00.000Z', openAccess=False, first_page=102913, last_page=None, pii='S1474034624005640', publicationDate='2024-10-31', sourceTitle='Advanced Engineering Informatics', title='Scene information guided aerial photogrammetric mission recomposition towards detailed level building reconstruction', uri='https://www.sciencedirect.com/science/article/pii/S1474034624005640?dgcid=api_sd_search-api-endpoint', volumeIssue='Volume 62, Part D'),
     Document(authors='Ruxandra Stoean; Nebojsa Bacanin; Leonard Ionescu', doi='10.1016/j.culher.2024.07.008', loadDate='2024-08-09T00:00:00.000Z', openAccess=False, first_page=18, last_page=26, pii='S1296207424001468', publicationDate='2024-10-31', sourceTitle='Journal of Cultural Heritage', title='Bridging the past and present: AI-driven 3D restoration of degraded artefacts for museum digital display', uri='https://www.sciencedirect.com/science/article/pii/S1296207424001468?dgcid=api_sd_search-api-endpoint', volumeIssue='Volume 69'),
     ...]

The list of results can be converted into a Pandas DataFrame.

.. code-block:: python

    >>> import pandas as pd
    >>> # Cast results to a pandas DataFrame
    >>> df = pd.DataFrame(sds.results)
    >>> # Display available fields
    >>> df.columns
    Index(['authors', 'doi', 'loadDate', 'openAccess', 'first_page', 'last_page',
       'pii', 'publicationDate', 'sourceTitle', 'title', 'uri', 'volumeIssue'],
      dtype='object')
    >>> # Get shape of the DataFrame (rows x columns)
    >>> df.shape
    (10, 12)
    >>> # Display the first 3 rows
    >>> df.head(3)

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
        <th>authors</th>
        <th>doi</th>
        <th>loadDate</th>
        <th>openAccess</th>
        <th>first_page</th>
        <th>last_page</th>
        <th>pii</th>
        <th>publicationDate</th>
        <th>sourceTitle</th>
        <th>title</th>
        <th>uri</th>
        <th>volumeIssue</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>Geontae Kim; Youngjin Cha</td>
        <td>10.1016/j.autcon.2024.105878</td>
        <td>2024-11-19T00:00:00.000Z</td>
        <td>True</td>
        <td>105878</td>
        <td>NaN</td>
        <td>S0926580524006149</td>
        <td>2024-12-15</td>
        <td>Automation in Construction</td>
        <td>3D Pixelwise damage mapping using a deep atten...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>Volume 168, Part B</td>
        </tr>
        <tr>
        <th>1</th>
        <td>Akram Akbar; Chun Liu; Zeran Xu</td>
        <td>10.1016/j.aei.2024.102913</td>
        <td>2024-11-16T00:00:00.000Z</td>
        <td>False</td>
        <td>102913</td>
        <td>NaN</td>
        <td>S1474034624005640</td>
        <td>2024-10-31</td>
        <td>Advanced Engineering Informatics</td>
        <td>Scene information guided aerial photogrammetri...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>Volume 62, Part D</td>
        </tr>
        <tr>
        <th>2</th>
        <td>Ruxandra Stoean; Nebojsa Bacanin; Leonard Ionescu</td>
        <td>10.1016/j.culher.2024.07.008</td>
        <td>2024-08-09T00:00:00.000Z</td>
        <td>False</td>
        <td>18</td>
        <td>26.0</td>
        <td>S1296207424001468</td>
        <td>2024-10-31</td>
        <td>Journal of Cultural Heritage</td>
        <td>Bridging the past and present: AI-driven 3D re...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>Volume 69</td>
        </tr>
    </tbody>
    </table>
    </div>