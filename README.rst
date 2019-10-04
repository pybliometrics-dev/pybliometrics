pybliometrics
=============

Access Elsevier Scopus's API from Python on a large scale.

Documentation: https://pybliometrics.readthedocs.io

Development: https://github.com/pybliometrics-dev/pybliometrics

.. image:: https://badge.fury.io/py/pybliometrics.svg
    :target: https://badge.fury.io/py/pybliometrics

.. image:: https://img.shields.io/pypi/pyversions/pybliometrics.svg
    :target: https://img.shields.io/pypi/pyversions/pybliometrics.svg

.. image:: https://readthedocs.org/projects/pybliometrics/badge/?version=stable
    :target: https://readthedocs.org/projects/pybliometrics/badge/?version=stable

.. image:: https://img.shields.io/pypi/dm/pybliometrics.svg
    :target: https://img.shields.io/pypi/dm/pybliometrics.svg

.. image:: https://img.shields.io/pypi/l/pybliometrics.svg
    :target: https://img.shields.io/pypi/l/pybliometrics.svg

.. image:: https://api.codeclimate.com/v1/badges/a4d7edd206a1252dfcfe/maintainability
   :target: https://codeclimate.com/github/pybliometrics-dev/pybliometrics/maintainability

Example
=======
.. example-begin
.. code:: python

    >>> # Document-specific information
    >>> from pybliometrics.scopus import AbstractRetrieval
    >>> ab = AbstractRetrieval("10.1016/j.softx.2019.100263")
    >>> ab.title
    'pybliometrics: Scriptable bibliometrics using a Python interface to Scopus'
    >>> ab.publicationName
    'SoftwareX'
    >>> ab.authors
    [Author(auid='57209617104', indexed_name='Rose M.E.', surname='Rose', given_name='Michael E.', affiliation=['60105007']),
    Author(auid='7004212771', indexed_name='Kitchin J.R.', surname='Kitchin', given_name='John R.', affiliation=['60027950'])]
    >>> # Author-specific information
    >>> from pybliometrics.scopus import AuthorRetrieval
    >>> au2 = AuthorRetrieval(ab.authors[1].auid)
    >>> au2.h_index
    '30'
    >>> au1 = AuthorRetrieval(ab.authors[0].auid)
    >>> au1.affiliation_current
    '60105007'
    >>> # Affiliation information
    >>> from pybliometrics.scopus import ContentAffiliationRetrieval
    >>> aff1 = ContentAffiliationRetrieval(au1.affiliation_current)
    >>> aff1.affiliation_name
    'Max Planck Institute for Innovation and Competition'

.. example-end

Installation
============

.. installation-begin

Install the stable version from PyPI:

.. code-block:: bash

    pip install pybliometrics

or the development version from the GitHub repository (requires git on your system):

.. code-block:: bash

    pip install git+git://github.com/pybliometrics-dev/pybliometrics

.. installation-end

Citation
========

If pybliometrics helped you getting data for research, please cite our corresponding paper:

* Rose, Michael E. and John R. Kitchin: "`pybliometrics: Scriptable bibliometrics using a Python interface to Scopus <./meta/1-s2.0-S2352711019300573-main.pdf>`_", SoftwareX 10 (2019) 100263.

Citing the paper helps the development of pybliometrics, because it justifies funneling resources into the development.  It also signals that you obtained data from Scopus in a transparent and replicable way.

Change log
==========

Please see `CHANGES.rst <./meta/CHANGES.rst>`_.

Contributing
============

Please see `CONTRIBUTING.rst <CONTRIBUTING.rst>`_. For a list of contributors see
`AUTHORS.rst <./meta/AUTHORS.rst>`_.

License
=======

MIT License; see `LICENSE <LICENSE>`_.
