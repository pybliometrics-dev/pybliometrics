Scopus Author
-------------

:doc:`ScopusAuthor <../reference/scopus.ScopusAuthor>` implements the `Author Retrieval API <https://api.elsevier.com/documentation/AuthorRetrievalAPI.wadl>`_.

This class is to interact with the entire author record in Scopus, using the author's Scopus ID (which can be passed as either an integer or a string):

.. code-block:: python
   
    >>> from scopus import ScopusAuthor
    >>> au = ScopusAuthor(7004212771)


The object can access many bits of data about an author, including the number of papers, h-index, current affiliation, etc.:

.. code-block:: python

    >>> au.name
    'John R. Kitchin'
    >>> au.ndocuments
    88
    >>> au.ncitations
    5068
    >>> au.hindex
    21
    >>> au.orcid
    '0000-0003-2625-9232'
    >>> au.current_affiliation
    'Carnegie Mellon University, Department of Chemical Engineering'


You can access the affiliation history as a list of `ScopusAffiliation <../reference/scopus.ScopusAffiliation>`_ objects:

.. code-block:: python

    >>> au.affiliation_history
    [<scopus.scopus_affiliation.ScopusAffiliation object at 0x7ff0ed28fda0>, <scopus.scopus_affiliation.ScopusAffiliation object at 0x7ff0ed29d128>, <scopus.scopus_affiliation.ScopusAffiliation object at 0x7ff0ed2a9cf8>, <scopus.scopus_affiliation.ScopusAffiliation object at 0x7ff0ed2a9ef0>, <scopus.scopus_affiliation.ScopusAffiliation object at 0x7ff0ed2a9fd0>]
    >>> for aff in au.affiliation_history:
    ...     print(aff.name)
    ... 
    National Energy Technology Laboratory, Morgantown
    TECH Lab
    National Energy Technology Laboratory, Pittsburgh
    United States Department of Energy
    Fritz Haber Institute of the Max Planck Society


There are a number of getter methods to obtain the co-authors (as ScopusAuthor objects), the written documents (as `ScopusAbstract <../reference/scopus.ScopusAbstract>`_ objects) and the number of publications per year (using `ScopusSearch <../reference/scopus.ScopusSearch>`_ and returning a `collections.Counter <https://docs.python.org/2/library/collections.html#collections.Counter>`_ object):

