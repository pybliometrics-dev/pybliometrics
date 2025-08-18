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

    >>> import pybliometrics
    >>> from pybliometrics.scival import AuthorMetrics
    >>> pybliometrics.scival.init()
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

Each metric property returns a list of `MetricData` namedtuples with the structure: `(author_id, author_name, metric, metric_type, year, value, percentage, threshold)`.

.. code-block:: python

    >>> author_metrics.CitationCount
    [MetricData(author_id=6602819806, author_name='Algül, Hana', metric='CitationCount', 
                metric_type='Citation count', year='all', value=1234, percentage=85.5, threshold=None)]

    >>> author_metrics.HIndices
    [MetricData(author_id=6602819806, author_name='Algül, Hana', metric='HIndices', 
                metric_type='h-index', year='all', value=46.0, percentage=None, threshold=None)]

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

**Getting All Metrics at Once**

You can retrieve all available metrics in a single list using the `all_metrics` property:

.. code-block:: python

    >>> all_data = author_metrics.all_metrics
    >>> len(all_data)
    29
    >>> # Convert to pandas DataFrame for analysis
    >>> import pandas as pd
    >>> df = pd.DataFrame(all_data)
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
        <th>author_id</th>
        <th>author_name</th>
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
        <td>AcademicCorporateCollaboration</td>
        <td>Academic-corporate collaboration</td>
        <td>all</td>
        <td>12.000000</td>
        <td>22.64151</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>1</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>AcademicCorporateCollaboration</td>
        <td>No academic-corporate collaboration</td>
        <td>all</td>
        <td>41.000000</td>
        <td>77.35849</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>2</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>AcademicCorporateCollaborationImpact</td>
        <td>Academic-corporate collaboration</td>
        <td>all</td>
        <td>43.166668</td>
        <td>NaN</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>3</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>AcademicCorporateCollaborationImpact</td>
        <td>No academic-corporate collaboration</td>
        <td>all</td>
        <td>14.682927</td>
        <td>NaN</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>4</th>
        <td>6602819806</td>
        <td>Algül, Hana</td>
        <td>Collaboration</td>
        <td>Institutional collaboration</td>
        <td>all</td>
        <td>6.000000</td>
        <td>11.32000</td>
        <td>NaN</td>
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
    >>> df = pd.DataFrame(multi_authors.all_metrics)
    >>> df.tail(5)


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
        <th>author_id</th>
        <th>author_name</th>
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
        <th>275</th>
        <td>6603480302</td>
        <td>Vogel-Heuser, Birgit</td>
        <td>OutputsInTopCitationPercentiles</td>
        <td>None</td>
        <td>2024</td>
        <td>5.0</td>
        <td>13.157895</td>
        <td>25.0</td>
        </tr>
        <tr>
        <th>276</th>
        <td>6603480302</td>
        <td>Vogel-Heuser, Birgit</td>
        <td>OutputsInTopCitationPercentiles</td>
        <td>None</td>
        <td>2020</td>
        <td>5.0</td>
        <td>10.000000</td>
        <td>25.0</td>
        </tr>
        <tr>
        <th>277</th>
        <td>6603480302</td>
        <td>Vogel-Heuser, Birgit</td>
        <td>OutputsInTopCitationPercentiles</td>
        <td>None</td>
        <td>2021</td>
        <td>14.0</td>
        <td>27.450981</td>
        <td>25.0</td>
        </tr>
        <tr>
        <th>278</th>
        <td>6603480302</td>
        <td>Vogel-Heuser, Birgit</td>
        <td>OutputsInTopCitationPercentiles</td>
        <td>None</td>
        <td>2022</td>
        <td>8.0</td>
        <td>24.242424</td>
        <td>25.0</td>
        </tr>
        <tr>
        <th>279</th>
        <td>6603480302</td>
        <td>Vogel-Heuser, Birgit</td>
        <td>OutputsInTopCitationPercentiles</td>
        <td>None</td>
        <td>2023</td>
        <td>1.0</td>
        <td>2.173913</td>
        <td>25.0</td>
        </tr>
    </tbody>
    </table>
    </div>


**Filtering Specific Metrics**

You can request only specific metrics to reduce API response size:

.. code-block:: python

    >>> h_index_only = AuthorMetrics("6602819806", metric_types=["HIndices"])
    >>> h_index_only.HIndices
    [MetricData(author_id=6602819806, author_name='Algül, Hana', metric='HIndices', 
                metric_type='h-index', year='all', value=46.0, percentage=None, threshold=None)]

    >>> # Multiple specific metrics
    >>> selected_metrics = AuthorMetrics("6602819806", 
    ...                                  metric_types=["CitationCount", "ScholarlyOutput"])


Downloaded results are cached to expedite subsequent analyses. This information may become outdated. To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as the maximum allowed number of days since the last modification date. For example, if you want to refresh all cached results older than 100 days, set `refresh=100`. Use `author_metrics.get_cache_file_mdate()` to obtain the date of last modification, and `author_metrics.get_cache_file_age()` to determine the number of days since the last modification.
