pybliometrics.scival.PublicationLookup
======================================

`PublicationLookup()` implements the `SciVal Publication Lookup API <https://dev.elsevier.com/documentation/SciValPublicationAPI.wadl>`_.

It accepts a Scopus ID as the main argument.

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

You initialize the class with the Scopus ID. The argument can be an integer or a string.

.. code-block:: python

    >>> import pybliometrics
    >>> from pybliometrics.scival import PublicationLookup
    >>> pybliometrics.scival.init()
    >>> pub = PublicationLookup('85036568406')

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(pub)
    Document with Scopus Id 85036568406 received:
    - Title: Soft Electrochemical Probes for Mapping the Distribution of Biomarkers and Injected Nanomaterials in Animal and Human Tissues
    - DOI: 10.1002/anie.201709271
    - Type: Article
    - Publication Year: 2017
    - 7 author(s) found
    - 3 institution(s) found

There are many attributes available in the response from the API. It is possible to explore the properties as in the following example:

.. code-block:: python

    >>> pub.id
    85036568406
    >>> pub.title
    'Soft Electrochemical Probes for Mapping the Distribution of Biomarkers and Injected Nanomaterials in Animal and Human Tissues'
    >>> pub.doi
    '10.1002/anie.201709271'
    >>> pub.publication_year
    2017
    >>> pub.type
    'Article'
    >>> pub.citation_count
    34
    >>> pub.source_title
    'Angewandte Chemie - International Edition'
    >>> pub.topic_id
    7563
    >>> pub.topic_cluster_id
    157
    >>> pub.sdgs
    ['SDG 3: Good Health and Well-being']

You can retrieve the authors as a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_, which pair conveniently with `pandas <https://pandas.pydata.org/>`_:

.. code-block:: python

    >>> pub.authors
    [Author(id=7404861905, name='Lin, T.-E.', uri='Author/7404861905'),
     Author(id=24537666700, name='Lu, Y.-J.', uri='Author/24537666700'),
     Author(id=7404248170, name='Sun, C.-L.', uri='Author/7404248170'),
     Author(id=7004202515, name='Pick, H.', uri='Author/7004202515'),
     Author(id=58307174900, name='Chen, J.-P.', uri='Author/58307174900'),
     Author(id=36246291500, name='Lesch, A.', uri='Author/36246291500'),
     Author(id=7102360867, name='Girault, H.H.', uri='Author/7102360867')]

    >>> import pandas as pd
    >>> print(pd.DataFrame(pub.authors))
                id           name                 uri
    0   7404861905     Lin, T.-E.   Author/7404861905
    1  24537666700      Lu, Y.-J.  Author/24537666700
    2   7404248170     Sun, C.-L.   Author/7404248170
    3   7004202515       Pick, H.   Author/7004202515
    4  58307174900    Chen, J.-P.  Author/58307174900
    5  36246291500      Lesch, A.  Author/36246291500
    6   7102360867  Girault, H.H.   Author/7102360867

The same structure applies for the attribute `institutions`:

.. code-block:: python

    >>> pub.institutions
    [Institution(id=217002, name='Chang Gung University', country='Taiwan', country_code='TWN'),
     Institution(id=306002, name='Swiss Federal Institute of Technology Lausanne', country='Switzerland', country_code='CHE'),
     Institution(id=725104, name='Chang Gung Memorial Hospital', country='Taiwan', country_code='TWN')]

    >>> import pandas as pd
    >>> print(pd.DataFrame(pub.institutions))
           id                                            name      country country_code
    0  217002                           Chang Gung University       Taiwan          TWN
    1  306002  Swiss Federal Institute of Technology Lausanne  Switzerland          CHE
    2  725104                    Chang Gung Memorial Hospital       Taiwan          TWN

Downloaded results are cached to expedite subsequent analyses. This information may become outdated. To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as the maximum allowed number of days since the last modification date. For example, if you want to refresh all cached results older than 100 days, set `refresh=100`. Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.