.. code-block:: python

    >>> coauthors = au.get_coauthors()
    >>> print([a.name for a in coauthors])
    ['Jens Kehlet Nørskov', 'Bruce C. Gates', 'Matthias Scheffler', 'Dionisios G. Vlachos', 'R. J. Gorte', 'Theodore E. Madey', 'Inkyu Song', 'Israel E. Wachs', 'David S. Sholl', 'Marc T M Koper', 'Christopher W. Jones', 'Jingguang Chen', 'Ulrich Stimming', 'Anatoly I. Frenkel', 'Mark A. Barteau', 'Andrew J. Gellman', 'William D. Jones', 'Karsten Reuter', 'Morris Morris Bullock', 'Hannes Jónsson', 'Terrence J. Collins', 'Henry W. Pennline', 'Jan Rossmeisl', 'Edward S. Rubin', 'Thomas Francisco Jaramillo', 'Susannah Scott', 'Paul A. Salvador', 'E. Charles H Sykes', 'David R. Luebke', 'David C M Miller', 'Thomas Bligaard', 'Evan Jacob Granite', 'John R. Kitchin', 'Newell R. Washburn', 'Bryan D. Morreale', 'Krishnan V. Damodaran', 'Venkatasubramanian K. Viswanathan', 'Lars Lindqvist', 'José Ignacio Martínez', 'Lisa Mauck Weiland', 'Kirk R. Gerdes', 'James B. Miller', 'Federico Calle-Vallejo', 'Mc Mahan L Gray', 'Edward M. Sabolsky', 'Heine Anton Hansen', 'Ashish B. Mhadeshwar', 'Jeongwoo Han', 'John A. Keith', 'Shelley Lynn Anna', 'Ashleigh E. Baber', 'Boris V. Yakshinskiy', 'Hunaid B. Nulwala', 'Nicholas S. Siefert', 'Wei Shi', 'James Landon', 'Jingguang G. Chen', 'Victor A. Kusuma', 'Vladimir V. Pushkarev', 'Heather L. Tierney', 'Christina R. Myers', 'Relja Vasić', 'Haiyan Su', 'David P. Hopkinson', 'Áshildur Logadóttir', 'Robert L. Thompson', 'Kevin P. Resnik', 'Adefemi A. Egbebi', 'John C. Eslick', 'Erik J. Albenze', 'Isabelacostinela Man', 'Yogesh V. Joshi', 'Neetha A. Khan', 'Hari Chandan Mantripragada', 'B. A. Calfa', 'Sneha A. Akhade', 'Nilay G. Inoǧlu', 'Stanislav V. Pandelov', 'Christopher J. Keturakis', 'Carmeline J. Dsilva', 'Jacob R. Boes', 'John R. McCormick', 'Peter L. Versteeg', 'Spencer D. Miller', 'Fei Gao', 'Petro Kondratyuk', 'Zhongnan Xu', 'Gamze Gumuslu', 'W. Richard Alesi', 'James X. Mao', 'Anita S. Lee', 'Paul A. Salvador', 'Matthew T. Curnan', 'Peter Kondratyuk', 'John D. Watkins', 'Ratiporn Munprom', 'Mitchell C. Groenenboom', 'Rumyana V. Petrova', 'Ethan L. Demeter', 'Bruno A. Calfa', 'Charles T. Campbell', 'Chunrong Yin', 'Alexander P. Hallenbeck', 'Robin Chao', 'Charles H. Sykes', 'Shayna L. Hilburg', 'Sumathy Raman', 'Prateek Mehta', 'Xu Zhou', 'Nilay Inolu', 'Walter Richard Alesi', 'Qingqi Fan', 'Hari Thirumalai', 'Steven M. Illes', 'Aaron Marks', 'John D. Michael', 'Siddharth Deshpande', 'Feiyang Geng']
    >>> print(au.get_document_eids(refresh=False))
    ['2-s2.0-85011269759', '2-s2.0-85012247151', '2-s2.0-85011665513', '2-s2.0-84971324241', '2-s2.0-84981347698', '2-s2.0-84963677251', '2-s2.0-84979493765', '2-s2.0-84951310415', '2-s2.0-84977837443', '2-s2.0-84930349644', '2-s2.0-84963599520', '2-s2.0-84947220242', '2-s2.0-84947716900', '2-s2.0-84946065058', '2-s2.0-84941248260', '2-s2.0-84930616647', '2-s2.0-84930662492', '2-s2.0-84928975689', '2-s2.0-84924911828', '2-s2.0-84923164062', '2-s2.0-84924130725', '2-s2.0-84927589996', '2-s2.0-84946493176', '2-s2.0-84949115648', '2-s2.0-84901638552', '2-s2.0-84898934670', '2-s2.0-84896759135', '2-s2.0-84896380535', '2-s2.0-84896585411', '2-s2.0-84908637059', '2-s2.0-84880986072', '2-s2.0-84881394200', '2-s2.0-84873706643', '2-s2.0-84876703352', '2-s2.0-84886483703', '2-s2.0-84867809683', '2-s2.0-84864914806', '2-s2.0-84865730756', '2-s2.0-84864592302', '2-s2.0-84863684845', '2-s2.0-84866142469', '2-s2.0-84861127526', '2-s2.0-84857197729', '2-s2.0-84857224144', '2-s2.0-84856818654', '2-s2.0-80052944171', '2-s2.0-80051860134', '2-s2.0-80051809046', '2-s2.0-79953651013', '2-s2.0-79952860396', '2-s2.0-79951537083', '2-s2.0-77956568341', '2-s2.0-77954747189', '2-s2.0-77956693843', '2-s2.0-77955464573', '2-s2.0-77949916234', '2-s2.0-72049114200', '2-s2.0-78649504144', '2-s2.0-78649528829', '2-s2.0-77952266872', '2-s2.0-73149124752', '2-s2.0-73149109096', '2-s2.0-67449106405', '2-s2.0-63649114440', '2-s2.0-60849113132', '2-s2.0-58649114498', '2-s2.0-78049295221', '2-s2.0-79952292116', '2-s2.0-79952296916', '2-s2.0-79952301915', '2-s2.0-78049231913', '2-s2.0-45149129361', '2-s2.0-40949100780', '2-s2.0-37349101648', '2-s2.0-58049109348', '2-s2.0-33750804660', '2-s2.0-33645645065', '2-s2.0-20544467859', '2-s2.0-15744396507', '2-s2.0-9744261716', '2-s2.0-13444307808', '2-s2.0-3042820285', '2-s2.0-2942640180', '2-s2.0-0142023762', '2-s2.0-0141924604', '2-s2.0-0037368024', '2-s2.0-0037197884']
    >>> print(au.n_yearly_publications(refresh=False))
    Counter({2015: 12, 2016: 8, 2009: 7, 2012: 7, 2014: 7, 2010: 5, 2004: 4, 2011: 4, 2013: 4, 2017: 3, 2003: 3, 2005: 2, 2002: 1, 2006: 1, 2008: 1})
