Abstract Retrieval
------------------

:doc:`AbstractRetrieval <../reference/scopus.AbstractRetrieval>` implements the `Abstract Retrieval API <https://api.elsevier.com/documentation/AbstractRetrievalAPI.wadl>`_.

It takes any identifier as main arguemnt: Most of the time it will be a `Scopus EID <http://kitchingroup.cheme.cmu.edu/blog/2015/06/07/Getting-a-Scopus-EID-from-a-DOI/>`_ but DOI, Scopus ID (the last part of the EID), PubMed identifier or Publisher Item Identifier (PII) work as well. `AbstractRetrieval` tries to infer the class itself - to speed this up you can tell the ID type via `ID_type`.  Retrieving these results is not fast, so we cache them to speed up subsequent uses of the code.  Sometimes you may want new results, e.g. to update citation counts, and then you set `refresh=True`.

The Scopus API allows a differing information depth via
`views <https://dev.elsevier.com/guides/AbstractRetrievalViews.htm>`_, some of which
are restricted.  The view 'META_ABS' is the highest unrestricted view and contains all information from other unrestricted views.  It is therefore the default view.  The view
with the most information content is 'FULL', which includes all information available with
'META_ABS', but is restricted.  In generally you should always try to use `view='FULL'`
when downloading an abstract and fall back to the default otherwise.  Note that
the view parameter does not take effect for cached files, i.e. to switch to another
view set `refresh=True` as well.

You initalize the class with an ID that Scopus uses, e.g. the EID:

.. code-block:: python
   
    >>> from scopus import AbstractRetrieval
    >>> ab = AbstractRetrieval("2-s2.0-84930616647", view='FULL', refresh=True)

You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(ab)
    [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward][2-s2.0-84930616647]]  John R. Kitchin, Examples of effective data sharing in scientific publishing, ACS Catalysis, 5(6), pp. 3894-3899, (2015). https://doi.org/10.1021/acscatal.5b00538, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward, cited 7 times (Scopus).
      Affiliations:
       Carnegie Mellon University


There are 48 attributes and 4 methods to interact with.  For example, to obtain bibliographic information:

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


Attributes `idxterms`, `subject_areas` and `authkeywords` (if provided) provide an idea on the content of a document:

.. code-block:: python

    >>> ab.idxterms
    ['Authoring tool', 'Data generation', 'Data Sharing', 'Human-readable',
    'Scientific publications', 'Traditional publishing']
    >>> ab.subject_areas
    [Area(area='Catalysis', abbreviation='CENG', code='1503')]
    >>> ab.authkeywords
    >>>


To obtain the total citation count (at the time the abstract was retrieved and cached):

.. code-block:: python

    >>> ab.citedby_count
    7


You get the authors as a list of `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_, which pair conveniently with `pandas <https://pandas.pydata.org/>`_:

.. code-block:: python

    >>> ab.authors
    [Author(auid='7004212771', indexed_name='Kitchin J.R.', surname='Kitchin',
    given_name='John R.', affiliation=['60027950'])]
    >>> import pandas as pd
    >>> print(pd.DataFrame(ab.authors))
        auid  indexed_name  surname given_name affiliation
     0  7004212771  Kitchin J.R.  Kitchin    John R.  [60027950]


The same structure applies for the attributes `affiliation` and `authorgroup`:

.. code-block:: python

    >>> ab.affiliation
    [Affiliation(id='60027950', name='Carnegie Mellon University',
    city='Pittsburgh', country='United States')]
    >>> ab.authorgroup
    [Author(affiliation_id='60027950', dptid='110785688',
    organization='Department of Chemical Engineering, Carnegie Mellon University',
    city='Pittsburgh', postalcode='15213', addresspart='5000 Forbes Avenue',
    country='United States', auid='7004212771', indexed_name='Kitchin J.',
    surname='Kitchin', given_name='John R.')]


Keep in mind that Scopus might not perfectly/correctly pair authors and affiliations as per the original document, even if it looks so on the web view.  In this case please request corrections to be made in Scopus' API here `here <https://service.elsevier.com/app/contact/supporthub/scopuscontent/>`_.

The references of an article (useful to build citation networks) are only
available if you downloaded the article with 'FULL' as `view` parameter.

