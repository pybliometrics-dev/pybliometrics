=============
API Reference
=============

Each classe in `pybliometrics` corresponds to one of the `Product Specific Scopus APIs <https://dev.elsevier.com/api_docs.html>`_.  See below links for class reference and examples.

Search APIs
-----------

.. toctree::
    :maxdepth: 1

    reference/AffiliationSearch.rst
    reference/AuthorSearch.rst
    reference/ScopusSearch.rst

Retrieval APIs
--------------

.. toctree::
    :maxdepth: 1

    reference/AbstractRetrieval.rst
    reference/AffiliationRetrieval.rst
    reference/AuthorRetrieval.rst

Metadata APIs
-------------

.. toctree::
    :maxdepth: 1

    reference/CitationOverview.rst
    reference/PlumXMetrics.rst
    reference/SerialSearch.rst
    reference/SerialTitle.rst
    reference/SubjectClassifications.rst

One other Metadata API, the Citations Count Metadata API, is not implemented yet.

Initialization
--------------

.. _doc-init:

.. currentmodule:: pybliometrics.utils

.. autoclass:: init
   :members:
   :inherited-members:
