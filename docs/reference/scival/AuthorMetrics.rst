pybliometrics.scival.AuthorMetrics
==================================

`AuthorMetrics()` implements the `SciVal Author Metrics API <https://dev.elsevier.com/documentation/SciValAuthorAPI.wadl>`_.

It accepts one or more Scopus Author IDs as the main argument and retrieves various performance metrics for the specified authors.

.. currentmodule:: pybliometrics.scival
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: AuthorMetrics
    :members:
    :inherited-members:

Examples
--------

You initialize the class with one or more Scopus Author IDs. The argument can be a single ID, a list of IDs, or a comma-separated string of IDs.

.. code-block:: python

    >>> from pybliometrics.scival import AuthorMetrics, init
    >>> init()
    >>> author_metrics = AuthorMetrics("6602819806")

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(author_metrics)
    AuthorMetrics for 1 author(s):
    - Algül, Hana (ID: 6602819806)

There are many properties available that provide different types of metrics. You can explore the available authors:

.. code-block:: python

    >>> author_metrics.authors
    [Author(id=6602819806, name='Algül, Hana', uri='Author/6602819806')]

**Individual Metric Properties**

Each metric property returns a list of `MetricData` namedtuples with the structure: `(entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)` where `entity_id` and `entity_name` refer to the author.

.. code-block:: python

    >>> author_metrics.CitationCount
    [MetricData(entity_id=6602819806, entity_name='Algül, Hana', metric='CitationCount', metric_type='CitationCount', year='all', value=1120, percentage=None, threshold=None)]

    >>> author_metrics.HIndices
    [MetricData(entity_id=6602819806, entity_name='Algül, Hana', metric='h-index', metric_type='HIndices', year='all', value=46.0, percentage=None, threshold=None)]

**Available Metric Properties**:

- `AcademicCorporateCollaboration`
- `AcademicCorporateCollaborationImpact`
- `CitationCount`
- `CitationsPerPublication`
- `CitedPublications`
- `Collaboration`
- `CollaborationImpact`
- `FieldWeightedCitationImpact`
- `HIndices` (only available when `by_year=False`)
- `OutputsInTopCitationPercentiles`
- `PublicationsInTopJournalPercentiles`
- `ScholarlyOutput`

.. note::
   **Unified Data Structure**: AuthorMetrics uses a unified `MetricData` structure with `entity_id` and `entity_name` fields. For authors, these fields contain the author ID and author name respectively. This structure is compatible with `InstitutionMetrics` and other SciVal metric classes, enabling consistent data analysis across different entity types.

**Concatenating Metrics**

Metrics can be concatenated and converted into a pandas DataFrame for easier analysis. 

.. code-block:: python

    >>> import pandas as pd
    >>> collab_data = []
    >>> collab_data.extend(author_metrics.Collaboration)
    >>> collab_data.extend(author_metrics.CollaborationImpact)
    >>> df = pd.DataFrame(collab_data)
    >>> df.head()


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
        <th>entity_id</th>
        <th>entity_name</th>
        <th>metric</th>
        <th>metric_type</th>
        <th>year</th>
        <th>value</th>
        <th>percentage</th>
        <th>threshold</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>Institutional collaboration</td>
        <td>Collaboration</td>
        <td>all</td>
        <td>6.000000</td>
        <td>11.32</td>
        <td>None</td>
        </tr>
        <tr>
        <th>1</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>International collaboration</td>
        <td>Collaboration</td>
        <td>all</td>
        <td>26.000000</td>
        <td>49.06</td>
        <td>None</td>
        </tr>
        <tr>
        <th>2</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>National collaboration</td>
        <td>Collaboration</td>
        <td>all</td>
        <td>21.000000</td>
        <td>39.62</td>
        <td>None</td>
        </tr>
        <tr>
        <th>3</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>Single authorship</td>
        <td>Collaboration</td>
        <td>all</td>
        <td>0.000000</td>
        <td>0.00</td>
        <td>None</td>
        </tr>
        <tr>
        <th>4</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>Institutional collaboration</td>
        <td>CollaborationImpact</td>
        <td>all</td>
        <td>3.500000</td>
        <td>NaN</td>
        <td>None</td>
        </tr>
        <tr>
        <th>5</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>International collaboration</td>
        <td>CollaborationImpact</td>
        <td>all</td>
        <td>28.461538</td>
        <td>NaN</td>
        <td>None</td>
        </tr>
        <tr>
        <th>6</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>National collaboration</td>
        <td>CollaborationImpact</td>
        <td>all</td>
        <td>17.095238</td>
        <td>NaN</td>
        <td>None</td>
        </tr>
        <tr>
        <th>7</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>Single authorship</td>
        <td>CollaborationImpact</td>
        <td>all</td>
        <td>0.000000</td>
        <td>NaN</td>
        <td>None</td>
        </tr>
    </tbody>
    </table>
    </div>


**Multiple Authors**

You can analyze multiple authors simultaneously. Furthermore, you can specify whether you want metrics broken down by year or not. If `by_year=True`, each metric will be returned for each year separately.

.. code-block:: python

    >>> multi_authors = AuthorMetrics([7201667143, 6603480302], by_year=True)
    >>> print(multi_authors)
    AuthorMetrics for 2 author(s):
    - Wolff, Klaus Dietrich (ID: 7201667143)
    - Vogel-Heuser, Birgit (ID: 6603480302)
    >>> # Create a DataFrame from the Collaboration metrics
    >>> df_multi = pd.DataFrame(multi_authors.Collaboration)
    >>> df_multi.head()


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
    <div>
    <table border="1" class="dataframe">
    <thead>
        <tr style="text-align: right;">
        <th></th>
        <th>entity_id</th>
        <th>entity_name</th>
        <th>metric</th>
        <th>metric_type</th>
        <th>year</th>
        <th>value</th>
        <th>percentage</th>
        <th>threshold</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>7201667143</td>
        <td>Wolff, Klaus Dietrich</td>
        <td>Institutional collaboration</td>
        <td>Collaboration</td>
        <td>2024</td>
        <td>3</td>
        <td>30.000002</td>
        <td>None</td>
        </tr>
        <tr>
        <th>1</th>
        <td>7201667143</td>
        <td>Wolff, Klaus Dietrich</td>
        <td>Institutional collaboration</td>
        <td>Collaboration</td>
        <td>2020</td>
        <td>3</td>
        <td>16.666668</td>
        <td>None</td>
        </tr>
        <tr>
        <th>2</th>
        <td>7201667143</td>
        <td>Wolff, Klaus Dietrich</td>
        <td>Institutional collaboration</td>
        <td>Collaboration</td>
        <td>2021</td>
        <td>2</td>
        <td>25.000000</td>
        <td>None</td>
        </tr>
        <tr>
        <th>3</th>
        <td>7201667143</td>
        <td>Wolff, Klaus Dietrich</td>
        <td>Institutional collaboration</td>
        <td>Collaboration</td>
        <td>2022</td>
        <td>0</td>
        <td>0.000000</td>
        <td>None</td>
        </tr>
        <tr>
        <th>4</th>
        <td>7201667143</td>
        <td>Wolff, Klaus Dietrich</td>
        <td>Institutional collaboration</td>
        <td>Collaboration</td>
        <td>2023</td>
        <td>4</td>
        <td>30.769232</td>
        <td>None</td>
        </tr>
    </tbody>
    </table>
    </div>
    </div>


**Filtering Specific Metrics**

You can request only specific metrics to reduce API response size:

.. code-block:: python

    >>> h_index_only = AuthorMetrics("6602819806", metric_types=["HIndices"])
    >>> h_index_only.HIndices
    [MetricData(entity_id=6602819806, entity_name='Algül, Hana', metric='h-index', metric_type='HIndices', year='all', value=46.0, percentage=None, threshold=None)]

    >>> # Multiple specific metrics
    >>> selected_metrics = AuthorMetrics("6602819806", metric_types=["CitationCount", "ScholarlyOutput"])
    >>> selected_metrics.CitationCount
    [MetricData(entity_id=6602819806, entity_name='Algül, Hana', metric='CitationCount', metric_type='CitationCount', year='all', value=1126, percentage=None, threshold=None)]


Downloaded results are cached to expedite subsequent analyses. This information may become outdated. To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as the maximum allowed number of days since the last modification date. For example, if you want to refresh all cached results older than 100 days, set `refresh=100`. Use `author_metrics.get_cache_file_mdate()` to obtain the date of last modification, and `author_metrics.get_cache_file_age()` to determine the number of days since the last modification.
