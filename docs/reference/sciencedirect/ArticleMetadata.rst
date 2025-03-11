pybliometrics.sciencedirect.ArticleMetadata
===========================================

`ArticleMetadata()` implements the `ScienceDirect Article Metadata API <https://dev.elsevier.com/documentation/ArticleMetadataAPI.wadl>`_.

The Article Metadata API allows users to search for documents using a Boolean syntax. It offers two views: 'STANDARD' and 'COMPLETE', with the 'COMPLETE' view providing more detailed data.

For a guide on how to query, check the `ScienceDirect Article Metadata Guide <https://dev.elsevier.com/sd_article_meta_tips.html>`_.

.. currentmodule:: pybliometrics.sciencedirect 
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: ArticleMetadata
    :members:
    :inherited-members:

Examples
--------
To use the class provide a query. An invalid search query will result in an error.

.. code-block:: python

    >>> import pandas as pd
    >>> from pybliometrics.sciencedirect import ArticleMetadata, init
    >>> init()
    >>> am = ArticleMetadata('TITLE("Bayesian Network") AND YEAR(2015)')

The `results` property contains a list of the metadata of the documents found. 
The available fields and a description can be found in the `Article Metadata Views <https://dev.elsevier.com/sd_article_meta_tips.html>`_.

.. code-block:: python

    >>> am.results
    [Document(authorKeywords='Flight control system ...', authors='Zhong, Lu;Haijun, Zeng', ...),
     Document(authorKeywords='Bayesian network infer...', authors='Kissinger, Jessica ...', ...),
     Document(authorKeywords='Bayesian networks | Pa...', authors='Druzdzel, Marek J.', ...),
     ...]
    
The field `teaser` from the first document can be accessed as follows:

.. code-block:: python

    >>> am_first_document = am.results[0]
    >>> am_first_document.teaser
    'Traditional probabilistic safety analysis methods are not suitable for modern flight control system with multi-state probability. In this papera Bayesian Network based probabilistic safety model is...'

The `results` can be casted to a pandas DataFrame:

.. code-block:: python

    >>> df = pd.DataFrame(am.results)
    >>> # Print retrieved fields
    >>> df.columns
    Index(['authorKeywords', 'authors', 'available_online_date', 'first_author',
       'abstract_text', 'doi', 'title', 'eid', 'link', 'openArchiveArticle',
       'openaccess_status', 'openaccessArticle', 'openaccessUserLicense',
       'pii', 'aggregationType', 'copyright', 'coverDate', 'coverDisplayDate',
       'edition', 'endingPage', 'isbn', 'publicationName', 'startingPage',
       'teaser', 'api_link', 'publicationType', 'vor_available_online_date'],
      dtype='object')
    >>> # Print shape of the dataframe (rows x columns)
    >>> df.shape
    (71, 27)
    >>> # Print first 5 rows
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
        <th>authorKeywords</th>
        <th>authors</th>
        <th>available_online_date</th>
        <th>first_author</th>
        <th>abstract_text</th>
        <th>doi</th>
        <th>title</th>
        <th>eid</th>
        <th>link</th>
        <th>openArchiveArticle</th>
        <th>...</th>
        <th>coverDisplayDate</th>
        <th>edition</th>
        <th>endingPage</th>
        <th>isbn</th>
        <th>publicationName</th>
        <th>startingPage</th>
        <th>teaser</th>
        <th>api_link</th>
        <th>publicationType</th>
        <th>vor_available_online_date</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>Flight control system | Bayesian network | Uni...</td>
        <td>Zhong, Lu;Haijun, Zeng</td>
        <td>2015-02-14</td>
        <td>Kang, Chen</td>
        <td>Traditional probabilistic safety analysis meth...</td>
        <td>10.1016/j.proeng.2014.12.523</td>
        <td>Research on Probabilistic Safety Analysis Appr...</td>
        <td>1-s2.0-S1877705814036376</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>False</td>
        <td>...</td>
        <td>2015</td>
        <td>None</td>
        <td>184</td>
        <td>None</td>
        <td>Procedia Engineering</td>
        <td>180</td>
        <td>Traditional probabilistic safety analysis meth...</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>fla</td>
        <td>None</td>
        </tr>
        <tr>
        <th>1</th>
        <td>Bayesian network inference | Large-scale data ...</td>
        <td>Kissinger, Jessica C.;Moreno, Alberto;Galinski...</td>
        <td>2015-06-17</td>
        <td>Yin, Weiwei</td>
        <td>High-throughput, genome-scale data present a u...</td>
        <td>10.1016/j.mbs.2015.06.006</td>
        <td>From genome-scale data to models of infectious...</td>
        <td>1-s2.0-S0025556415001248</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>False</td>
        <td>...</td>
        <td>December 2015</td>
        <td>None</td>
        <td>168</td>
        <td>None</td>
        <td>Mathematical Biosciences</td>
        <td>156</td>
        <td>•A generalized workflow for driving model deve...</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>fla</td>
        <td>2015-12-02</td>
        </tr>
        <tr>
        <th>2</th>
        <td>Bayesian networks | Parameter learning | EM al...</td>
        <td>Druzdzel, Marek J.</td>
        <td>2015-03-18</td>
        <td>Ratnapinda, Parot</td>
        <td>We compare three approaches to learning numeri...</td>
        <td>10.1016/j.jal.2015.03.007</td>
        <td>Learning discrete Bayesian network parameters ...</td>
        <td>1-s2.0-S1570868315000464</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>True</td>
        <td>...</td>
        <td>December 2015</td>
        <td>None</td>
        <td>642</td>
        <td>None</td>
        <td>Journal of Applied Logic</td>
        <td>628</td>
        <td>We compare three approaches to learning numeri...</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>fla</td>
        <td>2015-11-14</td>
        </tr>
        <tr>
        <th>3</th>
        <td>None</td>
        <td>Xie, Ashleigh;Tsai, Yi-Chin;Black, Deborah;Di ...</td>
        <td>2015-05-01</td>
        <td>Phan, Kevin</td>
        <td>None</td>
        <td>10.1016/j.hlc.2014.12.097</td>
        <td>Ministernotomy or minithoracotomy for minimall...</td>
        <td>1-s2.0-S1443950614009111</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>False</td>
        <td>...</td>
        <td>2015</td>
        <td>None</td>
        <td>e47</td>
        <td>None</td>
        <td>Heart, Lung and Circulation</td>
        <td>e46</td>
        <td>None</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>abs</td>
        <td>None</td>
        </tr>
        <tr>
        <th>4</th>
        <td>Bayesian Network | Structural Learning Algorit...</td>
        <td>HENRY, Sébastien;OUZROUT, Yacine</td>
        <td>2015-08-31</td>
        <td>DIALLO, Thierno M.L.</td>
        <td>This paper presents the CBNB (Causal Bayesian ...</td>
        <td>10.1016/j.ifacol.2015.06.449</td>
        <td>Bayesian Network Building for Diagnosis in Ind...</td>
        <td>1-s2.0-S2405896315006886</td>
        <td>https://www.sciencedirect.com/science/article/...</td>
        <td>False</td>
        <td>...</td>
        <td>2015</td>
        <td>None</td>
        <td>2416</td>
        <td>None</td>
        <td>IFAC-PapersOnLine</td>
        <td>2411</td>
        <td>This paper presents the CBNB (Causal Bayesian ...</td>
        <td>https://api.elsevier.com/content/article/pii/S...</td>
        <td>fla</td>
        <td>2015-08-31</td>
        </tr>
    </tbody>
    </table>
    <p>5 rows × 27 columns</p>
    </div>