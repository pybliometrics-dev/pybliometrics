All classes (except the reports class) correspond to one of the `Product Specific Scopus APIs <https://dev.elsevier.com/api_docs.html>`_.

There are Search APIs and Retrieval APIs. They have in common that the obtained result is cached in a subfolder in `~/.scopus/` on your hard drive. Subsequent analysis becomes much quicker this way. A boolean `refresh` parameter steers whether this file should be refreshed or not.

.. contents::


Search APIs
===========

.. include:: examples/ScopusSearch.rst

Two other Search APIs, Author Search and Affiliation Search, are not implemented yet.


Retrieval APIs
==============

.. include:: examples/ScopusAbstract.rst

.. include:: examples/ScopusAffiliation.rst

.. include:: examples/ScopusAuthor.rst


report
======

.. include:: examples/report.rst