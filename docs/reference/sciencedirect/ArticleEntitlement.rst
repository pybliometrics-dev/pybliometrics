pybliometrics.sciencedirect.ArticleEntitlement
==============================================

`ArticleEntitlement()` implements the `ScienceDirect Article Entitlement API <https://dev.elsevier.com/documentation/ArticleEntitlementAPI.wadl>`_.

The Article Entitlement API allows you to check whether you have access to a specific document. Further, it let's you retrieve the identifiers of a document like the EID, DOI, PII, Scopus ID and Pubmed ID. The 'FULL' view is the default and only view available.

.. currentmodule:: pybliometrics.sciencedirect
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: ArticleEntitlement
    :members:
    :inherited-members:

Examples
--------
You initialize the class with an ID that ScienceDirect uses, e.g. the DOI:

.. code-block:: python

    >>> from pybliometrics.sciencedirect import ArticleEntitlement, init
    >>> init()
    >>> ae = ArticleEntitlement('10.1016/j.reseneeco.2015.06.001')

To check whether a document exists and whether you have access to it, you can use the `status` and `entitled` properties.

.. code-block:: python

    >>> ae.status
    'found'
    >>> ae.entitled
    True

In addition to the entitlement status, `ArticleEntitlement` contains information about the document's identifiers:

.. code-block:: python

    >>> ae.eid
    '1-s2.0-S092876551500038X'
    >>> ae.doi
    '10.1016/j.reseneeco.2015.06.001'
    >>> ae.pii
    'S0928-7655(15)00038-X'
    >>> ae.pii_norm
    'S092876551500038X'
    >>> ae.scopus_id
    '84935028440'
    >>> ae.pubmed_id
    None