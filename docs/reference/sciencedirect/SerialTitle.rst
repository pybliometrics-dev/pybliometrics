pybliometrics.sciencedirect.SerialTitle
=======================================

`SerialTitle()` implements the `Serial Title API <https://dev.elsevier.com/documentation/SerialTitleAPI.wadl>`_.  It offers basic information on registered serials (also known as sources), including publisher details, identifiers, and various metrics.
Note that this class accesses the same API endpoint as the :class:`pybliometrics.scopus.SerialTitle` class.

.. currentmodule:: pybliometrics.sciencedirect
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: SerialTitle
    :members:
    :inherited-members:
    :no-index:

Examples
--------

You initialize the class with an ISSN or an E-ISSN (works with and without hyphen, but leading zeros are mandatory):

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.sciencedirect import SerialTitle, init
    >>> init()
    >>> source = SerialTitle("03781119")

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(source)
    'Gene', journal published by 'Elsevier B.V.', is active in Genetics
    Metrics as of 2025-05-18:
        SJR:  year value
            2023 0.725
        SNIP: year value
            2023 0.765
        ISSN: 0378-1119, E-ISSN: 1879-0038, Scopus ID: 15636

The object has a number of attributes but no methods.  For example, information regarding the source itself:

.. code-block:: python

    >>> source.title
    'Gene'
    >>> source.publisher
    'Elsevier B.V.'
    >>> source.issn
    '0378-1119'
    >>> source.eissn
    '1879-0038'
    >>> source.source_id
    15636


Crucially, it provides three metrics: `CiteScore <https://service.elsevier.com/app/answers/detail/a_id/30562/supporthub/scopus/>`_, `SCImago Journal Rank indicator <https://www.scimagojr.com/journalrank.php>`_), and `Source Normalized Impact Factor (SNIP) <https://blog.scopus.com/posts/journal-metrics-in-scopus-source-normalized-impact-per-paper-snip>`_.  This information is presented in lists of two-element tuples, with the first element indicating the year of metric evaluation.

.. code-block:: python

    >>> source.citescoreyearinfolist
    [Citescoreinfolist(year=2023, citescore=6.1),
     Citescoreinfolist(year=2024, citescore=5.1)]
    >>> source.sjrlist
    [(2023, 0.725)]
    >>> source.sniplist
    [(2023, 0.765)]

The `citescoreyearinfolist` property provides detailed information for all available years when `view="CITESCORE"` is used.  It includes the status of the metric, the document count and citation count (of the previous 4 years), the share of documents actually cited, and the rank and percentile for each related ASJC subject:

.. code-block:: python

    >>> import pandas as pd
    >>> source_full = SerialTitle("00368075", view="CITESCORE")
    >>> info = pd.DataFrame(source_full.citescoreyearinfolist)
    >>> print(info)


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
        <th>year</th>
        <th>citescore</th>
        <th>status</th>
        <th>documentcount</th>
        <th>citationcount</th>
        <th>percentcited</th>
        <th>rank</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>2024</td>
        <td>5.1</td>
        <td>In-Progress</td>
        <td>2616</td>
        <td>13257</td>
        <td>79</td>
        <td>[(1311, 153, 56)]</td>
        </tr>
        <tr>
        <th>1</th>
        <td>2023</td>
        <td>6.1</td>
        <td>Complete</td>
        <td>2487</td>
        <td>15073</td>
        <td>81</td>
        <td>[(1311, 129, 62)]</td>
        </tr>
        <tr>
        <th>2</th>
        <td>2022</td>
        <td>7.0</td>
        <td>Complete</td>
        <td>2653</td>
        <td>18487</td>
        <td>84</td>
        <td>[(1311, 96, 70)]</td>
        </tr>
        <tr>
        <th>3</th>
        <td>2021</td>
        <td>7.0</td>
        <td>Complete</td>
        <td>3001</td>
        <td>21031</td>
        <td>86</td>
        <td>[(1311, 88, 73)]</td>
        </tr>
        <tr>
        <th>4</th>
        <td>2020</td>
        <td>5.6</td>
        <td>Complete</td>
        <td>3034</td>
        <td>16950</td>
        <td>83</td>
        <td>[(1311, 110, 66)]</td>
        </tr>
        <tr>
        <th>5</th>
        <td>2019</td>
        <td>4.8</td>
        <td>Complete</td>
        <td>3183</td>
        <td>15368</td>
        <td>79</td>
        <td>[(1311, 128, 60)]</td>
        </tr>
        <tr>
        <th>6</th>
        <td>2018</td>
        <td>4.4</td>
        <td>Complete</td>
        <td>3156</td>
        <td>13862</td>
        <td>74</td>
        <td>[(1311, 141, 56)]</td>
        </tr>
        <tr>
        <th>7</th>
        <td>2017</td>
        <td>5.0</td>
        <td>Complete</td>
        <td>3055</td>
        <td>15223</td>
        <td>80</td>
        <td>[(1311, 119, 62)]</td>
        </tr>
        <tr>
        <th>8</th>
        <td>2016</td>
        <td>4.8</td>
        <td>Complete</td>
        <td>3559</td>
        <td>17163</td>
        <td>80</td>
        <td>[(1311, 113, 63)]</td>
        </tr>
        <tr>
        <th>9</th>
        <td>2015</td>
        <td>4.3</td>
        <td>Complete</td>
        <td>3660</td>
        <td>15710</td>
        <td>78</td>
        <td>[(2700, 1074, 67), (1311, 134, 55)]</td>
        </tr>
        <tr>
        <th>10</th>
        <td>2014</td>
        <td>3.1</td>
        <td>Complete</td>
        <td>3116</td>
        <td>9540</td>
        <td>70</td>
        <td>[(2700, 1412, 56), (1311, 186, 37)]</td>
        </tr>
        <tr>
        <th>11</th>
        <td>2013</td>
        <td>2.2</td>
        <td>Complete</td>
        <td>2336</td>
        <td>5196</td>
        <td>57</td>
        <td>[(2700, 1706, 47), (1311, 209, 28)]</td>
        </tr>
        <tr>
        <th>12</th>
        <td>2012</td>
        <td>2.6</td>
        <td>Complete</td>
        <td>1517</td>
        <td>3979</td>
        <td>53</td>
        <td>[(2700, 1494, 53), (1311, 189, 34)]</td>
        </tr>
        <tr>
        <th>13</th>
        <td>2011</td>
        <td>4.4</td>
        <td>Complete</td>
        <td>934</td>
        <td>4120</td>
        <td>76</td>
        <td>[(2700, 861, 72), (1311, 100, 64)]</td>
        </tr>
    </tbody>
    </table>
    <p>14 rows × 7 columns</p>
    </div>


The `yearly_data` time series includes the number of documents published in a given year.  It contains the number of documents published in this year, the share of review articles thereof, the number and share of not-cited documents, and the number of distinct documents that were cited in this year.


.. code-block:: python

    >>> source.yearly_data[-1]
	Yearlydata(year=2025, publicationcount=403, revpercent=14.14, zerocitessce=335, zerocitespercentsce=83.12655086848635, citecountsce=9307)
    >>> yearly_data = pd.DataFrame(source.yearly_data)
    >>> yearly_data.head()

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
        <th>year</th>
        <th>publicationcount</th>
        <th>revpercent</th>
        <th>zerocitessce</th>
        <th>zerocitespercentsce</th>
        <th>citecountsce</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>1996</td>
        <td>762</td>
        <td>0.00</td>
        <td>18</td>
        <td>2.362205</td>
        <td>21298</td>
        </tr>
        <tr>
        <th>1</th>
        <td>1997</td>
        <td>853</td>
        <td>0.23</td>
        <td>21</td>
        <td>2.461899</td>
        <td>20631</td>
        </tr>
        <tr>
        <th>2</th>
        <td>1998</td>
        <td>631</td>
        <td>0.16</td>
        <td>28</td>
        <td>4.437401</td>
        <td>21748</td>
        </tr>
        <tr>
        <th>3</th>
        <td>1999</td>
        <td>505</td>
        <td>3.37</td>
        <td>5</td>
        <td>0.990099</td>
        <td>22319</td>
        </tr>
        <tr>
        <th>4</th>
        <td>2000</td>
        <td>617</td>
        <td>4.38</td>
        <td>4</td>
        <td>0.648298</td>
        <td>22038</td>
        </tr>
    </tbody>
    </table>
    <p>5 rows × 6 columns</p>
    </div>


By default, `SerialTitle()` retrieves only the most recent metrics, although yearly data is available from 1996 onwards.  If you provide a year or a range of years via the optional parameter `years`, `SerialTitle()` will retrieve information for these years (except for the CiteScore):

.. code-block:: python

    >>> source_y = SerialTitle("2352-7110", years="2017-2019")
    >>> source_y.citescoreyearinfolist
    [Citescoreinfolist(year=2023, citescore=5.5),
     Citescoreinfolist(year=2024, citescore=4.2)]
    >>> source_y.sjrlist
    [(2017, 3.724), (2018, 4.539), (2019, 0.445)]
    >>> source_y.sniplist
    [(2017, 5.287), (2018, 5.153), (2019, 1.025)]


Fields associated with the source are stored as a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_:

.. code-block:: python

    >>> source.subject_area
    [Subjectarea(area='Genetics', abbreviation='BIOC', code=1311)]

Additionally, there is information on Open Access status, which, however, is often empty.

Downloaded results are cached to expedite subsequent analyses. This information may become outdated. To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date. For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.
