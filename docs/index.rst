pybliometrics: Python-based API-Wrapper to access Scopus
========================================================

pybliometrics is an easy to use Python library to pull, cache and extract data from the Scopus database.

.. include:: ../README.rst
   :start-after: example-begin
   :end-before: example-end

.. include:: installation.rst

=======
Classes
=======

pybliometrics provides one class per Scopus API Access Point (see https://dev.elsevier.com/api_docs.html):

.. currentmodule:: pybliometrics

.. autosummary::

   scopus.AbstractRetrieval
   scopus.ContentAffiliationRetrieval
   scopus.AuthorRetrieval
   scopus.AffiliationSearch
   scopus.AuthorSearch
   scopus.ScopusSearch
   scopus.CitationOverview
   scopus.SerialTitle

========
Citation
========

.. include:: ../README.rst
   :start-after: citation-begin
   :end-before: citation-end

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. Hidden links for Navigation side panel
.. toctree::
   :maxdepth: 3
   :hidden:

   examples
   tips
   reference
   configuration
   changelog
   authors
   contributing
