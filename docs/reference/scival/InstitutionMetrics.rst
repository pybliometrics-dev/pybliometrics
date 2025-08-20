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
                metric_type='CitationCount', year='all', value=368527, percentage=None, threshold=None)]

For **nested metrics** (like CollaborationImpact), `metric_type` contains the main category and `metric` contains the specific sub-type:

.. code-block:: python

    >>> institution_metrics.CollaborationImpact
    [MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='Institutional collaboration', 
                metric_type='CollaborationImpact', year='all', value=8.610204, percentage=None, threshold=None),
     MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='International collaboration', 
                metric_type='CollaborationImpact', year='all', value=22.430689, percentage=None, threshold=None),
     MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='National collaboration', 
                metric_type='CollaborationImpact', year='all', value=9.935493, percentage=None, threshold=None),
     MetricData(entity_id=309021, entity_name='Humboldt University of Berlin', metric='Single authorship', 
                metric_type='CollaborationImpact', year='all', value=3.187361, percentage=None, threshold=None)]

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

**Concatenating Metrics**



.. code-block:: python

    >>> import pandas as pd
    >>>
    >>> collab_data = []
    >>> collab_data.extend(institution_metrics.Collaboration)
    >>> collab_data.extend(institution_metrics.CollaborationImpact)
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
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>Institutional collaboration</td>
        <td>Collaboration</td>
        <td>all</td>
        <td>980.000000</td>
        <td>4.32</td>
        <td>None</td>
        </tr>
        <tr>
        <th>1</th>
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>International collaboration</td>
        <td>Collaboration</td>
        <td>all</td>
        <td>12754.000000</td>
        <td>56.16</td>
        <td>None</td>
        </tr>
        <tr>
        <th>2</th>
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>National collaboration</td>
        <td>Collaboration</td>
        <td>all</td>
        <td>6728.000000</td>
        <td>29.63</td>
        <td>None</td>
        </tr>
        <tr>
        <th>3</th>
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>Single authorship</td>
        <td>Collaboration</td>
        <td>all</td>
        <td>2247.000000</td>
        <td>9.89</td>
        <td>None</td>
        </tr>
        <tr>
        <th>4</th>
        <td>309021</td>
        <td>Humboldt University of Berlin</td>
        <td>Institutional collaboration</td>
        <td>CollaborationImpact</td>
        <td>all</td>
        <td>8.610204</td>
        <td>NaN</td>
        <td>None</td>
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
    >>> # Get CitedPublications metrics
    >>> df = pd.DataFrame(multi_institutions.CitedPublications)
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
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2024</td>
        <td>2400</td>
        <td>66.133920</td>
        <td>None</td>
        </tr>
        <tr>
        <th>1</th>
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2020</td>
        <td>3294</td>
        <td>89.462250</td>
        <td>None</td>
        </tr>
        <tr>
        <th>2</th>
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2021</td>
        <td>3385</td>
        <td>88.404290</td>
        <td>None</td>
        </tr>
        <tr>
        <th>3</th>
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2022</td>
        <td>3209</td>
        <td>86.472650</td>
        <td>None</td>
        </tr>
        <tr>
        <th>4</th>
        <td>309050</td>
        <td>Technical University of Berlin</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2023</td>
        <td>3044</td>
        <td>80.529100</td>
        <td>None</td>
        </tr>
        <tr>
        <th>5</th>
        <td>309076</td>
        <td>Heidelberg University</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2024</td>
        <td>5937</td>
        <td>72.517410</td>
        <td>None</td>
        </tr>
        <tr>
        <th>6</th>
        <td>309076</td>
        <td>Heidelberg University</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2020</td>
        <td>7423</td>
        <td>92.005455</td>
        <td>None</td>
        </tr>
        <tr>
        <th>7</th>
        <td>309076</td>
        <td>Heidelberg University</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2021</td>
        <td>7828</td>
        <td>90.864770</td>
        <td>None</td>
        </tr>
        <tr>
        <th>8</th>
        <td>309076</td>
        <td>Heidelberg University</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2022</td>
        <td>7354</td>
        <td>88.166885</td>
        <td>None</td>
        </tr>
        <tr>
        <th>9</th>
        <td>309076</td>
        <td>Heidelberg University</td>
        <td>CitedPublications</td>
        <td>CitedPublications</td>
        <td>2023</td>
        <td>6921</td>
        <td>85.150100</td>
        <td>None</td>
        </tr>
    </tbody>
    </table>
    </div>


Downloaded results are cached to expedite subsequent analyses. This information may become outdated. To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as the maximum allowed number of days since the last modification date. For example, if you want to refresh all cached results older than 100 days, set `refresh=100`. Use `institution_metrics.get_cache_file_mdate()` to obtain the date of last modification, and `institution_metrics.get_cache_file_age()` to determine the number of days since the last modification.
