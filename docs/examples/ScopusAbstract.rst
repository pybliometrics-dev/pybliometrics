Scopus Abstract
---------------

:doc:`ScopusAbstract <../reference/scopus.ScopusAbstract>` implements the `Abstract Retrieval API <https://api.elsevier.com/documentation/AbstractRetrievalAPI.wadl>`_.

It takes a `Scopus EID <http://kitchingroup.cheme.cmu.edu/blog/2015/06/07/Getting-a-Scopus-EID-from-a-DOI/>`_.  Retrieving these results is not fast, so we cache them to speed up subsequent uses of the code.  Sometimes you may want new results, e.g. to update citation counts, and then you set `refresh=True`.

You initalize the class with Scopus' Electronic Identifier (EID):

.. code-block:: python
   
    >>> from scopus import ScopusAbstract
    >>> ab = ScopusAbstract("2-s2.0-84930616647")

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(ab)
    [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward][2-s2.0-84930616647]]  John R. Kitchin, Examples of effective data sharing in scientific publishing, ACS Catalysis, 5(6), p. 3894-3899, (2015). https://doi.org/10.1021/acscatal.5b00538, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward, cited 4 times (Scopus).
      Affiliations:
       id:60027950 Carnegie Mellon University


You can print the abstract in a variety of formats, including LaTeX, bibtex, HTML, and RIS.For bibtex entries, you get a uuid for the key:

.. code-block:: python

    >>> print(ab.bibtex)
    @article{9b0ff2dc-1550-11e7-b54a-48d705e201bd,
      author = {John R. Kitchin},
      title = {Examples of effective data sharing in scientific publishing},
      journal = {ACS Catalysis},
      year = {2015},
      volume = {5},
      number = {6},
      pages = {3894-3899},
      doi = {10.1021/acscatal.5b00538}
    }
    >>> print(ab.ris)
    TY  - JOUR
    AU  - Kitchin J.R.
    TI  - Examples of effective data sharing in scientific publishing
    JO  - ACS Catalysis
    VL  - 5
    IS  - 6
    DA  - 2015-06-05
    SP  - 3894-3899
    PY  - 2015
    DO  - 10.1021/acscatal.5b00538
    UR  - https://doi.org/10.1021/acscatal.5b00538
    ER  - 


The object has a number of attributes to interact with.

For example, to obtain bibliographic information:

.. code-block:: python

    >>> ab.publicationName
    'ACS Catalysis'
    >>> ab.aggregationType
    'Journal'
    >>> ab.coverDate
    '2015-06-05'
    >>> ab.volume
    '5'
    >>> ab.issueIdentifier
    '6'
    >>> ab.pageRange
    '3894-3899'
    >>> ab.doi
    '10.1021/acscatal.5b00538'


To obtain the total citation count (at the time the abstract was retrieved and cached):

.. code-block:: python

    >>> ab.citedby_count
    4


You get the authors as a list:

.. code-block:: python

    >>> for au in ab.authors:
    ...     print(au)
    ...     print(au.auid)
    ...     for aff in au.affiliations:
    ...         print(aff.id)
    ... 
    1. John R. Kitchin scopusid:7004212771 affiliation_id:60027950
    7004212771


Finally to obtain information of all listed affiliations:

.. code-block:: python

    >>> for aff in ab.affiliations:
    ...     print(aff.affilname)
    ...     print(aff.id)
    ...     print(aff.city, aff.country)
    ...
    Carnegie Mellon University
    60027950
    Pittsburgh United States


The references of an article (useful to build citation networks) are only
available if you downloaded the article with 'FULL' as `view` parameter.
The standard view is 'META_ABS' which is the highest free view.

.. code-block:: python

    >>> ab = ScopusAbstract("2-s2.0-84930616647", view="FULL")
    >>> ab.references
    ['2-s2.0-84881394200', '2-s2.0-84896585411', '2-s2.0-84949115648',
    '2-s2.0-84908637059', '2-s2.0-84901638552', '2-s2.0-84896380535',
    '2-s2.0-84923164062', '2-s2.0-84923164062', '2-s2.0-84930667693',
    '2-s2.0-79952591087', '2-s2.0-84923165709', '2-s2.0-0036572216',
    '2-s2.0-84924117832', '2-s2.0-84930624433', '2-s2.0-79955561198',
    '2-s2.0-84930642229', '2-s2.0-0010630518', '2-s2.0-84861337169',
    '2-s2.0-34247481878', '2-s2.0-79958260504', '2-s2.0-58149108944',
    '2-s2.0-84917679308']
