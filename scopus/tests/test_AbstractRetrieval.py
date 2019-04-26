#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `AbstractRetrieval` module."""

from collections import namedtuple
from nose.tools import assert_equal, assert_true

import scopus

# Base information
ab1 = scopus.AbstractRetrieval("2-s2.0-84930616647", view="FULL", refresh=True)
# Conference proceeding and no references
ab2 = scopus.AbstractRetrieval("2-s2.0-0029486824", view="FULL", refresh=True)
# Issuetitle and no affiliation
ab3 = scopus.AbstractRetrieval("2-s2.0-0001270077", view="FULL", refresh=True)
# Author group broken and author keywords
ab4 = scopus.AbstractRetrieval("2-s2.0-0000016206", view="FULL", refresh=True)
# ISBN
ab5 = scopus.AbstractRetrieval("2-s2.0-84919546381", view="FULL", refresh=True)
# Funding, sequencebanks, chemicals
ab6 = scopus.AbstractRetrieval("2-s2.0-85053478849", view="FULL", refresh=True)
# Contributor group
ab7 = scopus.AbstractRetrieval("2-s2.0-85050253030", view="FULL", refresh=True)
# REF view
ab8 = scopus.AbstractRetrieval("2-s2.0-84951753303", view="REF", refresh=True)


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


def test_affiliation():
    aff = namedtuple('Affiliation', 'id name city country')
    expected = [aff(id='60027950', name='Carnegie Mellon University',
                    city='Pittsburgh', country='United States')]
    assert_equal(ab1.affiliation, expected)
    assert_equal(ab3.affiliation, None)


def test_aggregationType():
    assert_equal(ab1.aggregationType, 'Journal')
    assert_equal(ab2.aggregationType, 'Conference Proceeding')


def test_authkeywords():
    assert_equal(ab1.authkeywords, None)
    expected = ['Bayesian analysis', 'Seasonality',
                'Structural breaks', 'Unit roots']
    assert_equal(ab4.authkeywords, expected)


def test_authors():
    fields = 'auid indexed_name surname given_name affiliation_id'
    auth = namedtuple('Author', fields)
    expected = [auth(auid='7004212771', indexed_name='Kitchin J.R.',
                surname='Kitchin', given_name='John R.',
                affiliation_id=['60027950'])]
    assert_equal(ab1.authors, expected)


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


def test_citedby_count():
    expected = 5
    assert_true(ab1.citedby_count >= expected)


def test_citedby_link():
    expected = 'https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b'\
        '&scp=84930616647&origin=inward'
    assert_equal(ab1.citedby_link, expected)


def test_chemials():
    received = ab6.chemicals
    assert_true(isinstance(received, list))
    assert_equal(len(received), 5)
    chemical = namedtuple('Chemical', 'source chemical_name cas_registry_number')
    expected = chemical(source='esbd', chemical_name='magnesium',
                        cas_registry_number='7439-95-4')
    assert_true(expected in received)
    assert_equal(ab3.chemicals, None)


def test_confcode():
    assert_equal(ab2.confcode, '44367')


def test_confdate():
    assert_equal(ab2.confdate, ((1995, 12, 13), (1995, 12, 15)))


def test_conflocation():
    assert_equal(ab2.conflocation, 'New Orleans, LA, USA')


def test_confname():
    expected2 = "Proceedings of the 1995 34th IEEE Conference on Decision "\
                "and Control. Part 1 (of 4)"
    assert_equal(ab2.confname, expected2)
    assert_equal(ab3.confname, None)
    expected7 = '20th Symposium on Design, Test, Integration and Packaging '\
                'of MEMS and MOEMS, DTIP 2018'
    assert_equal(ab7.confname, expected7)


def test_confsponsor():
    assert_equal(ab2.confsponsor, 'IEEE')
    assert_equal(ab3.confsponsor, None)
    expected7 = ['ARTOV.IMM.CNR.IT', 'CMP.IMAG.FR', 'CNRS.FR',
                 'EPS.IEEE.ORG', 'LIRMM.FR']
    assert_equal(ab7.confsponsor, expected7)


def test_contributor_group():
    fields = 'given_name initials surname indexed_name role'
    pers = namedtuple('Contributor', fields)
    expected = pers(given_name='Romolo', initials='R.', surname='Marcelli',
                    indexed_name='Marcelli R.', role='edit')
    received = ab7.contributor_group
    assert_equal(len(received), 7)
    assert_true(expected in received)
    assert_equal(ab3.contributor_group, None)


def test_correspondence():
    fields = 'surname initials organization country city_group'
    corr = namedtuple('Correspondence', fields)
    expected2 = corr(surname='Boukas', initials='E.K.',
        organization='Ecole Polytechnique de Montreal', country='Canada',
        city_group='Montreal')
    assert_equal(ab2.correspondence, expected2)
    assert_equal(ab3.correspondence, None)


def test_coverDate():
    assert_true(ab1.coverDate, '2015-06-05')


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


def test_doi():
    assert_equal(ab1.doi, '10.1021/acscatal.5b00538')
    assert_equal(ab4.doi, None)


def test_eid():
    assert_equal(ab1.eid, '2-s2.0-84930616647')


def test_endingPage():
    assert_equal(ab1.endingPage, '3899')


def test_funding():
    received = ab6.funding
    assert_true(isinstance(received, list))
    assert_equal(len(received), 2)
    fund = namedtuple('Funding', 'agency string id acronym country')
    expected6 = fund(agency=None, string='CNRT',
        acronym=None, id=None, country=None)
    assert_true(expected6 in received)
    assert_equal(ab5.funding, None)


def test_funding_text():
    e = 'The authors gratefully acknowledge CNRT “Nickel et son '\
        'Environnement” for providing the financial support. The results '\
        'reported in this publication are gathered from the CNRT report '\
        '“Ecomine BioTop”. Appendix A'
    assert_equal(ab6.funding_text, e)


def test_get_html():
    e = '@article{Kaufmann1991FairnessPricing,\n  author = {Patrick J. '\
        'Kaufmann and Gwen Ortmeyer and N. Craig Smith},\n  title = {{'\
        'Fairness in consumer pricing}},\n  journal = {Journal of Consumer '\
        'Policy},\n  year = {1991},\n  volume = {14},\n  number = {2},\n  '\
        'pages = {117-140},\n  doi = {10.1007/BF00381915}}'
    assert_equal(ab3.get_bibtex(), e)


def test_get_latex():
    e = 'Philip Hans Franses, Henk Hoekh and Richard Paap, \\textit{'\
        'Bayesian analysis of seasonal unit roots and seasonal mean shifts},'\
        ' Journal of Econometrics, \\textbf{78(2)}, pp. 359-380 (1997).\\'\
        'href{https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&'\
        'scp=0000016206&origin=inward}{scopus:2-s2.0-0000016206}.'
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
        '55456187700">N. Craig Smith</a>, <a href="https://www.scopus.com/'\
        'inward/record.uri?partnerID=HzOxMe3b&scp=0001270077&origin=inward'\
        '">Fairness in consumer pricing</a>, <a href="https://www.scopus.'\
        'com/source/sourceInfo.url?sourceId=130073">Journal of Consumer '\
        'Policy</a>, <b>14(2)</b>, pp. 117-140, (1991). <a href="https://'\
        'doi.org/10.1007/BF00381915">doi:10.1007/BF00381915</a>.'
    assert_equal(ab3.get_html(), e)


def test_isbn():
    assert_equal(ab3.isbn, None)
    assert_equal(ab5.isbn, ('0203881486', '9780203881484'))


def test_issn():
    assert_equal(ab1.issn, '21555435')
    assert_equal(ab5.issn, None)


def test_identifier():
    assert_equal(ab1.identifier, '84930616647')


def test_idxterms():
    expected = ['Control variables', 'Cost function',
                'Hamilton-Jacobi-Isaacs equation', 'Machine capacity',
                'Stochastic manufacturing systems', 'Value function']
    assert_equal(ab2.idxterms, expected)
    assert_equal(ab4.idxterms, None)


def test_issueIdentifier():
    assert_equal(ab1.issueIdentifier, '6')


def test_issuetitle():
    assert_equal(ab3.issuetitle, 'Law, Economics and Behavioural Sciences')


def test_language():
    assert_equal(ab1.language, 'eng')


def test_pageRange():
    assert_equal(ab1.pageRange, '3894-3899')


def test_publicationName():
    assert_equal(ab1.publicationName, 'ACS Catalysis')


def test_publisher():
    assert_equal(ab1.publisher, 'American Chemical Society')


def test_publisheraddress():
    assert_equal(ab2.publisheraddress, 'Piscataway, NJ, United States')


def test_refcount():
    assert_equal(ab4.refcount, '18')


def test_references():
    fields = 'position id doi title authors authors_auid authors_affiliationid '\
             'sourcetitle publicationyear volume issue first last citedbycount '\
             'text fulltext'
    ref = namedtuple('Reference', fields)
    fulltext1 = 'Implementing Reproducible Research; Stodden, V.; Leisch, '\
                'F.; Peng, R. D., Eds., Chapman and Hall/CRC: London, 2014.'
    expected1 = ref(position='22', id='85055586929', doi=None, title=None,
        authors='Stodden, V.; Leisch, F.; Peng, R.D.', authors_auid=None,
        authors_affiliationid=None, fulltext=fulltext1,
        sourcetitle='Implementing Reproducible Research',
        publicationyear='2014', volume=None, issue=None, first=None,
        last=None, citedbycount=None, text='Eds. Chapman and Hall/CRC: London.')
    assert_equal(ab1.references[-1], expected1)
    assert_equal(ab2.references, None)
    fulltext4 = 'Chib, S., 1995, Marginal likelihood from the Gibbs output, '\
                'Journal of the American Statistical Association 90, 1313-1321.'
    expected4 = ref(position='1', id='0041974049', doi=None,
        title='Marginal likelihood from the Gibbs output', authors='Chib, S.',
        sourcetitle='Journal of the American Statistical Association',
        publicationyear='1995', volume='90', issue=None, first='1313',
        last='1321', text=None, fulltext=fulltext4, citedbycount=None,
        authors_auid=None, authors_affiliationid=None)
    authors3 = 'Armbrust, Michael; Fox, Armando; Griffith, Rean; Joseph, '\
        'Anthony D.; Katz, Randy; Konwinski, Andy; Lee, Gunho; '\
        'Patterson, David; Rabkin, Ariel; Stoica, Ion; Zaharia, Matei'
    expected8 =  ref(position='1', id='77950347409', authors=authors3,
        doi='10.1145/1721654.1721672', title='A view of cloud computing',
        sourcetitle='Communications of the ACM',
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


def test_sequencebank():
    received = ab6.sequencebank
    assert_true(isinstance(received, list))
    bank = namedtuple('Chemical', 'name sequence_number type')
    expected = bank(name='GENBANK', type='submitted',
                    sequence_number='MH150839:MH150870')
    assert_true(expected in received)
    assert_equal(ab3.sequencebank, None)


def test_source_id():
    assert_equal(ab1.source_id, '19700188320')


def test_sourcetitle_abbreviation():
    assert_equal(ab1.sourcetitle_abbreviation, 'ACS Catal.')


def test_srctype():
    assert_equal(ab1.srctype, 'j')
    assert_equal(ab2.srctype, 'p')


def test_startingPage():
    assert_equal(ab1.startingPage, '3894')


def test_subject_areas():
    area = namedtuple('Area', 'area abbreviation code')
    expected = [area(area='Catalysis', abbreviation='CENG', code='1503'),
                area(area='Chemistry (all)', abbreviation='CHEM', code='1600')]
    assert_equal(ab1.subject_areas, expected)


def test_title():
    expected = 'Examples of effective data sharing in scientific publishing'
    assert_equal(ab1.title, expected)


def test_url():
    expected = 'https://api.elsevier.com/content/abstract/scopus_id/84930616647'
    assert_equal(ab1.url, expected)


def test_volume():
    assert_equal(ab1.volume, '5')


def test_website():
    assert_equal(ab1.website, 'http://pubs.acs.org/page/accacs/about.html')
    assert_equal(ab2.website, None)
