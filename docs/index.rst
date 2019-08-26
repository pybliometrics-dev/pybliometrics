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
   :maxdepth: 3
   :hidden:

   examples
   tips
   reference
   configuration
   changelog
   authors
   contributing
