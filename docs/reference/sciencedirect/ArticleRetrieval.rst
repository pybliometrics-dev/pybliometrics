pybliometrics.sciencedirect.ArticleRetrieval
============================================

`ArticleRetrieval()` implements the `ScienceDirect Article (Full Text) Retrieval API <https://dev.elsevier.com/documentation/ArticleRetrievalAPI.wadl>`_.

It accepts any identifier as the main argument.  Most commonly, this will be a `Scopus EID <http://kitchingroup.cheme.cmu.edu/blog/2015/06/07/Getting-a-Scopus-EID-from-a-DOI/>`_, but DOI, Scopus ID (the last part of the EID), PubMed identifier or Publisher Item Identifier (PII) work as well.  `ArticleRetrieval` tries to infer the class itself - to speed this up you can tell the ID type via `id_type`.

The Article (Full Text) API allows a differing information depth via `views <https://dev.elsevier.com/sd_article_retrieval_views.html>`_, some of which are restricted.  The 'META_ABS' view is the most comprehensive among unrestricted views, encompassing all information from other unrestricted views.  It is therefore the default view.  The view with the most information content is 'FULL', which includes all information available with 'META', but is restricted.  Generally, you should always try to use `view='FULL'` when downloading an abstract and fall back to the default otherwise.

In addition, the 'ENTITLED' view lets you check you whether you have access to this class.

.. currentmodule:: pybliometrics.sciencedirect
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: ArticleRetrieval
    :members:
    :inherited-members:

Examples
--------
You initialize the class with an ID that ScienceDirect uses, e.g. the EID:

.. code-block:: python

    >>> from pybliometrics.sciencedirect import ArticleRetrieval, init
    >>> init()
    >>> ar = ArticleRetrieval('S2949948823000112', view='FULL')

`ArticleRetrieval` has 34 properties to interact with, including the `abstract` and the complete `originalText`:

.. code-block:: python

    >>> ar.abstract
    'Artificial Neural Networks (ANNs) are a type of machine learning algorithm inspired by the structure and function of the human brain...'
    >>> ar.originalText
    'serial JL 783536 291210 291861 291871 291876 291884 31 90 Journal of Economy and Technology ...'

In addition to metadata such as `authors`, `coverDate` and `pubType`, `ArticleRetrieval` contains information about the `subjects` of the document:

.. code-block:: python

    >>> ar.subjects
    ['Artificial neural networks', 'Supply chain management']
