##########################################################################
pybliometrics: Python-based API-Wrapper to access Scopus and ScienceDirect
##########################################################################

pybliometrics is an easy to use Python library to pull, cache and extract data from the Scopus database and its sister databases like ScienceDirect. It provides one class per `API Access Point <https://dev.elsevier.com/api_docs.html>`_:

.. include:: ../README.rst
   :start-after: example-begin
   :end-before: example-end

.. include:: installation.rst

==========================
Classes for the Scopus API
==========================

.. currentmodule:: pybliometrics.scopus

.. autosummary::

   AbstractRetrieval
   AffiliationRetrieval
   AffiliationSearch
   AuthorRetrieval
   AuthorSearch
   CitationOverview
   PlumXMetrics
   ScopusSearch
   SerialSearch
   SerialTitle
   SubjectClassifications

=================================
Classes for the ScienceDirect API
=================================

.. currentmodule:: pybliometrics.sciencedirect

.. autosummary::

   ArticleEntitlement
   ArticleMetadata
   ArticleRetrieval
   ObjectMetadata
   ObjectRetrieval
   ScienceDirectSearch
   ScDirSubjectClassifications

========
Citation
========

If pybliometrics helped you getting data for research, please cite our corresponding paper:

* Rose, Michael E. and John R. Kitchin: "`pybliometrics: Scriptable bibliometrics using a Python interface to Scopus <https://www.sciencedirect.com/science/article/pii/S2352711019300573>`_", SoftwareX 10 (2019) 100263.

Citing the paper helps the development of pybliometrics, because it justifies funneling resources into the development.  It also signals that you obtained data from Scopus in a transparent and replicable way.

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. Hidden links for Navigation side panel
.. toctree::
   :maxdepth: 4
   :hidden:

   reference
   access
   configuration
   tips
   changelog
   authors
   contributing
