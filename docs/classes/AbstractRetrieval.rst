pybliometrics.scopus.AbstractRetrieval
======================================

`AbstractRetrieval()` implements the `Scopus Abstract Retrieval API <https://dev.elsevier.com/documentation/AbstractRetrievalAPI.wadl>`_.

It takes any identifier as main argument: Most of the time it will be a `Scopus EID <http://kitchingroup.cheme.cmu.edu/blog/2015/06/07/Getting-a-Scopus-EID-from-a-DOI/>`_, but DOI, Scopus ID (the last part of the EID), PubMed identifier or Publisher Item Identifier (PII) work as well. `AbstractRetrieval` tries to infer the class itself - to speed this up you can tell the ID type via `ID_type`.

The Abstract Retrieval API allows a differing information depth via `views <https://dev.elsevier.com/guides/AbstractRetrievalViews.htm>`_, some of which are restricted.  The view 'META_ABS' is the highest unrestricted view and contains all information from other unrestricted views.  It is therefore the default view.  The view with the most information content is 'FULL', which includes all information available with 'META_ABS', but is restricted.  In generally you should always try to use `view='FULL'` when downloading an abstract and fall back to the default otherwise.

.. currentmodule:: pybliometrics.scopus
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: AbstractRetrieval
   :members:
   :inherited-members:

Examples
--------
You initialize the class with an ID that Scopus uses, e.g. the EID:

.. code-block:: python

    >>> from pybliometrics.scopus import AbstractRetrieval
    >>> ab = AbstractRetrieval("2-s2.0-85068268027", view='FULL')


You can obtain basic information just by printing the object:

.. code-block:: python

    >>> print(ab)
    Michael E. Rose and John R. Kitchin: "pybliometrics: Scriptable bibliometrics using a Python interface to Scopus", SoftwareX, 10, (no pages found)(2019). https://doi.org/10.1016/j.softx.2019.100263.
    34 citation(s) as of 2022-04-07
      Affiliation(s):
       Max Planck Institute for Innovation and Competition
       Carnegie Mellon University


There are 52 attributes and 8 methods to interact with.  For example, to obtain bibliographic information:

.. code-block:: python

    >>> ab.publicationName
    'SoftwareX'
    >>> ab.aggregationType
    'Journal'
    >>> ab.coverDate
    '2019-07-01'
    >>> ab.volume
    '10'
    >>> ab.issueIdentifier
    None
    >>> ab.pageRange
    None
    >>> ab.doi
    '10.1016/j.softx.2019.100263'
    >>> ab.openaccessFlag
    True


Attributes `idxterms`, `subject_areas` and `authkeywords` (if provided) provide an idea on the content of a document:

.. code-block:: python

    >>> ab.idxterms
    ['Bibliometrics', 'Python', 'Python interfaces', 'Reproducibilities',
     'Scientometrics', 'Scopus', 'Scopus database', 'User friendly interface']
    >>> ab.subject_areas
    [Area(area='Software', abbreviation='COMP', code=1712),
     Area(area='Computer Science Applications', abbreviation='COMP', code=1706)]
    >>> ab.authkeywords
    ['Bibliometrics', 'Python', 'Scientometrics', 'Scopus', 'Software']


To obtain the total citation count (at the time the abstract was retrieved and cached):

.. code-block:: python

    >>> ab.citedby_count
    34


You get the authors as a list of `namedtuples <https://docs.python.org/3/library/collections.html#collections.namedtuple>`_, which pair conveniently with `pandas <https://pandas.pydata.org/>`_:

.. code-block:: python

    >>> ab.authors
    [Author(auid=57209617104, indexed_name='Rose M.E.', surname='Rose',
            given_name='Michael E.', affiliation='60105007'),
     Author(auid=7004212771, indexed_name='Kitchin J.R.', surname='Kitchin',
            given_name='John R.', affiliation='60027950')]

    >>> import pandas as pd
    >>> print(pd.DataFrame(ab.authors))
              auid  indexed_name  surname  given_name affiliation
    0  57209617104     Rose M.E.     Rose  Michael E.  60105007
    1   7004212771  Kitchin J.R.  Kitchin     John R.  60027950


The same structure applies for the attributes `affiliation` and `authorgroup`:

.. code-block:: python

    >>> ab.affiliation
    [Affiliation(id=60105007, name='Max Planck Institute for Innovation and Competition',
                 city='Munich', country='Germany'),
     Affiliation(id=60027950, name='Carnegie Mellon University',
                 city='Pittsburgh', country='United States')]

    >>> ab.authorgroup
    [Author(affiliation_id=60105007, dptid=None,
            organization='Max Planck Institute for Innovation and Competition',
            city=None, postalcode=None, addresspart=None, country='Germany',
            collaboration=None, auid=57209617104, orcid=None,
            indexed_name='Rose M.E.', surname='Rose', given_name='Michael E.'),
     Author(affiliation_id=60027950, dptid=110785688,
            organization='Carnegie Mellon University, Department of Chemical Engineering',
            city=None, postalcode=None, addresspart=None, country='United States',
            collaboration=None, auid=7004212771, orcid=None,
            indexed_name='Kitchin J.R.', surname='Kitchin', given_name='John R.')]



Keep in mind that Scopus might not perfectly/correctly pair authors and affiliations as per the original document, even if it looks so on the web view.  In this case please request corrections to be made in Scopus' API here `here <https://service.elsevier.com/app/contact/supporthub/scopuscontent/>`_.

The references of an article (useful to build citation networks) are only
available if you downloaded the article with 'FULL' as `view` parameter.

.. code-block:: python

    >>> ab.refcount
    25
    >>> refs = ab.references
    >>> refs[0]
    Reference(position='1', id='38949137710', doi='10.1007/978-94-007-7618-0˙310',
              title='Comparison of PubMed, Scopus, Web of Science, and Google Scholar:
                     strengths and weaknesses',
              authors='Falagas, M.E.; Pitsouni, E.I.; Malietzis, G.A.; Pappas, G.',
              authors_auid=None, authors_affiliationid=None, sourcetitle='FASEB J',
              publicationyear='2007', coverDate=None, volume=None, issue=None,
              first=None, last=None, citedbycount=None, type=None,
              fulltext='Falagas, M.E., Pitsouni, E.I., Malietzis, G.A., Pappas, G.,
                        Comparison of PubMed, Scopus, Web of Science, and Google
                        Scholar: strengths and weaknesses. FASEB J 22:2 (2007),
                        338–342, 10.1007/978-94-007-7618-0˙310.')

    >>> df = pd.DataFrame(refs)
    >>> df.columns
    Index(['position', 'id', 'doi', 'title', 'authors', 'authors_auid',
           'authors_affiliationid', 'sourcetitle', 'publicationyear', 'coverDate',
           'volume', 'issue', 'first', 'last', 'citedbycount', 'type', 'fulltext'],
          dtype='object')
    >>> df['eid'] = '2-s2.0-' + df['id']
    >>> df['eid'].tolist()
    ['2-s2.0-38949137710', '2-s2.0-84956635108', '2-s2.0-84954384742',
     '2-s2.0-85054706190', '2-s2.0-84978682989', '2-s2.0-85047117387',
     '2-s2.0-85068267813', '2-s2.0-84959420483', '2-s2.0-85041892797',
     '2-s2.0-85019268211', '2-s2.0-85059309053', '2-s2.0-85033499871',
     nan, '2-s2.0-85068268189', '2-s2.0-84958069531', '2-s2.0-84964429621',
     '2-s2.0-84977619412', '2-s2.0-85068262994', nan, '2-s2.0-23744500479',
     '2-s2.0-70349549313', nan, '2-s2.0-85042855814', '2-s2.0-85068258349',
     '2-s2.0-84887264733']


Setting `view="REF"` accesses the REF view of the article, which provides more information on the referenced items (but less on other attributes of the document):

.. code-block:: python

    >>> ab_ref = AbstractRetrieval("2-s2.0-85068268027", view='REF')
    >>> ab_ref.references[0]
    Reference(position='1', id='38949137710', doi='10.1096/fj.07-9492LSF',
              title='Comparison of PubMed, Scopus, Web of Science, and Google Scholar:
                      Strengths and weaknesses',
               authors='Falagas, Matthew E.; Pitsouni, Eleni I.; Malietzis, George A.;
                        Falagas, Matthew E.; Pappas, Georgios',
               authors_auid='7003962139; 16240046300; 43761284000; 7003962139; 7102070422',
               authors_affiliationid='60033272; 60033272; 60033272; 60015849; 60081865',
               sourcetitle='FASEB Journal', publicationyear=None, coverDate='2008-02-01',
               volume='22', issue='2', first='338', last='342', citedbycount='1676',
               type='resolvedReference', fulltext=None)


The list of authors contains duplicate because of the 1:1 pairing with the authors' affiliation IDs.  In above example, 7003962139 is affiliated with 60033272 and with 60015849.  Authors are therefore grouped by affiliation ID.

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

    >>> ab_fund = AbstractRetrieval("2-s2.0-85053478849", view="FULL")
    >>> ab_fund.funding
    [Funding(agency=None, string='CNRT “Nickel et son Environnement',
     agency_id=None, funding_id=None, acronym=None, country=None)]
    >> ab_fund.funding_text
    'The authors gratefully acknowledge CNRT “Nickel et son Environnement” for
    providing the financial support. The results reported in this publication
    are gathered from the CNRT report “Ecomine BioTop”.'
    >>> ab_fund.chemicals
    [Chemical(source='esbd', chemical_name='calcium',
              cas_registry_number='7440-70-2;14092-94-5'),
     Chemical(source='esbd', chemical_name='magnesium',
              cas_registry_number='7439-95-4'),
     Chemical(source='nlm', chemical_name='Fertilizers', cas_registry_number=None),
     Chemical(source='nlm', chemical_name='Sewage', cas_registry_number=None),
     Chemical(source='nlm', chemical_name='Soil', cas_registry_number=None)]
    >>> ab_fund.sequencebank
    [Sequencebank(name='GENBANK', sequence_number='MH150839:MH150870', type='submitted')]


You can print the abstract in a variety of formats, including LaTeX, bibtex, HTML, and RIS. For bibtex entries, the key is the first author's surname, the year, and the first and last name of the title:

.. code-block:: python

    >>> print(ab.get_bibtex())
    @article{Rose2019Pybliometrics:Scopus,
      author = {Michael E. Rose and John R. Kitchin},
      title = {{pybliometrics: Scriptable bibliometrics using a Python interface to Scopus}},
      journal = {SoftwareX},
      year = {2019},
      volume = {10},
      number = {None},
      pages = {-},
      doi = {10.1016/j.softx.2019.100263}}
    >>> print(ab.get_ris())
    TY  - JOUR
    TI  - pybliometrics: Scriptable bibliometrics using a Python interface to Scopus
    JO  - SoftwareX
    VL  - 10
    DA  - 2019-07-01
    PY  - 2019
    SP  - None
    AU  - Rose M.E.
    AU  - Kitchin J.R.
    DO  - 10.1016/j.softx.2019.100263
    UR  - https://doi.org/10.1016/j.softx.2019.100263
    ER  -


Downloaded results are cached to speed up subsequent analysis.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to get the date of last modification, and `ab.get_cache_file_age()` the number of days since the last modification.
