report
------

This class provides a function to generate a report on a `ScopusSearch <../reference/scopus.ScopusSearch>`_ object.  It outputs text in `Emacs org-format <http://orgmode.org/>`_.

*reports* summarizes the results in a variety of ways, such as the number of hits, which journals they are published in, who the coauthors are, their affiliations (here *reports* makes use of potentially cached author and affiliation views), how many times the articles have been published, and more.

.. code-block:: python
   
    >>> from scopus import report, ScopusSearch
    >>> s = ScopusSearch('FIRSTAUTH ( kitchin  j.r. )', refresh=True)
    >>> report(s, 'Kitchin - first author')
    *** Report for Kitchin - first author

        #+attr_latex: :placement [H] :center nil
        #+caption: Types of documents found for Kitchin - first author.
        | Document type | count |
        |-
        | Journal | 11 |
        | Conference Proceeding | 1 |



        11 articles (1539 citations) found by 12 authors

        #+attr_latex: :placement [H] :center nil
        #+caption: Author publication counts for Kitchin - first author.
        | name | count | categories |
        |-
        | [[https://www.scopus.com/authid/detail.uri?authorId=7004212771][Kitchin J.R.]] | 11 | Chemical Engineering (all) (26), Chemistry (all) (23), Physical and Theoretical Chemistry (22) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=7501891385][Chen J.G.]] | 5 | Catalysis (134), Physical and Theoretical Chemistry (129), Condensed Matter Physics (81) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=7005171428][Barteau M.A.]] | 5 | Physical and Theoretical Chemistry (111), Catalysis (81), Surfaces and Interfaces (80) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=7007042214][Norskov J.K.]] | 3 | Physical and Theoretical Chemistry (174), Condensed Matter Physics (134), Catalysis (130) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=7006349643][Reuter K.]] | 1 | Physics and Astronomy (all) (65), Condensed Matter Physics (58), Physical and Theoretical Chemistry (51) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=6602686751][Yakshinskiy B.]] | 1 | Condensed Matter Physics (26), Electrical and Electronic Engineering (16), Electronic, Optical and Magnetic Materials (14) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=50761335600][Van Gulick A.E.]] | 1 | Experimental and Cognitive Psychology (3), Ophthalmology (3), Cognitive Neuroscience (3) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=35514271900][Gellman A.J.]] | 1 | Physical and Theoretical Chemistry (92), Surfaces and Interfaces (65), Condensed Matter Physics (62) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=7102229641][Scheffler M.]] | 1 | Condensed Matter Physics (216), Physics and Astronomy (all) (178), Physical and Theoretical Chemistry (74) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=35477902900][Madey T.E.]] | 1 | Condensed Matter Physics (209), Surfaces and Interfaces (176), Physical and Theoretical Chemistry (147) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=7401797491][Khan N.A.]] | 1 | Physical and Theoretical Chemistry (14), Catalysis (9), Surfaces and Interfaces (6) |
        | [[https://www.scopus.com/authid/detail.uri?authorId=55755405700][Zilinski L.D.]] | 1 | Library and Information Sciences (7), Information Systems (4), Arts and Humanities (all) (1) |



        #+attr_latex: :placement [H] :center nil
        #+caption: Journal publication counts for Kitchin - first author.
        | Journal | count | IPP |
        |-
        | [[http://www.scopus.com/source/sourceInfo.url?sourceId=12284][Surface Science]] | 3 | 0 |
        | [[http://www.scopus.com/source/sourceInfo.url?sourceId=11000153773][Physical Review B - Condensed Matter and Materials]] | 2 | 0 |
        | [[http://www.scopus.com/source/sourceInfo.url?sourceId=145200][International Journal on Digital Libraries]] | 1 | 0 |
        | [[http://www.scopus.com/source/sourceInfo.url?sourceId=28134][Journal of Chemical Physics]] | 1 | 0 |
        | [[http://www.scopus.com/source/sourceInfo.url?sourceId=29150][Physical Review Letters]] | 1 | 0 |
        | [[http://www.scopus.com/source/sourceInfo.url?sourceId=16275][AIChE Journal]] | 1 | 0 |
        | [[http://www.scopus.com/source/sourceInfo.url?sourceId=16377][Catalysis Today]] | 1 | 0 |
        | [[http://www.scopus.com/source/sourceInfo.url?sourceId=19700188320][ACS Catalysis]] | 1 | 0 |



        #+attr_latex: :placement [H] :center nil
        #+caption: Journal publication counts for Kitchin - first author sorted by IPP.
        | Journal | count | IPP |
        |-
        |[[http://www.scopus.com/source/sourceInfo.url?sourceId=12284][Surface Science]]|3|0|
        |[[http://www.scopus.com/source/sourceInfo.url?sourceId=11000153773][Physical Review B - Condensed Matter and Materials]]|2|0|
        |[[http://www.scopus.com/source/sourceInfo.url?sourceId=145200][International Journal on Digital Libraries]]|1|0|
        |[[http://www.scopus.com/source/sourceInfo.url?sourceId=28134][Journal of Chemical Physics]]|1|0|
        |[[http://www.scopus.com/source/sourceInfo.url?sourceId=29150][Physical Review Letters]]|1|0|
        |[[http://www.scopus.com/source/sourceInfo.url?sourceId=16275][AIChE Journal]]|1|0|
        |[[http://www.scopus.com/source/sourceInfo.url?sourceId=16377][Catalysis Today]]|1|0|
        |[[http://www.scopus.com/source/sourceInfo.url?sourceId=19700188320][ACS Catalysis]]|1|0|


        #+attr_latex: :placement [H] :center nil
        #+caption: Top cited publication counts for Kitchin - first author. j-index = 8.
        | title | cite count |
        |-
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=2942640180&origin=inward][Modification of the surface electronic and chemical properti]] | 621 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=13444307808&origin=inward][Role of strain and ligand effects in the modification of the]] | 542 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0141924604&origin=inward][Elucidation of the active surface and origin of the weak met]] | 120 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=20544467859&origin=inward][Trends in the chemical properties of early transition metal ]] | 104 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=40949100780&origin=inward][Alloy surface segregation in reactive environments: First-pr]] | 74 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=67449106405&origin=inward][Correlations in coverage-dependent atomic adsorption energie]] | 42 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0037368024&origin=inward][A comparison of gold and molybdenum nanoparticles on TiO2(1 ]] | 30 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward][Examples of effective data sharing in scientific publishing]] | 5 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84971324241&origin=inward][High-throughput methods using composition and structure spre]] | 1 |
        | [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85019169906&origin=inward][Automating data sharing through authoring tools]] | 0 |


        #+caption: Number of authors on each publication for Kitchin - first author.
        [[./Kitchin - first author-nauthors-per-publication.png]]
        **** Bibliography  :noexport:
             :PROPERTIES:
             :VISIBILITY: folded
             :END:
        1. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85019169906&origin=inward][2-s2.0-85019169906]]  J.R. Kitchin, A.E. Van Gulick and L.D. Zilinski, Automating data sharing through authoring tools, International Journal on Digital Libraries, 18(2), p. 93-98, (2017). https://doi.org/10.1007/s00799-016-0173-7, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=85019169906&origin=inward, cited 0 times (Scopus).
          Affiliations:
           id:60027950 Carnegie Mellon University
        2. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84971324241&origin=inward][2-s2.0-84971324241]]  J.R. Kitchin and A.J. Gellman, High-throughput methods using composition and structure spread libraries, AIChE Journal, 62(11), p. 3826-3835, (2016). https://doi.org/10.1002/aic.15294, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84971324241&origin=inward, cited 1 times (Scopus).
          Affiliations:
           id:60027950 Carnegie Mellon University
        3. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930349644&origin=inward][2-s2.0-84930349644]]  John R. Kitchin, Data sharing in Surface Science, Surface Science, 647, p. 103-107, (2016). https://doi.org/10.1016/j.susc.2015.05.007, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930349644&origin=inward, cited 0 times (Scopus).
          Affiliations:
           id:60027950 Carnegie Mellon University
        4. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward][2-s2.0-84930616647]]  John R. Kitchin, Examples of effective data sharing in scientific publishing, ACS Catalysis, 5(6), p. 3894-3899, (2015). https://doi.org/10.1021/acscatal.5b00538, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward, cited 5 times (Scopus).
          Affiliations:
           id:60027950 Carnegie Mellon University
        5. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=67449106405&origin=inward][2-s2.0-67449106405]]  John R. Kitchin, Correlations in coverage-dependent atomic adsorption energies on Pd(111), Physical Review B - Condensed Matter and Materials Physics, 79(20), Art. No. 205412 (2009). https://doi.org/10.1103/PhysRevB.79.205412, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=67449106405&origin=inward, cited 42 times (Scopus).
          Affiliations:
           id:60027950 Carnegie Mellon University
        6. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=40949100780&origin=inward][2-s2.0-40949100780]]  J.R. Kitchin, K. Reuter and M. Scheffler, Alloy surface segregation in reactive environments: First-principles atomistic thermodynamics study of Ag3 Pd(111) in oxygen atmospheres, Physical Review B - Condensed Matter and Materials Physics, 77(7), Art. No. 075437 (2008). https://doi.org/10.1103/PhysRevB.77.075437, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=40949100780&origin=inward, cited 74 times (Scopus).
          Affiliations:
           id:60008644 Fritz Haber Institute of the Max Planck Society
           id:60027950 Carnegie Mellon University
        8. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=20544467859&origin=inward][2-s2.0-20544467859]]  J.R. Kitchin, J.K. Nørskov, M.A. Barteau and J.G. Chen, Trends in the chemical properties of early transition metal carbide surfaces: A density functional study, Catalysis Today, 105(1 SPEC. ISS.), p. 66-73, (2005). https://doi.org/10.1016/j.cattod.2005.04.008, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=20544467859&origin=inward, cited 104 times (Scopus).
          Affiliations:
           id:60023004 University of Delaware
           id:60011373 Danmarks Tekniske Universitet
        9. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=13444307808&origin=inward][2-s2.0-13444307808]]  J.R. Kitchin, J.K. Nørskov, M.A. Barteau and J.G. Chen, Role of strain and ligand effects in the modification of the electronic and chemical Properties of bimetallic surfaces, Physical Review Letters, 93(15), (no pages found) (2004). https://doi.org/10.1103/PhysRevLett.93.156801, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=13444307808&origin=inward, cited 542 times (Scopus).
          Affiliations:
           id:60023004 University of Delaware
           id:60011373 Danmarks Tekniske Universitet
        10. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=2942640180&origin=inward][2-s2.0-2942640180]]  J.R. Kitchin, J.K. Nørskov, M.A. Barteau and J.G. Chen, Modification of the surface electronic and chemical properties of Pt(111) by subsurface 3d transition metals, Journal of Chemical Physics, 120(21), p. 10240-10246, (2004). https://doi.org/10.1063/1.1737365, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=2942640180&origin=inward, cited 621 times (Scopus).
          Affiliations:
           id:60023004 University of Delaware
           id:60011373 Danmarks Tekniske Universitet
        11. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0141924604&origin=inward][2-s2.0-0141924604]]  J.R. Kitchin, N.A. Khan, M.A. Barteau, J.G. Chen, B. Yakshinskiy and T.E. Madey, Elucidation of the active surface and origin of the weak metal-hydrogen bond on Ni/Pt(1 1 1) bimetallic surfaces: A surface science and density functional theory study, Surface Science, 544(2-3), p. 295-308, (2003). https://doi.org/10.1016/j.susc.2003.09.007, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0141924604&origin=inward, cited 120 times (Scopus).
          Affiliations:
           id:60023004 University of Delaware
           id:60030623 Rutgers, The State University of New Jersey
        12. [[https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0037368024&origin=inward][2-s2.0-0037368024]]  J.R. Kitchin, M.A. Barteau and J.G. Chen, A comparison of gold and molybdenum nanoparticles on TiO2(1 1 0) 1 × 2 reconstructed single crystal surfaces, Surface Science, 526(3), p. 323-331, (2003). https://doi.org/10.1016/S0039-6028(02)02679-1, https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=0037368024&origin=inward, cited 30 times (Scopus).
          Affiliations:
           id:60023004 University of Delaware


After rendering, this yields

.. include:: report_example.rst
