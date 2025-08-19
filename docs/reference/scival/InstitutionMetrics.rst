pybliometrics.scival.InstitutionMetrics
=======================================

`InstitutionMetrics()` implements the `SciVal Institution Metrics API <https://dev.elsevier.com/documentation/SciValInstitutionAPI.wadl>`_.

It accepts one or more SciVal Institution IDs as the main argument and retrieves various performance metrics for the specified institutions.

.. currentmodule:: pybliometrics.scival
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: InstitutionMetrics
    :members:
    :inherited-members:

Examples
--------

You initialize the class with one or more SciVal Institution IDs. The argument can be a single ID, a list of IDs, or a comma-separated string of IDs.

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scival import InstitutionMetrics
    >>> pybliometrics.scival.init()
    >>> institution_metrics = InstitutionMetrics("309021")

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(institution_metrics)
    InstitutionMetrics for 1 institution(s):
    - Humboldt University of Berlin (ID: 309021)

There are many properties available that provide different types of metrics. You can explore the available institutions:

.. code-block:: python

    >>> institution_metrics.institutions
    [Institution(id=309021, name='Humboldt University of Berlin', uri='Institution/309021')]

**Individual Metric Properties**

Each metric property returns a list of `MetricData` namedtuples with the structure: `(entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)` where `entity_id` and `entity_name` refer to the institution.

.. code-block:: python

    >>> institution_metrics.CitationCount
    [MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='CitationCount', 
                metric_type=None, year='all', value=368527, percentage=None, threshold=None)]

    >>> institution_metrics.CollaborationImpact
    [MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='CollaborationImpact', 
                metric_type='Institutional collaboration', year='all', value=8.610204, percentage=None, threshold=None),
     MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='CollaborationImpact', 
                metric_type='International collaboration', year='all', value=22.430689, percentage=None, threshold=None),
     MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='CollaborationImpact', 
                metric_type='National collaboration', year='all', value=9.935493, percentage=None, threshold=None),
     MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='CollaborationImpact', 
                metric_type='Single authorship', year='all', value=3.187361, percentage=None, threshold=None)]

**Available Metric Properties**:

- `AcademicCorporateCollaboration`
- `AcademicCorporateCollaborationImpact`
- `CitationCount`
- `CitationsPerPublication`
- `CitedPublications`
- `Collaboration`
- `CollaborationImpact`
- `FieldWeightedCitationImpact`
- `OutputsInTopCitationPercentiles`
- `PublicationsInTopJournalPercentiles`
- `ScholarlyOutput`

.. note::
   **Unified Data Structure**: InstitutionMetrics uses a unified `MetricData` structure with `entity_id` and `entity_name` fields. For institutions, these fields contain the institution ID and institution name respectively. This structure is compatible with `AuthorMetrics` and other SciVal metric classes, enabling consistent data analysis across different entity types.

**Getting All Metrics at Once**

You can retrieve all available metrics in a single list using the `all_metrics` property:

.. code-block:: python

    >>> all_data = institution_metrics.all_metrics
    >>> len(all_data)
    28
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
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>AcademicCorporateCollaboration</td>
        <td>Academic-corporate collaboration</td>
        <td>all</td>
        <td>1015.000000</td>
        <td>4.469594</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>1</th>
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>AcademicCorporateCollaboration</td>
        <td>No academic-corporate collaboration</td>
        <td>all</td>
        <td>21694.000000</td>
        <td>95.530410</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>2</th>
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>AcademicCorporateCollaborationImpact</td>
        <td>Academic-corporate collaboration</td>
        <td>all</td>
        <td>59.104435</td>
        <td>NaN</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>3</th>
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>AcademicCorporateCollaborationImpact</td>
        <td>No academic-corporate collaboration</td>
        <td>all</td>
        <td>14.222181</td>
        <td>NaN</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>4</th>
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>Collaboration</td>
        <td>Institutional collaboration</td>
        <td>all</td>
        <td>980.000000</td>
        <td>4.320000</td>
        <td>NaN</td>
        </tr>
    </tbody>
    </table>
    </div>


**Multiple Institutions**

You can analyze multiple institutions simultaneously and retrieve metrics `by_year`:

.. code-block:: python

    >>> multi_institutions = InstitutionMetrics([309050, 309076], by_year=True)
    >>> print(multi_institutions)
    InstitutionMetrics for 2 institution(s):
    - Technical University of Berlin (ID: 309050)
    - Heidelberg University  (ID: 309076)
    >>> # Get all collaboration metrics for all institutions
    >>> df = pd.DataFrame(multi_institutions.all_metrics)
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
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>AcademicCorporateCollaboration</td>
        <td>Academic-corporate collaboration</td>
        <td>2024</td>
        <td>282.0</td>
        <td>7.770736</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>1</th>
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>AcademicCorporateCollaboration</td>
        <td>Academic-corporate collaboration</td>
        <td>2020</td>
        <td>285.0</td>
        <td>7.740358</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>2</th>
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>AcademicCorporateCollaboration</td>
        <td>Academic-corporate collaboration</td>
        <td>2021</td>
        <td>250.0</td>
        <td>6.529120</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>3</th>
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>AcademicCorporateCollaboration</td>
        <td>Academic-corporate collaboration</td>
        <td>2022</td>
        <td>249.0</td>
        <td>6.709782</td>
        <td>NaN</td>
        </tr>
        <tr>
        <th>4</th>
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>AcademicCorporateCollaboration</td>
        <td>Academic-corporate collaboration</td>
        <td>2023</td>
        <td>253.0</td>
        <td>6.693122</td>
        <td>NaN</td>
        </tr>
    </tbody>
    </table>
    </div>


Downloaded results are cached to expedite subsequent analyses. This information may become outdated. To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as the maximum allowed number of days since the last modification date. For example, if you want to refresh all cached results older than 100 days, set `refresh=100`. Use `institution_metrics.get_cache_file_mdate()` to obtain the date of last modification, and `institution_metrics.get_cache_file_age()` to determine the number of days since the last modification.
