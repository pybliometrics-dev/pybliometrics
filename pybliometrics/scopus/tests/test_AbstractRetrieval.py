#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.AbstractRetrieval` module."""

from collections import namedtuple
from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import AbstractRetrieval

# Base information
ab1 = AbstractRetrieval("2-s2.0-84930616647", view="FULL", refresh=30)
# Conference proceeding and no references
ab2 = AbstractRetrieval("2-s2.0-0029486824", view="FULL", refresh=30)
# Issuetitle and no affiliation
ab3 = AbstractRetrieval("2-s2.0-0001270077", view="FULL", refresh=30)
# Author group broken and author keywords
ab4 = AbstractRetrieval("2-s2.0-0000016206", view="FULL", refresh=30)
# ISBN
ab5 = AbstractRetrieval("2-s2.0-84919546381", view="FULL", refresh=30)
# Funding, sequencebanks, chemicals
ab6 = AbstractRetrieval("2-s2.0-85040230676", view="FULL", refresh=30)
# Contributor group
ab7 = AbstractRetrieval("2-s2.0-85050253030", view="FULL", refresh=30)
# REF view
ab8 = AbstractRetrieval("2-s2.0-84951753303", view="REF", refresh=30)


def test_abstract():
    expected = 'In this paper we propose a Bayesian analysis of seasonal '\
        'unit roots in quarterly observed time series. Seasonal unit root '\
        'processes are useful to describe economic series with changing '\
        'seasonal fluctuations. A natural alternative model for similar '\
        'purposes contains deterministic seasonal mean shifts instead of '\
        'seasonal stochastic trends. This leads to analysing seasonal unit '\
        'roots in the presence of mean shifts using Bayesian techniques. '\
        'Our method is illustrated using several simulated and empirical data.'
    assert_equal(ab4.abstract, expected)
    assert_equal(ab8.abstract, None)


def test_affiliation():
    aff = namedtuple('Affiliation', 'id name city country')
    expected = [aff(id='60027950', name='Carnegie Mellon University',
                    city='Pittsburgh', country='United States')]
    assert_equal(ab1.affiliation, expected)
    assert_equal(ab3.affiliation, None)
    assert_equal(ab8.affiliation, None)


def test_aggregationType():
    assert_equal(ab1.aggregationType, 'Journal')
    assert_equal(ab2.aggregationType, 'Conference Proceeding')
    assert_equal(ab8.aggregationType, None)


def test_authkeywords():
    assert_equal(ab1.authkeywords, None)
    expected = ['Bayesian analysis', 'Seasonality',
                'Structural breaks', 'Unit roots']
    assert_equal(ab4.authkeywords, expected)
    assert_equal(ab8.authkeywords, None)


def test_authorgroup():
    fields = 'affiliation_id dptid organization city postalcode '\
             'addresspart country auid indexed_name surname given_name'
    auth = namedtuple('Author', fields)
    expected = [auth(affiliation_id='60027950', dptid='110785688',
        organization='Department of Chemical Engineering, Carnegie Mellon University',
        city='Pittsburgh', postalcode='15213', addresspart='5000 Forbes Avenue',
        country='United States', auid='7004212771',
        indexed_name='Kitchin J.', surname='Kitchin', given_name='John R.')]
    assert_equal(ab1.authorgroup, expected)
    assert_equal(ab8.authorgroup, None)


def test_authors():
    fields = 'auid indexed_name surname given_name affiliation_id'
    auth = namedtuple('Author', fields)
    expected = [auth(auid='7004212771', indexed_name='Kitchin J.R.',
                surname='Kitchin', given_name='John R.',
                affiliation_id=['60027950'])]
    assert_equal(ab1.authors, expected)
    assert_equal(ab8.authors, None)


def test_citedby_count():
    expected = 5
    assert_true(ab1.citedby_count >= expected)
    assert_equal(ab8.citedby_count, None)


def test_citedby_link():
    expected = 'https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b'\
        '&scp=84930616647&origin=inward'
    assert_equal(ab1.citedby_link, expected)
    assert_equal(ab8.citedby_link, None)


def test_chemials():
    received = ab6.chemicals
    assert_true(isinstance(received, list))
    assert_equal(len(received), 6)
    chemical = namedtuple('Chemical', 'source chemical_name cas_registry_number')
    expected = chemical(source='esbd', cas_registry_number='126547-89-5',
        chemical_name='intercellular adhesion molecule 1')
    assert_true(expected in received)
    assert_equal(ab3.chemicals, None)
    assert_equal(ab8.chemicals, None)


def test_confcode():
    assert_equal(ab2.confcode, '44367')
    assert_equal(ab8.confcode, None)


def test_confdate():
    assert_equal(ab2.confdate, ((1995, 12, 13), (1995, 12, 15)))
    assert_equal(ab8.confdate, None)


def test_conflocation():
    assert_equal(ab2.conflocation, 'New Orleans, LA, USA')
    assert_equal(ab8.conflocation, None)


def test_confname():
    expected2 = "Proceedings of the 1995 34th IEEE Conference on Decision "\
                "and Control. Part 1 (of 4)"
    assert_equal(ab2.confname, expected2)
    assert_equal(ab3.confname, None)
    expected7 = '20th Symposium on Design, Test, Integration and Packaging '\
                'of MEMS and MOEMS, DTIP 2018'
    assert_equal(ab7.confname, expected7)
    assert_equal(ab8.confname, None)


def test_confsponsor():
    assert_equal(ab2.confsponsor, 'IEEE')
    assert_equal(ab3.confsponsor, None)
    expected7 = ['ARTOV.IMM.CNR.IT', 'CMP.IMAG.FR', 'CNRS.FR',
                 'EPS.IEEE.ORG', 'LIRMM.FR']
    assert_equal(ab7.confsponsor, expected7)
    assert_equal(ab8.confsponsor, None)


def test_contributor_group():
    fields = 'given_name initials surname indexed_name role'
    pers = namedtuple('Contributor', fields)
    expected = pers(given_name='Romolo', initials='R.', surname='Marcelli',
                    indexed_name='Marcelli R.', role='edit')
    received = ab7.contributor_group
    assert_equal(len(received), 7)
    assert_true(expected in received)
    assert_equal(ab3.contributor_group, None)
    assert_equal(ab8.contributor_group, None)


def test_correspondence():
    fields = 'surname initials organization country city_group'
    corr = namedtuple('Correspondence', fields)
    expected2 = corr(surname='Boukas', initials='E.K.',
        organization='Ecole Polytechnique de Montreal', country='Canada',
        city_group='Montreal')
    assert_equal(ab2.correspondence, expected2)
    assert_equal(ab3.correspondence, None)
    assert_equal(ab8.correspondence, None)


def test_coverDate():
    assert_equal(ab1.coverDate, '2015-06-05')
    assert_equal(ab8.coverDate, None)


def test_description():
    expected = 'In this paper we propose a Bayesian analysis of seasonal '\
               'unit roots in quarterly observed time series. Seasonal unit '\
               'root processes are useful to describe economic series with '\
               'changing seasonal fluctuations. A natural alternative model '\
               'for similar purposes contains deterministic seasonal mean '\
               'shifts instead of seasonal stochastic trends. This leads to '\
               'analysing seasonal unit roots in the presence of mean '\
               'shifts using Bayesian techniques. Our method is illustrated '\
               'using several simulated and empirical data.'
    assert_equal(ab4.description, expected)
    assert_equal(ab8.description, None)


def test_doi():
    assert_equal(ab1.doi, '10.1021/acscatal.5b00538')
    assert_equal(ab4.doi, '10.1016/s0304-4076(97)00018-3')
    assert_equal(ab8.doi, None)


def test_eid():
    assert_equal(ab1.eid, '2-s2.0-84930616647')
    assert_equal(ab8.eid, None)


def test_endingPage():
    assert_equal(ab1.endingPage, '3899')
    assert_equal(ab8.endingPage, None)


def test_funding():
    received = ab6.funding
    assert_true(isinstance(received, list))
    assert_equal(len(received), 5)
    fund = namedtuple('Funding', 'agency string id acronym country')
    expected6 = fund(agency='Deutsche Forschungsgemeinschaft',
        string='German Research Foundation', acronym='DFG',
        id='http://data.elsevier.com/vocabulary/SciValFunders/501100001659',
        country='http://sws.geonames.org/2921044/')
    assert_true(expected6 in received)
    assert_equal(ab5.funding, None)
    assert_equal(ab8.funding, None)


def test_funding_text():
    e = 'ACKNOWLEDGMENTS. We thank Dieter Blaas for providing ICAM-1–specific '\
        'antiserum (supersup). This work was supported by Netherlands '\
        'Organization for Scientific Research Grant NWO-VICI-91812628 '\
        '(to F.J.M.v.K.), by German Research Foundation Grant SFB685 '\
        '(to T.S. and G.Z.), and Wellcome Trust PhD Studentship support '\
        '102572/B/13/Z (to D.L.H.). All EM was performed in the Astbury '\
        'Biostructure Laboratory, which was funded by the University of '\
        'Leeds and the Wellcome Trust (108466/Z/15/Z).'
    assert_equal(ab6.funding_text, e)
    assert_equal(ab8.funding_text, None)


def test_get_bibtex():
    e = '@article{Kaufmann1991FairnessPricing,\n  author = {Patrick J. '\
        'Kaufmann and Gwen Ortmeyer and N. Craig Smith},\n  title = {{'\
        'Fairness in consumer pricing}},\n  journal = {Journal of Consumer '\
        'Policy},\n  year = {1991},\n  volume = {14},\n  number = {2},\n  '\
        'pages = {117-140},\n  doi = {10.1007/BF00381915}}'
    assert_equal(ab3.get_bibtex(), e)


def test_get_latex():
    e = 'Philip Hans Franses, Henk Hoekh and Richard Paap, \\textit{'\
        'Bayesian analysis of seasonal unit roots and seasonal mean shifts}, '\
        'Journal of Econometrics, \\textbf{78(2)}, pp. 359-380 (1997). \\'\
        'href{https://doi.org/10.1016/s0304-4076(97)00018-3}{doi:10.1016/'\
        's0304-4076(97)00018-3}, \\href{https://www.scopus.com/inward/'\
        'record.uri?partnerID=HzOxMe3b&scp=0000016206&origin=inward}'\
        '{scopus:2-s2.0-0000016206}.'
    assert_equal(ab4.get_latex(), e)


def test_get_ris():
    e = 'TY  - JOUR\nTI  - Examples of effective data sharing in scientific '\
        'publishing\nJO  - ACS Catalysis\nVL  - 5\nDA  - 2015-06-05\nPY  - '\
        '2015\nSP  - 3894-3899\nAU  - Kitchin J.R.\nDO  - 10.1021/'\
        'acscatal.5b00538\nUR  - https://doi.org/10.1021/acscatal.5b00538\n'\
        'IS  - 6\nER  - \n\n'
    assert_equal(ab1.get_ris(), e)


def test_get_html():
    e = '<a href="https://www.scopus.com/authid/detail.url?origin=Author'\
        'Profile&authorId=7201922462">Patrick J. Kaufmann</a>, <a href="'\
        'https://www.scopus.com/authid/detail.url?origin=AuthorProfile&'\
        'authorId=16430389100">Gwen Ortmeyer</a> and <a href="https://'\
        'www.scopus.com/authid/detail.url?origin=AuthorProfile&authorId='\
        '55613241349">N. Craig Smith</a>, <a href="https://www.scopus.com/'\
        'inward/record.uri?partnerID=HzOxMe3b&scp=0001270077&origin=inward">'\
        'Fairness in consumer pricing</a>, <a href="https://www.scopus.com/'\
        'source/sourceInfo.url?sourceId=130073">Journal of Consumer Policy'\
        '</a>, <b>14(2)</b>, pp. 117-140, (1991). <a href="https://doi.org/'\
        '10.1007/BF00381915">doi:10.1007/BF00381915</a>.'
    assert_equal(ab3.get_html(), e)


def test_isbn():
    assert_equal(ab3.isbn, None)
    assert_equal(ab5.isbn, ('0203881486', '9780203881484'))
    assert_equal(ab8.isbn, None)


def test_issn():
    assert_equal(ab1.issn, '21555435')
    assert_equal(ab5.issn, None)
    assert_equal(ab8.issn, None)


def test_identifier():
    assert_equal(ab1.identifier, '84930616647')
    assert_equal(ab8.identifier, None)


def test_idxterms():
    expected = ['Control variables', 'Cost function',
                'Hamilton-Jacobi-Isaacs equation', 'Machine capacity',
                'Stochastic manufacturing systems', 'Value function']
    assert_equal(ab2.idxterms, expected)
    assert_equal(ab4.idxterms, None)


def test_issueIdentifier():
    assert_equal(ab1.issueIdentifier, '6')
    assert_equal(ab8.issueIdentifier, None)


def test_issuetitle():
    assert_equal(ab3.issuetitle, 'Law, Economics and Behavioural Sciences')
    assert_equal(ab8.issuetitle, None)


def test_language():
    assert_equal(ab1.language, 'eng')
    assert_equal(ab8.language, None)


def test_openaccess():
    assert_equal(ab5.openaccess, "2")
    assert_equal(ab6.openaccess, "1")
    assert_equal(ab7.openaccess, "0")
    assert_equal(ab8.openaccess, None)


def test_openaccessFlag():
    assert_equal(ab5.openaccessFlag, None)
    assert_equal(ab6.openaccessFlag, True)
    assert_equal(ab7.openaccessFlag, False)
    assert_equal(ab8.openaccessFlag, None)


def test_pageRange():
    assert_equal(ab1.pageRange, '3894-3899')
    assert_equal(ab8.pageRange, None)


def test_pii():
    assert_equal(ab4.pii, 'S0304407697000183')
    assert_equal(ab5.pii, None)
    assert_equal(ab6.pii, None)


def test_publicationName():
    assert_equal(ab1.publicationName, 'ACS Catalysis')
    assert_equal(ab8.publicationName, None)


def test_publisher():
    assert_equal(ab1.publisher, 'American Chemical Society')
    assert_equal(ab8.publisher, None)


def test_publisheraddress():
    assert_equal(ab2.publisheraddress, 'Piscataway, NJ, United States')
    assert_equal(ab8.publisheraddress, None)


def test_pubmed_id():
    assert_equal(ab6.pubmed_id, '29284752')
    assert_equal(ab7.pubmed_id, None)


def test_refcount():
    assert_equal(ab4.refcount, '18')
    assert_equal(ab8.refcount, '48')


def test_references_full():
    fields = 'position id doi title authors authors_auid authors_affiliationid '\
             'sourcetitle publicationyear volume issue first last citedbycount '\
             'type text fulltext'
    ref = namedtuple('Reference', fields)
    fulltext1 = 'Implementing Reproducible Research; Stodden, V.; Leisch, '\
                'F.; Peng, R. D., Eds., Chapman and Hall/CRC: London, 2014.'
    expected1 = ref(position='22', id='85055586929', doi=None, title=None,
        authors='Stodden, V.; Leisch, F.; Peng, R.D.', authors_auid=None,
        authors_affiliationid=None, fulltext=fulltext1,
        sourcetitle='Implementing Reproducible Research', type=None,
        publicationyear='2014', volume=None, issue=None, first=None,
        last=None, citedbycount=None, text='Eds. Chapman and Hall/CRC: London.')
    assert_equal(ab1.references[-1], expected1)
    assert_equal(ab2.references, None)


def test_references_ref():
    fields = 'position id doi title authors authors_auid authors_affiliationid '\
             'sourcetitle publicationyear volume issue first last citedbycount '\
             'type text fulltext'
    ref = namedtuple('Reference', fields)
    authors8 = 'Armbrust, Michael; Fox, Armando; Griffith, Rean; Joseph, '\
        'Anthony D.; Katz, Randy; Konwinski, Andy; Lee, Gunho; '\
        'Patterson, David; Rabkin, Ariel; Stoica, Ion; Zaharia, Matei'
    expected8 = ref(position='1', id='77950347409', authors=authors8,
        doi='10.1145/1721654.1721672', title='A view of cloud computing',
        sourcetitle='Communications of the ACM', type='resolvedReference',
        publicationyear=None, volume='53', issue='4', first='50',
        last='58', text=None, fulltext=None, citedbycount='0',
        authors_auid='35800975300; 35571093800; 57198081560; 7202236336; '\
            '7401788602; 25926395200; 56326032000; 7401930147; 26534952300; '\
            '7007009125; 15064891400',
        authors_affiliationid='60025038; 60025038; 60025038; 60025038; 60025038; '\
            '60025038; 60025038; 60025038; 60025038; 60025038; 60025038')
    assert_true(int(ab8.references[0].citedbycount) >= 0)
    assert_equal(ab8.references[0]._replace(citedbycount="0"), expected8)


def test_scopus_link():
    expected = 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&'\
        'scp=84930616647&origin=inward'
    assert_equal(ab1.scopus_link, expected)


def test_self_link():
    expected = 'https://api.elsevier.com/content/abstract/scopus_id/84930616647'
    assert_equal(ab1.self_link, expected)
    assert_equal(ab8.self_link, None)


def test_sequencebank():
    received = ab6.sequencebank
    assert_true(isinstance(received, list))
    assert_equal(len(received), 3)
    bank = namedtuple('Chemical', 'name sequence_number type')
    expected = bank(name='GENBANK', sequence_number='MG272373',
                    type='referenced')
    assert_true(expected in received)
    assert_equal(ab3.sequencebank, None)
    assert_equal(ab8.sequencebank, None)


def test_source_id():
    assert_equal(ab1.source_id, '19700188320')
    assert_equal(ab8.source_id, None)


def test_sourcetitle_abbreviation():
    assert_equal(ab1.sourcetitle_abbreviation, 'ACS Catal.')
    assert_equal(ab8.sourcetitle_abbreviation, None)


def test_srctype():
    assert_equal(ab1.srctype, 'j')
    assert_equal(ab2.srctype, 'p')
    assert_equal(ab8.srctype, None)


def test_startingPage():
    assert_equal(ab1.startingPage, '3894')
    assert_equal(ab8.startingPage, None)


def test_subject_areas():
    area = namedtuple('Area', 'area abbreviation code')
    expected = [area(area='Catalysis', abbreviation='CENG', code='1503'),
                area(area='Chemistry (all)', abbreviation='CHEM', code='1600')]
    assert_equal(ab1.subject_areas, expected)
    assert_equal(ab8.subject_areas, None)


def test_title():
    expected = 'Examples of effective data sharing in scientific publishing'
    assert_equal(ab1.title, expected)
    assert_equal(ab8.title, None)


def test_url():
    expected = 'https://api.elsevier.com/content/abstract/scopus_id/84930616647'
    assert_equal(ab1.url, expected)
    assert_equal(ab8.url, None)


def test_volume():
    assert_equal(ab1.volume, '5')
    assert_equal(ab8.volume, None)


def test_website():
    assert_equal(ab1.website, 'http://pubs.acs.org/page/accacs/about.html')
    assert_equal(ab2.website, None)
    assert_equal(ab8.website, None)
