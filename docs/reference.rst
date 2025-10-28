=============
API Reference
=============

Each class in `pybliometrics` corresponds to one of the `Product Specific APIs <https://dev.elsevier.com/api_docs.html>`_ for Scopus, ScienceDirect and SciVal.  See below links for class reference and examples.

Scopus
======

**Search APIs**

.. toctree::
    :maxdepth: 1

    reference/scopus/AffiliationSearch.rst
    reference/scopus/AuthorSearch.rst
    reference/scopus/ScopusSearch.rst

**Retrieval APIs**

.. toctree::
    :maxdepth: 1

    reference/scopus/AbstractRetrieval.rst
    reference/scopus/AffiliationRetrieval.rst
    reference/scopus/AuthorRetrieval.rst

**Metadata APIs**

.. toctree::
    :maxdepth: 1

    reference/scopus/CitationOverview.rst
    reference/scopus/PlumXMetrics.rst
    reference/scopus/SerialTitleSearch.rst
    reference/scopus/SerialTitleISSN.rst
    reference/scopus/SubjectClassifications.rst

One other Metadata API, the Citations Count Metadata API, is not implemented yet.


ScienceDirect
=============

**Search APIs**

.. toctree::
    :maxdepth: 1

    reference/sciencedirect/ScienceDirectSearch.rst
    reference/sciencedirect/ArticleMetadata.rst

**Retrieval APIs**

.. toctree::
    :maxdepth: 1

    reference/sciencedirect/ArticleEntitlement.rst
    reference/sciencedirect/ArticleRetrieval.rst
    reference/sciencedirect/NonserialTitle.rst
    reference/sciencedirect/ObjectMetadata.rst
    reference/sciencedirect/ObjectRetrieval.rst
    reference/sciencedirect/SerialTitleISSN.rst

One other Retrieval API, the Article Hosting Permission API, is not implemented yet.

**Metadata APIs**

.. toctree::
    :maxdepth: 1

    reference/sciencedirect/SubjectClassifications.rst

Two other Metadata APIs, Serial Title Metadata API and Nonserial Title Metadata API, are not implemented yet.


SciVal
======

.. toctree::
    :maxdepth: 1
    
    reference/scival/AuthorMetrics.rst
    reference/scival/InstitutionLookupMetrics.rst
    reference/scival/PublicationLookup.rst
    reference/scival/TopicLookupMetrics.rst

Several other APIs are not implemented yet.


Initialization
==============

.. _doc-init:

.. currentmodule:: pybliometrics.utils

.. autoclass:: init
   :members:
   :inherited-members:
