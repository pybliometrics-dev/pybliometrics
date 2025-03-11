pybliometrics.scopus.ScienceDirectSearch
==========================================

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
    100%|██████████| 8/8 [00:05<00:00,  1.39it/s]

To access the results, use the attribute `results` which contains a list of `Document` namedtuples.

.. code-block:: python

    >>> # Access the results
    >>> results = sds.results
    [Document(authors='Dong He;Wenhua Qian;Jinde Cao', first_author='Dong He', doi='10.1016/j.cag.2025.104181', title='GEAST-RF: Geometry Enhanced 3D Arbitrary Style Transfer Via Neural Radiance Fields', link='https://www.sciencedirect.com/science/article/pii/S0097849325000202?dgcid=api_sd_search-api-endpoint', load_date='2025-02-16T00:00:00.000Z', openaccess_status=False, pii='S0097849325000202', coverDate='2025-02-16', endingPage=None, publicationName='Computers & Graphics', startingPage='104181', api_link='https://api.elsevier.com/content/article/pii/S0097849325000202', volume=None),
     Document(authors='Qicheng Xu;Min Hu;Xitao Zhang', first_author='Qicheng Xu', doi='10.1016/j.asr.2025.01.065', title='A neural radiance fields method for 3D reconstruction of space target', link='https://www.sciencedirect.com/science/article/pii/S0273117725000973?dgcid=api_sd_search-api-endpoint', load_date='2025-02-01T00:00:00.000Z', openaccess_status=False, pii='S0273117725000973', coverDate='2025-02-01', endingPage=None, publicationName='Advances in Space Research', startingPage=None, api_link='https://api.elsevier.com/content/article/pii/S0273117725000973', volume=None),
     Document(authors='Jian Liu;Zhen Yu', first_author='Jian Liu', doi='10.1016/j.neucom.2025.129420', title='SA3D-L: A lightweight model for 3D object segmentation using neural radiance fields', link='https://www.sciencedirect.com/science/article/pii/S092523122500092X?dgcid=api_sd_search-api-endpoint', load_date='2025-01-14T00:00:00.000Z', openaccess_status=False, pii='S092523122500092X', coverDate='2025-03-28', endingPage=None, publicationName='Neurocomputing', startingPage='129420', api_link='https://api.elsevier.com/content/article/pii/S092523122500092X', volume='623'),
     ...]

The list of results can be cast into a Pandas DataFrame.

.. code-block:: python

    >>> import pandas as pd
    >>> # Cast results to a pandas DataFrame
    >>> df = pd.DataFrame(sds.results)
    >>> # Display available fields
    >>> df.columns
    Index(['eid', 'filename', 'height', 'mimetype', 'ref', 'size', 'type', 'url',
       'width'],
      dtype='object')
    >>> # Get shape of the DataFrame (rows x columns)
    (200, 14)
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
        <td>Dong He;Wenhua Qian;Jinde Cao</td>
        <td>Dong He</td>
        <td>10.1016/j.cag.2025.104181</td>
        <td>GEAST-RF: Geometry Enhanced 3D Arbitrary Style...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>2025-02-16T00:00:00.000Z</td>
        <td>False</td>
        <td>S0097849325000202</td>
        <td>2025-02-16</td>
        <td>None</td>
        <td>Computers &amp; Graphics</td>
        <td>104181</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>None</td>
        </tr>
        <tr>
        <th>1</th>
        <td>Qicheng Xu;Min Hu;Xitao Zhang</td>
        <td>Qicheng Xu</td>
        <td>10.1016/j.asr.2025.01.065</td>
        <td>A neural radiance fields method for 3D reconst...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>2025-02-01T00:00:00.000Z</td>
        <td>False</td>
        <td>S0273117725000973</td>
        <td>2025-02-01</td>
        <td>None</td>
        <td>Advances in Space Research</td>
        <td>None</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>None</td>
        </tr>
        <tr>
        <th>2</th>
        <td>Jian Liu;Zhen Yu</td>
        <td>Jian Liu</td>
        <td>10.1016/j.neucom.2025.129420</td>
        <td>SA3D-L: A lightweight model for 3D object segm...</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>2025-01-14T00:00:00.000Z</td>
        <td>False</td>
        <td>S092523122500092X</td>
        <td>2025-03-28</td>
        <td>None</td>
        <td>Neurocomputing</td>
        <td>129420</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>623</td>
        </tr>
    </tbody>
    </table>
    </div>

