pybliometrics.sciencedirect.ScienceDirectSearch
=================================================

`ScopusSearch()` implements the `ScienceDirect Search API <https://nonprod-devportal.elsevier.com/documentation/ScienceDirectSearchAPI.wadl>`_.  It executes a query to search for documents and retrieves the resulting records.
Any query that works in the `Advanced Document Search on sciencedirect.com <https://www.sciencedirect.com/search/entry>`_ will work.
For a complete guide on how to query check the `documentation <https://service.elsevier.com/app/answers/detail/a_id/25974/supporthub/sciencedirect/>`_.

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

The class is initialized with a search query. To see the download progress, set `verbose=True`.

.. code-block:: python

    >>> from pybliometrics.sciencedirect import ScienceDirectSearch, init
    >>> init()
    >>> # Retrieve documents based on the search query  
    >>> sds = ScienceDirectSearch('"neural radiance fields" AND "3D" AND YEAR(2024)', verbose=True)
    Downloading results for query ""neural radiance fields" AND "3D" AND YEAR(2024)":
    100%|██████████| 6/6 [00:04<00:00,  1.04it/s]

To access the results, use the attribute `results` which contains a list of `Document` namedtuples.

.. code-block:: python

    >>> # Access the results
    >>> sds.results
    [Document(authors='Lizhi Jiang;Peng W. Chee;Longsheng Fu', first_author='Lizhi Jiang', doi='10.1016/j.compag.2026.112063', title='Robot-assisted Neural Radiance fields for plot-level cotton crop 3D reconstruction and yield estimation', link='https://www.sciencedirect.com/science/article/pii/S0168169926006587?dgcid=api_sd_search-api-endpoint', load_date='2026-06-22T00:00:00.000Z', openaccess_status=False, pii='S0168169926006587', coverDate='2026-09-15', endingPage=None, publicationName='Computers and Electronics in Agriculture', startingPage='112063', api_link='https://api.elsevier.com/content/article/pii/S0168169926006587', volume='252'),
     Document(authors='Zhi Wang;Shuaipeng Fei;Yuntao Ma', first_author='Zhi Wang', doi='10.1016/j.compag.2026.111790', title='Beetroot type classification based on 3D structure constructed with neural radiance fields', link='https://www.sciencedirect.com/science/article/pii/S0168169926003856?dgcid=api_sd_search-api-endpoint', load_date='2026-04-20T00:00:00.000Z', openaccess_status=False, pii='S0168169926003856', coverDate='2026-07-01', endingPage=None, publicationName='Computers and Electronics in Agriculture', startingPage='111790', api_link='https://api.elsevier.com/content/article/pii/S0168169926003856', volume='248'),
     Document(authors='Wei Zhou;Wenbo Chu;Keqiang Li', first_author='Wei Zhou', doi='10.1016/j.cjme.2025.100093', title='Autonomous driving scenario generation based on neural radiance fields or 3D Gaussian splatting: State-of-the-art investigations, reviews, and perspectives', link='https://www.sciencedirect.com/science/article/pii/S1000934525000975?dgcid=api_sd_search-api-endpoint', load_date='2025-09-30T00:00:00.000Z', openaccess_status=True, pii='S1000934525000975', coverDate='2026-01-31', endingPage=None, publicationName='Chinese Journal of Mechanical Engineering', startingPage='100093', api_link='https://api.elsevier.com/content/article/pii/S1000934525000975', volume='39'),
     ...]

The list of results can be cast into a Pandas DataFrame.

.. code-block:: python

    >>> import pandas as pd
    >>> # Cast results to a pandas DataFrame
    >>> df = pd.DataFrame(sds.results)
    >>> # Display available fields
    >>> df.columns
    Index(['authors', 'first_author', 'doi', 'title', 'link', 'load_date',
           'openaccess_status', 'pii', 'coverDate', 'endingPage',
           'publicationName', 'startingPage', 'api_link', 'volume'],
          dtype='str')
    >>> # Get shape of the DataFrame (rows x columns)
    >>> df.shape
    (506, 14)
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
        <th>first_author</th>
        <th>doi</th>
        <th>title</th>
        <th>link</th>
        <th>load_date</th>
        <th>openaccess_status</th>
        <th>pii</th>
        <th>coverDate</th>
        <th>endingPage</th>
        <th>publicationName</th>
        <th>startingPage</th>
        <th>api_link</th>
        <th>volume</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>Lizhi Jiang;Peng W. Chee;Longsheng Fu</td>
        <td>Lizhi Jiang</td>
        <td>10.1016/j.compag.2026.112063</td>
        <td>Robot-assisted Neural Radiance fields for plot...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>2026-06-22T00:00:00.000Z</td>
        <td>False</td>
        <td>S0168169926006587</td>
        <td>2026-09-15</td>
        <td>NaN</td>
        <td>Computers and Electronics in Agriculture</td>
        <td>112063</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>252</td>
        </tr>
        <tr>
        <th>1</th>
        <td>Zhi Wang;Shuaipeng Fei;Yuntao Ma</td>
        <td>Zhi Wang</td>
        <td>10.1016/j.compag.2026.111790</td>
        <td>Beetroot type classification based on 3D struc...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>2026-04-20T00:00:00.000Z</td>
        <td>False</td>
        <td>S0168169926003856</td>
        <td>2026-07-01</td>
        <td>NaN</td>
        <td>Computers and Electronics in Agriculture</td>
        <td>111790</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>248</td>
        </tr>
        <tr>
        <th>2</th>
        <td>Wei Zhou;Wenbo Chu;Keqiang Li</td>
        <td>Wei Zhou</td>
        <td>10.1016/j.cjme.2025.100093</td>
        <td>Autonomous driving scenario generation based o...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>2025-09-30T00:00:00.000Z</td>
        <td>True</td>
        <td>S1000934525000975</td>
        <td>2026-01-31</td>
        <td>NaN</td>
        <td>Chinese Journal of Mechanical Engineering</td>
        <td>100093</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>39</td>
        </tr>
    </tbody>
    </table>
    </div>