.. code-block:: python

    >>> ab.ref_count
    '22'
    >>> refs = ab.references
    >>> len(refs)
    22
    >>> refs[0]
    Reference(position='1', id='84881394200', doi=None, title=None,
    authors='Hallenbeck, A.P.; Kitchin, J.R.', sourcetitle='Ind. Eng. Chem. Res.',
    publicationyear='2013', volume='52', issue=None, first='10788', last='10794',
    text=None, fulltext='Hallenbeck, A. P.; Kitchin, J. R. Ind. Eng. Chem. Res. 2013, 52, 10788-10794 10.1021/ie400582a', citedbycount=None, authors_auid=[], authors_affiliationid=[])
    >>> df = pd.DataFrame(refs)
    >>> df.columns
    Index(['position', 'id', 'doi', 'title', 'authors', 'authors_auid',
           'authors_affiliationid', 'sourcetitle', 'publicationyear', 'volume',
           'issue', 'first', 'last', 'citedbycount', 'text', 'fulltext'],
          dtype='object')
    >>> df['eid'] = '2-s2.0-' + df['id']
    >>> list(df['eid'])
    ['2-s2.0-84881394200', '2-s2.0-84896585411', '2-s2.0-84949115648', '2-s2.0-84908637059', '2-s2.0-84901638552', '2-s2.0-84896380535', '2-s2.0-84923164062', '2-s2.0-84923164062', '2-s2.0-84930667693', '2-s2.0-79952591087', '2-s2.0-84923165709', '2-s2.0-0036572216', '2-s2.0-84924117832', '2-s2.0-84930624433', '2-s2.0-79955561198', '2-s2.0-84930642229', '2-s2.0-0010630518', '2-s2.0-84861337169', '2-s2.0-34247481878', '2-s2.0-79958260504', '2-s2.0-58149108944', '2-s2.0-84917679308']

Setting `view="REF"` accesses the REF view of the article, which provides more information on the referenced items (but less on other attributes of the document):

.. code-block:: python

    >>> ab = AbstractRetrieval("2-s2.0-84930616647", view='REF', refresh=True)
    >>> ab.references[0]
    Reference(position='1', id='84881394200', doi='10.1021/ie400582a',
    title='Effects of O2 and SO2 on the capture capacity of a primary-amine
    based polymeric CO2 sorbent', authors='Hallenbeck, Alexander P.; Kitchin, John R.;
    Hallenbeck, Alexander P.; Kitchin, John R.', authors_auid=['55569145100', '7004212771',
    '55569145100', '7004212771'], authors_affiliationid=['60090776', '60090776',
    '60027950', '60027950'], sourcetitle='Industrial and Engineering Chemistry Research',
    publicationyear=None, volume='52', issue='31', first='10788', last='10794',
    citedbycount='28', text=None, fulltext=None)

For conference proceedings, Scopus also collects information on the conference:

.. code-block:: python

    >>> cp = AbstractRetrieval("2-s2.0-0029486824", view="FULL")
    >>> cp.confname
    'Proceedings of the 1995 34th IEEE Conference on Decision and Control. Part 1 (of 4)'
    >>> cp.confcode
    '44367'
    >>> cp.confdate
    ((1995, 12, 13), (1995, 12, 15))
    >>> cp.conflocation
    'New Orleans, LA, USA'
    >>> cp.confsponsor
    'IEEE'


Some articles have information on funding, chemicals and genome banks:

.. code-block:: python

    >>> fund = AbstractRetrieval("2-s2.0-85053478849", view="FULL")
    >>> fund.funding
    [Funding(agency=None, string='CNRT “Nickel et son Environnement', id=None, acronym=None, country=None)]
    >> fund.funding_text
    'The authors gratefully acknowledge CNRT “Nickel et son Environnement” for
    providing the financial support. The results reported in this publication
    are gathered from the CNRT report “Ecomine BioTop”. Appendix A'
    >>> fund.chemicals
    [Chemical(source='esbd', chemical_name='calcium', cas_registry_number='7440-70-2;14092-94-5'),
    Chemical(source='esbd', chemical_name='magnesium', cas_registry_number='7439-95-4')]
    >>> fund.sequencebank
    [Sequencebank(name='GENBANK', sequence_number='MH150839:MH150870',
    type='submitted')]


You can print the abstract in a variety of formats, including LaTeX, bibtex, HTML, and RIS. For bibtex entries, the key is the first author's surname, the year, and the first and last name of the title:

.. code-block:: python

    >>> print(ab.get_bibtex())
    @article{Kitchin2015ExamplesPublishing,
      author = {John R. Kitchin},
      title = {{Examples of effective data sharing in scientific publishing}},
      journal = {ACS Catalysis},
      year = {2015},
      volume = {5},
      number = {6},
      pages = {3894-3899},
      doi = {10.1021/acscatal.5b00538}}
    >>> print(ab.get_ris())
    TY  - JOUR
    TI  - Examples of effective data sharing in scientific publishing
    JO  - ACS Catalysis
    VL  - 5
    DA  - 2015-06-05
    PY  - 2015
    SP  - 3894-3899
    AU  - Kitchin J.R.
    DO  - 10.1021/acscatal.5b00538
    UR  - https://doi.org/10.1021/acscatal.5b00538
    IS  - 6
    ER  - 


