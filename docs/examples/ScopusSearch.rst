Scopus Search
-------------

:doc:`ScopusSearch <../reference/scopus.ScopusSearch>` implements the `Scopus Search API <https://api.elsevier.com/documentation/SCOPUSSearchAPI.wadl>`_. It performs a query and then retrieves the records of the query for analysis.

The class is initialized with a search query on which you read about in `Scopus Author Search Tips <https://api.elsevier.com/documentation/search/AUTHORSearchTips.htm>`_ (an invalid search query will result in an error).

.. code-block:: python
   
    >>> from scopus import ScopusSearch
    >>> s = ScopusSearch('FIRSTAUTH ( kitchin  j.r. )', refresh=True)


Currently class mostly serves to provide a list of EIDs which you can use for the `ScopusAbstract <../reference/scopus.ScopusAbstract>`_ class:

.. code-block:: python

    >>> s.EIDS
    ['2-s2.0-84971324241', '2-s2.0-84930349644', '2-s2.0-84930616647', '2-s2.0-67449106405', '2-s2.0-40949100780', '2-s2.0-37349101648', '2-s2.0-20544467859', '2-s2.0-13444307808', '2-s2.0-2942640180', '2-s2.0-0141924604', '2-s2.0-0037368024']


You can print an entire summary of search results:

.. code-block:: python

    >>> print(s.org_summary)
    1. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84971324241&origin=inward][2-s2.0-84971324241]]  J.R. Kitchin and A.J. Gellman, High-throughput methods using composition and structure spread libraries, AIChE Journal, 62(11), p. 3826-3835, (2016). http://dx.doi.org/10.1002/aic.15294, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84971324241&origin=inward, cited 1 times (Scopus).
      Affiliations:
       id:60027950 Carnegie Mellon University
    2. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930349644&origin=inward][2-s2.0-84930349644]]  John R. Kitchin, Data sharing in Surface Science, Surface Science, 647, p. 103-107, (2016). http://dx.doi.org/10.1016/j.susc.2015.05.007, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930349644&origin=inward, cited 0 times (Scopus).
      Affiliations:
       id:60027950 Carnegie Mellon University
    3. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward][2-s2.0-84930616647]]  John R. Kitchin, Examples of effective data sharing in scientific publishing, ACS Catalysis, 5(6), p. 3894-3899, (2015). http://dx.doi.org/10.1021/acscatal.5b00538, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward, cited 4 times (Scopus).
      Affiliations:
       id:60027950 Carnegie Mellon University
    4. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=67449106405&origin=inward][2-s2.0-67449106405]]  John R. Kitchin, Correlations in coverage-dependent atomic adsorption energies on Pd(111), Physical Review B - Condensed Matter and Materials Physics, 79(20), Art. No. 205412 (2009). http://dx.doi.org/10.1103/PhysRevB.79.205412, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=67449106405&origin=inward, cited 40 times (Scopus).
      Affiliations:
       id:60027950 Carnegie Mellon University
    5. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=40949100780&origin=inward][2-s2.0-40949100780]]  J.R. Kitchin, K. Reuter and M. Scheffler, Alloy surface segregation in reactive environments: First-principles atomistic thermodynamics study of Ag3 Pd(111) in oxygen atmospheres, Physical Review B - Condensed Matter and Materials Physics, 77(7), Art. No. 075437 (2008). http://dx.doi.org/10.1103/PhysRevB.77.075437, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=40949100780&origin=inward, cited 70 times (Scopus).
      Affiliations:
       id:60008644 Fritz Haber Institute of the Max Planck Society
       id:60027950 Carnegie Mellon University
    7. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=20544467859&origin=inward][2-s2.0-20544467859]]  J.R. Kitchin, J.K. Nørskov, M.A. Barteau and J.G. Chen, Trends in the chemical properties of early transition metal carbide surfaces: A density functional study, Catalysis Today, 105(1 SPEC. ISS.), p. 66-73, (2005). http://dx.doi.org/10.1016/j.cattod.2005.04.008, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=20544467859&origin=inward, cited 95 times (Scopus).
      Affiliations:
       id:60011373 Danmarks Tekniske Universitet
       id:60023004 University of Delaware
    8. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=13444307808&origin=inward][2-s2.0-13444307808]]  J.R. Kitchin, J.K. Nørskov, M.A. Barteau and J.G. Chen, Role of strain and ligand effects in the modification of the electronic and chemical Properties of bimetallic surfaces, Physical Review Letters, 93(15), (no pages found) (2004). http://dx.doi.org/10.1103/PhysRevLett.93.156801, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=13444307808&origin=inward, cited 501 times (Scopus).
      Affiliations:
       id:60011373 Danmarks Tekniske Universitet
       id:60023004 University of Delaware
    9. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=2942640180&origin=inward][2-s2.0-2942640180]]  J.R. Kitchin, J.K. Nørskov, M.A. Barteau and J.G. Chen, Modification of the surface electronic and chemical properties of Pt(111) by subsurface 3d transition metals, Journal of Chemical Physics, 120(21), p. 10240-10246, (2004). http://dx.doi.org/10.1063/1.1737365, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=2942640180&origin=inward, cited 588 times (Scopus).
      Affiliations:
       id:60011373 Danmarks Tekniske Universitet
       id:60023004 University of Delaware
    10. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0141924604&origin=inward][2-s2.0-0141924604]]  J.R. Kitchin, N.A. Khan, M.A. Barteau, J.G. Chen, B. Yakshinskiy and T.E. Madey, Elucidation of the active surface and origin of the weak metal-hydrogen bond on Ni/Pt(1 1 1) bimetallic surfaces: A surface science and density functional theory study, Surface Science, 544(2-3), p. 295-308, (2003). http://dx.doi.org/10.1016/j.susc.2003.09.007, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0141924604&origin=inward, cited 118 times (Scopus).
      Affiliations:
       id:60023004 University of Delaware
       id:60030623 Rutgers, The State University of New Jersey
    11. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0037368024&origin=inward][2-s2.0-0037368024]]  J.R. Kitchin, M.A. Barteau and J.G. Chen, A comparison of gold and molybdenum nanoparticles on TiO2(1 1 0) 1 × 2 reconstructed single crystal surfaces, Surface Science, 526(3), p. 323-331, (2003). http://dx.doi.org/10.1016/S0039-6028(02)02679-1, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0037368024&origin=inward, cited 30 times (Scopus).
      Affiliations:
       id:60023004 University of Delaware
