pybliometrics: Python-based API-Wrapper to access Scopus
========================================================

pybliometrics is an easy to use Python library to pull, cache and extract data from the Scopus database.

.. include:: installation.rst


=======
Classes
=======

pybliometrics provides classes to interact with the various Scopus APIs (see https://dev.elsevier.com/api_docs.html):

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

* Rose, Michael E. and John R. Kitchin (2019): "`scopus: Scriptable bibliometrics using a Python interface to Scopus <https://raw.githubusercontent.com/scopus-api/pybliometrics/master/meta/RoseJohn2019_scopus.pdf>`_", Max Planck Institute for Innovation and Competition Research Paper No. 19-03.

Citing the paper helps the development of pybliometrics, because it justifies funneling resources into the development.

==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. Hidden links for Navigation side panel
.. toctree::
   :maxdepth: 2
   :hidden:

   examples
   tips
   reference
   configuration
   changelog
   authors
   contributing
