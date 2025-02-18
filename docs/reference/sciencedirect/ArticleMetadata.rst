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

