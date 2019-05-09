Examples
--------

All classes (except the reports class) correspond to one of the `Product Specific Scopus APIs <https://dev.elsevier.com/api_docs.html>`_.

There are Search APIs and Retrieval APIs. They have in common that the obtained result is cached in a subfolder in `~/.scopus/` on your hard drive. Subsequent analysis becomes much quicker this way. A boolean `refresh` parameter steers whether this file should be refreshed or not.

.. contents::


Search APIs
~~~~~~~~~~~

.. toctree::
    examples/AffiliationSearch.rst
    examples/AuthorSearch.rst
    examples/ScopusSearch.rst


Retrieval APIs
~~~~~~~~~~~~~~

.. toctree::
    examples/AbstractRetrieval.rst
    examples/AuthorRetrieval.rst
    examples/ContentAffiliationRetrieval.rst


Metadata APIs
~~~~~~~~~~~~~

.. toctree::
    examples/CitationOverview.rst
    examples/SerialTitle.rst

One other Metadata API, the Subject Classifications, is not implemented yet.
