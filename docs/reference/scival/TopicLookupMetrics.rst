pybliometrics.scival.TopicLookupMetrics
========================================

`TopicLookupMetrics()` implements the `metrics` endpoint of the `SciVal TopicLookup API <https://dev.elsevier.com/documentation/SciValTopicAPI.wadl>`_.

It accepts one or more SciVal Topic IDs as the main argument and retrieves various performance metrics for the specified topics.

.. currentmodule:: pybliometrics.scival
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: TopicLookupMetrics
    :members:
    :inherited-members:

Examples
--------

You initialize the class with one or more SciVal Topic IDs. The argument can be a single ID, a list of IDs, or a comma-separated string of IDs.

.. code-block:: python

    >>> from pybliometrics.scival import TopicLookupMetrics, init
    >>> init()
    >>> topic_metrics = TopicLookupMetrics("2782")

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(topic_metrics)
    TopicLookupMetrics for 1 topic(s):
    - Enhancing Reproducibility through Open Science Practices (ID: 2782)

There are many properties available that provide different types of metrics. You can explore the available topics:

.. code-block:: python

    >>> topic_metrics.topics
    [Topic(id=2782, name='Enhancing Reproducibility through Open Science Practices', uri='Topic/2782', 
           prominencePercentile=99.044914, scholarlyOutput=2455)]

**Properties with** `MetricData`

Properties like `CitationCount` return a list of `MetricData` namedtuples with the structure: `(entity_id, entity_name, metric, year, value, percentage, threshold)` where `entity_id` and `entity_name` refer to the topic.

.. code-block:: python

    >>> topic_metrics.CitationCount
    [MetricData(entity_id=2782, entity_name='Enhancing Reproducibility through Open Science Practices', 
                metric='CitationCount', year='all', value=32637, percentage=None, threshold=None)]

Other properties that also retruen `MetricData` include `AuthorCount`, `FieldWeightedCitationImpact`, `InstitutionCount`, and `ScholarlyOutput`.

**Specialized properties**

Properties like `TopAuthors` return specialized namedtuples with different structures.

.. code-block:: python

    >>> topic_metrics.TopAuthors[:3]
    [TopAuthor(entity_id=2782, entity_name='Enhancing Reproducibility through Open Science Practices', 
               author_id=6602573237, author_name='Vazire, Simine', publicationCount=29),
     TopAuthor(entity_id=2782, entity_name='Enhancing Reproducibility through Open Science Practices', 
               author_id=57226848754, author_name='Ioannidis, John P.A.', publicationCount=28),
     TopAuthor(entity_id=2782, entity_name='Enhancing Reproducibility through Open Science Practices', 
               author_id=23984790800, author_name='Dreber, Anna', publicationCount=22)]

Other specialized properties include `CorePapers`, `MostRecentlyPublishedPapers`, `RelatedTopics`, `TopCitedPublications`, `TopInstitutions`, `TopJournals`, and `TopKeywords`.

**Concatenating Metrics**

You can concatenate properties with `MetricData` into a single DataFrame for easier analysis.

.. code-block:: python

    >>> import pandas as pd
    >>>
    >>> data = []
    >>> data.extend(topics_metrics.CitationCount)
    >>> data.extend(topics_metrics.ScholarlyOutput)
    >>> df = pd.DataFrame(data)
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
        <th>year</th>
        <th>value</th>
        <th>percentage</th>
        <th>threshold</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>9350</td>
        <td>Molecular Catalysts for Hydrogen Production Ad...</td>
        <td>CitationCount</td>
        <td>all</td>
        <td>10707</td>
        <td>None</td>
        <td>None</td>
        </tr>
        <tr>
        <th>1</th>
        <td>11084</td>
        <td>Machine Learning Potentials in Molecular Simul...</td>
        <td>CitationCount</td>
        <td>all</td>
        <td>66222</td>
        <td>None</td>
        <td>None</td>
        </tr>
        <tr>
        <th>2</th>
        <td>9350</td>
        <td>Molecular Catalysts for Hydrogen Production Ad...</td>
        <td>ScholarlyOutput</td>
        <td>all</td>
        <td>809</td>
        <td>None</td>
        <td>None</td>
        </tr>
        <tr>
        <th>3</th>
        <td>11084</td>
        <td>Machine Learning Potentials in Molecular Simul...</td>
        <td>ScholarlyOutput</td>
        <td>all</td>
        <td>2405</td>
        <td>None</td>
        <td>None</td>
        </tr>
    </tbody>
    </table>
    </div>


**Multiple Topics**

You can analyze multiple topics simultaneously and retrieve metrics `by_year`:

.. code-block:: python

    >>> multi_topics = TopicLookupMetrics(["9350", "11084"], by_year=True)
    >>> print(multi_topics)
    TopicLookupMetrics for 2 topic(s):
    - Molecular Catalysts for Hydrogen Production Advances (ID: 9350)
    - Machine Learning Potentials in Molecular Simulations (ID: 11084)

Properties can always be converted to a DataFrame for easier analysis.

.. code-block:: python

    >>> df = pd.DataFrame(multi_topics.ScholarlyOutput)
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
        <th>year</th>
        <th>value</th>
        <th>percentage</th>
        <th>threshold</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>2782</td>
        <td>Enhancing Reproducibility through Open Science Practices</td>
        <td>ScholarlyOutput</td>
        <td>2024</td>
        <td>580</td>
        <td>None</td>
        <td>None</td>
        </tr>
        <tr>
        <th>1</th>
        <td>2782</td>
        <td>Enhancing Reproducibility through Open Science Practices</td>
        <td>ScholarlyOutput</td>
        <td>2020</td>
        <td>394</td>
        <td>None</td>
        <td>None</td>
        </tr>
        <tr>
        <th>2</th>
        <td>2782</td>
        <td>Enhancing Reproducibility through Open Science Practices</td>
        <td>ScholarlyOutput</td>
        <td>2021</td>
        <td>462</td>
        <td>None</td>
        <td>None</td>
        </tr>
        <tr>
        <th>3</th>
        <td>2782</td>
        <td>Enhancing Reproducibility through Open Science Practices</td>
        <td>ScholarlyOutput</td>
        <td>2022</td>
        <td>480</td>
        <td>None</td>
        <td>None</td>
        </tr>
        <tr>
        <th>4</th>
        <td>2782</td>
        <td>Enhancing Reproducibility through Open Science Practices</td>
        <td>ScholarlyOutput</td>
        <td>2023</td>
        <td>539</td>
        <td>None</td>
        <td>None</td>
        </tr>
    </tbody>
    </table>
    </div>


Downloaded results are cached to expedite subsequent analyses. This information may become outdated. To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as the maximum allowed number of days since the last modification date. For example, if you want to refresh all cached results older than 100 days, set `refresh=100`. Use `topic_metrics.get_cache_file_mdate()` to obtain the date of last modification, and `topic_metrics.get_cache_file_age()` to determine the number of days since the last modification.