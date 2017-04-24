Scopus Affiliation
------------------

:doc:`ScopusAffiliation <../reference/scopus.ScopusAffiliation>` implements the `Content Affiliation Retrieval API <https://api.elsevier.com/documentation/AffiliationRetrievalAPI.wadl>`_. It provides basic information on registered affiliations, like city, country, its members, and more.

You initialize the class with Scopus' Affiliation ID:

.. code-block:: python
   
    >>> from scopus import ScopusAffiliation
    >>> aff = ScopusAffiliation("60000356")


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(aff)
    University of Cape Town (10200 authors, 42003 documents)
        Private Bag X3
        Cape Town, South Africa
        https://www.scopus.com/affil/profile.uri?afid=60000356&partnerID=HzOxMe3b&origin=inward


The object has a number of attributes but no methods:

.. code-block:: python

    >>> aff.name
    'University of Cape Town'
    >>> aff.country
    'South Africa'
    >>> aff.nauthors
    '10200'
    >>> aff.ndocuments
    '42003'
