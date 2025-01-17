pybliometrics.scival.PublicationLookup
======================================

`PublicationLookup()` implements the `Scival Publication Lookup API <https://dev.elsevier.com/documentation/SciValPublicationAPI.wadl>`_.

It accepts any identifier as the main argument which is Scopus ID (the last part of the EID).

.. currentmodule:: pybliometrics.scival
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: PublicationLookup
   :members:
   :inherited-members:

Examples
--------
You initialize the class with an ID that Scopus uses, e.g. the ID:

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scival import PublicationLookup
    >>> pybliometrics.scival.init()
    >>> pub = PublicationLookup(85036568406)


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(pub)
    - ID: 85036568406
    - Title: Soft Electrochemical Probes for Mapping the Distribution of Biomarkers and Injected Nanomaterials in Animal and Human Tissues
    - DOI: 10.1002/anie.201709271
    - Type: Article
    - Year: 2017
    - Citation Count: 34
    - Source Title: Angewandte Chemie - International Edition
    - Topic ID: 7563
    - Topic Cluster ID: 157
    - Link: https://api.elsevier.com/analytics/scival/publication/85036568406?view=&apiKey=bea5cd32b1ad6cf822f6dea4e6dd7413&httpAccept=application/json&insttoken=b6fdf867f748e53962ff8ff8b9a18ded
    - Authors: Lin, T.-E., Lu, Y.-J., Sun, C.-L., Pick, H., Chen, J.-P., Lesch, A., Girault, H.H.
    - Institutions: Chang Gung University, Swiss Federal Institute of Technology Lausanne, Chang Gung Memorial Hospital
    - SDGs: SDG 3: Good Health and Well-being


You can access different attributes of the publication

.. code-block:: python

    >>> pub.id
    '85036568406'
    >>> pub.type
    'Article'
    >>> pub.title
    'Soft Electrochemical Probes for Mapping the Distribution of Biomarkers and Injected Nanomaterials in Animal and Human Tissues'
    >>> pub.doi
    '10.1002/anie.201709271'
    >>> pub.publication_year
    2017
    >>> pub.citation_count
    34
    >>> pub.source_title
    'Angewandte Chemie - International Edition'


The attributes `authors`, `institutions` and `sdgs` offer insights into the document's content:

.. code-block:: python

    >>> pub.authors
    [Author(id=7404861905, name='Lin, T.-E.', link='https://api.elsevier.com/analytics/scival/author/7404861905'),
    Author(id=24537666700, name='Lu, Y.-J.', link='https://api.elsevier.com/analytics/scival/author/24537666700'),
    Author(id=7404248170, name='Sun, C.-L.', link='https://api.elsevier.com/analytics/scival/author/7404248170'),
    Author(id=7004202515, name='Pick, H.', link='https://api.elsevier.com/analytics/scival/author/7004202515'),
    Author(id=58307174900, name='Chen, J.-P.', link='https://api.elsevier.com/analytics/scival/author/58307174900'),
    Author(id=36246291500, name='Lesch, A.', link='https://api.elsevier.com/analytics/scival/author/36246291500'),
    Author(id=7102360867, name='Girault, H.H.', link='https://api.elsevier.com/analytics/scival/author/7102360867')]

    >>> pub.institutions
    [Institution(id=217002, name='Chang Gung University', country='Taiwan', country_code='TWN', link='https://api.elsevier.com/analytics/scival/institution/217002'),
    Institution(id=306002, name='Swiss Federal Institute of Technology Lausanne', country='Switzerland', country_code='CHE', link='https://api.elsevier.com/analytics/scival/institution/306002'), Institution(id=725104, name='Chang Gung Memorial Hospital', country='Taiwan', country_code='TWN', link='https://api.elsevier.com/analytics/scival/institution/725104')]

    >>> pub.sdgs
    ['SDG 3: Good Health and Well-being']


Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.