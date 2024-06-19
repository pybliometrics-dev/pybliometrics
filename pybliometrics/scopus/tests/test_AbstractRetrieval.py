"""Tests for `scopus.AbstractRetrieval` module."""

from collections import namedtuple

from pybliometrics.scopus import AbstractRetrieval, init

init()

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
# Collaboration
ab9 = AbstractRetrieval("2-s2.0-85097473741", view="FULL", refresh=30)
# ENTITLED view
ar10 = AbstractRetrieval('10.1109/Multi-Temp.2019.8866947', view='ENTITLED', refresh=30)
# REF view without refs
ab11 = AbstractRetrieval('2-s2.0-0031874638', view="REF", refresh=30)
# FULL view with list of collaborations
ab12 = AbstractRetrieval('2-s2.0-85044008512', view='FULL', refresh=30)


def test_abstract():
    expected = 'In this paper we propose a Bayesian analysis of seasonal '\
        'unit roots in quarterly observed time series. Seasonal unit root '\
        'processes are useful to describe economic series with changing '\
        'seasonal fluctuations. A natural alternative model for similar '\
        'purposes contains deterministic seasonal mean shifts instead of '\
        'seasonal stochastic trends. This leads to analysing seasonal unit '\
        'roots in the presence of mean shifts using Bayesian techniques. '\
        'Our method is illustrated using several simulated and empirical data.'
    assert ab4.abstract == expected
    assert ab8.abstract is None


def test_affiliation():
    aff = namedtuple('Affiliation', 'id name city country')
    expected = [aff(id=60104842, name='College of Engineering',
                    city='Pittsburgh', country='United States')]
    assert ab1.affiliation == expected
    assert ab3.affiliation is None
    assert ab8.affiliation is None


def test_aggregationType():
    assert ab1.aggregationType == 'Journal'
    assert ab2.aggregationType == 'Conference Proceeding'
    assert ab8.aggregationType is None


def test_authkeywords():
    assert ab1.authkeywords is None
    expected = ['Bayesian analysis', 'Seasonality',
                'Structural breaks', 'Unit roots']
    assert ab4.authkeywords == expected
    assert ab8.authkeywords is None


def test_authorgroup():
    fields = 'affiliation_id collaboration_id dptid organization city postalcode '\
        'addresspart country auid orcid indexed_name surname given_name'
    auth = namedtuple('Author', fields, defaults=[None for _ in fields.split()])
    # Test FULL document w.o. collaboration
    expected = [auth(affiliation_id=60104842, dptid=None,
        organization='Department of Chemical Engineering, Carnegie Mellon University',
        city='Pittsburgh', postalcode='15213', addresspart='5000 Forbes Avenue',
        country='United States', auid=7004212771, orcid=None, indexed_name='Kitchin J.R.',
        surname='Kitchin', given_name='John R.')]
    assert ab1.authorgroup == expected
    # Test FULL document w. 1 collaboration
    expected = auth(auid=7403019450, indexed_name='Ahn J.K.', surname='Ahn', given_name='J.K.')
    assert ab9.authorgroup[0] == expected
    # Test FULL document w. list of collaborations
    expected = auth(collaboration_id='S0920379618302370-8f4b482a50491834a3f938b012344bfd',
                indexed_name='JET Contributors')
    assert ab12.authorgroup[-1] == expected
    # Test REF view
    assert ab8.authorgroup is None


def test_authors():
    fields = 'auid indexed_name surname given_name affiliation_id'
    auth = namedtuple('Author', fields)
    expected = [auth(auid=7004212771, indexed_name='Kitchin J.R.',
                surname='Kitchin', given_name='John R.',
                affiliation_id='60104842')]
    assert ab1.authors == expected
    assert ab8.authors is None
    assert ar10.authors is None


def test_citedby_count():
    expected = 5
    assert ab1.citedby_count >= expected
    assert ab8.citedby_count is None


def test_citedby_link():
    expected = 'https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b'\
        '&scp=84930616647&origin=inward'
    assert ab1.citedby_link == expected
    assert ab8.citedby_link is None


def test_chemials():
    received = ab6.chemicals
    assert isinstance(received, list)
    assert len(received) == 6
    chemical = namedtuple('Chemical', 'source chemical_name cas_registry_number')
    expected = chemical(source='esbd', cas_registry_number='126547-89-5',
        chemical_name='intercellular adhesion molecule 1')
    assert expected in received
    assert ab3.chemicals is None
    assert ab8.chemicals is None


def test_confcode():
    assert ab2.confcode == 44367
    assert ab8.confcode is None


def test_confdate():
    assert ab2.confdate == ((1995, 12, 13), (1995, 12, 15))
    assert ab8.confdate is None


def test_conflocation():
    assert ab2.conflocation == 'New Orleans, LA, USA'
    assert ab8.conflocation is None


def test_confname():
    expected2 = "Proceedings of the 1995 34th IEEE Conference on Decision "\
                "and Control. Part 1 (of 4)"
    assert ab2.confname == expected2
    assert ab3.confname is None
    expected7 = '20th Symposium on Design, Test, Integration and Packaging '\
                'of MEMS and MOEMS, DTIP 2018'
    assert ab7.confname == expected7
    assert ab8.confname is None


def test_confsponsor():
    assert ab2.confsponsor == 'IEEE'
    assert ab3.confsponsor is None
    expected7 = ['ARTOV.IMM.CNR.IT', 'CMP.IMAG.FR', 'CNRS.FR',
                 'EPS.IEEE.ORG', 'LIRMM.FR']
    assert ab7.confsponsor == expected7
    assert ab8.confsponsor is None


def test_contributor_group():
    fields = 'given_name initials surname indexed_name role'
    pers = namedtuple('Contributor', fields)
    expected = pers(given_name='Romolo', initials='R.', surname='Marcelli',
                    indexed_name='Marcelli R.', role='edit')
    received = ab7.contributor_group
    assert len(received) == 7
    assert expected in received
    assert ab3.contributor_group is None
    assert ab8.contributor_group is None


def test_copyright():
    assert ab8.copyright is None
    expected = "Copyright 2021 Elsevier B.V., All rights reserved."
    assert ab9.copyright == expected


def test_copyright_type():
    assert ab8.copyright_type is None
    assert ab9.copyright_type == "Elsevier"


def test_correspondence():
    fields = 'surname initials organization country city_group'
    corr = namedtuple('Correspondence', fields)
    expected2 = corr(surname='Boukas', initials='E.K.',
        organization='Ecole Polytechnique de Montreal', country='Canada',
        city_group='Montreal')
    assert ab2.correspondence[0] == expected2
    assert ab3.correspondence is None
    assert ab8.correspondence is None


def test_coverDate():
    assert ab1.coverDate == '2015-06-05'
    assert ab8.coverDate is None


def test_date_created():
    assert ab8.date_created is None
    assert ab9.date_created == (2021, 9, 14)


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
    assert ab4.description == expected
    assert ab8.description is None


def test_doi():
    assert ab1.doi == '10.1021/acscatal.5b00538'
    assert ab4.doi == '10.1016/s0304-4076(97)00018-3'
    assert ab8.doi is None


def test_eid():
    assert ab1.eid == '2-s2.0-84930616647'
    assert ab8.eid is None


def test_endingPage():
    assert ab1.endingPage == '3899'
    assert ab8.endingPage is None


def test_entitlement():
    assert ab8.document_entitlement_status is None
    assert ab9.document_entitlement_status is None
    assert ar10.document_entitlement_status == 'ENTITLED'


def test_funding():
    received = ab6.funding
    assert isinstance(received, list)
    assert len(received) == 5
    fund = namedtuple('Funding', 'agency agency_id string funding_id acronym country')
    expected6 = fund(
        agency='Deutsche Forschungsgemeinschaft',
        agency_id='http://data.elsevier.com/vocabulary/SciValFunders/501100001659',
        string='German Research Foundation', acronym='DFG',
        funding_id=['SFB685'],
        country='http://sws.geonames.org/2921044/')
    assert expected6 in received
    assert ab5.funding is None
    assert ab8.funding is None


def test_funding_text():
    e = 'ACKNOWLEDGMENTS. We thank Dieter Blaas for providing ICAM-1–specific '\
        'antiserum (supersup). This work was supported by Netherlands '\
        'Organization for Scientific Research Grant NWO-VICI-91812628 '\
        '(to F.J.M.v.K.), by German Research Foundation Grant SFB685 '\
        '(to T.S. and G.Z.), and Wellcome Trust PhD Studentship support '\
        '102572/B/13/Z (to D.L.H.). All EM was performed in the Astbury '\
        'Biostructure Laboratory, which was funded by the University of '\
        'Leeds and the Wellcome Trust (108466/Z/15/Z).'
    assert ab6.funding_text == e
    assert ab8.funding_text is None


def test_get_bibtex():
    e = '@article{Kaufmann1991FairnessPricing,\n  author = {Patrick J. '\
        'Kaufmann and Gwen Ortmeyer and N. Craig Smith},\n  title = {{'\
        'Fairness in consumer pricing}},\n  journal = {Journal of Consumer '\
        'Policy},\n  year = {1991},\n  volume = {14},\n  number = {2},\n  '\
        'pages = {117-140},\n  doi = {10.1007/BF00381915}}'
    assert ab3.get_bibtex() == e


def test_get_latex():
    e = 'Philip Hans Franses, Henk Hoekh and Richard Paap, \\textit{'\
        'Bayesian analysis of seasonal unit roots and seasonal mean shifts}, '\
        'Journal of Econometrics, \\textbf{78(2)}, pp. 359-380 (1997). \\'\
        'href{https://doi.org/10.1016/s0304-4076(97)00018-3}{doi:10.1016/'\
        's0304-4076(97)00018-3}, \\href{https://www.scopus.com/inward/'\
        'record.uri?partnerID=HzOxMe3b&scp=0000016206&origin=inward}'\
        '{scopus:2-s2.0-0000016206}.'
    assert ab4.get_latex() == e


def test_get_ris():
    e = 'TY  - JOUR\nTI  - Examples of effective data sharing in scientific '\
        'publishing\nJO  - ACS Catalysis\nVL  - 5\nDA  - 2015-06-05\nPY  - '\
        '2015\nSP  - 3894-3899\nAU  - Kitchin J.R.\nDO  - 10.1021/'\
        'acscatal.5b00538\nUR  - https://doi.org/10.1021/acscatal.5b00538\n'\
        'IS  - 6\nER  - \n\n'
    assert ab1.get_ris() == e


def test_get_html():
    e = '<a href="https://www.scopus.com/authid/detail.url?origin=Author'\
        'Profile&authorId=7201922462">Patrick J. Kaufmann</a>, <a href="'\
        'https://www.scopus.com/authid/detail.url?origin=AuthorProfile&'\
        'authorId=16430389100">Gwen Ortmeyer</a> and <a href="https://'\
        'www.scopus.com/authid/detail.url?origin=AuthorProfile&authorId='\
        '57225963896">N. Craig Smith</a>, <a href="https://www.scopus.com/'\
        'inward/record.uri?partnerID=HzOxMe3b&scp=0001270077&origin=inward">'\
        'Fairness in consumer pricing</a>, <a href="https://www.scopus.com/'\
        'source/sourceInfo.url?sourceId=130073">Journal of Consumer Policy'\
        '</a>, <b>14(2)</b>, pp. 117-140, (1991). <a href="https://doi.org/'\
        '10.1007/BF00381915">doi:10.1007/BF00381915</a>.'
    assert ab3.get_html() == e


def test_isbn():
    assert ab3.isbn is None
    assert ab5.isbn == ('0203881486', '9780203881484')
    assert ab8.isbn is None


def test_issn():
    issn = namedtuple('ISSN', 'print electronic')
    expected1 = issn(print='21555435', electronic=None)
    assert ab1.issn == expected1
    expected3 = issn(print='03425843', electronic='15730700')
    assert ab3.issn == expected3
    assert ab5.issn is None
    assert ab8.issn is None


def test_identifier():
    assert ab1.identifier == 84930616647
    assert ab8.identifier is None


def test_idxterms():
    expected = ['Control variables', 'Cost function',
                'Hamilton-Jacobi-Isaacs equation', 'Machine capacity',
                'Stochastic manufacturing systems', 'Value function']
    assert ab2.idxterms == expected
    assert ab4.idxterms is None


def test_issueIdentifier():
    assert ab1.issueIdentifier == '6'
    assert ab8.issueIdentifier is None


def test_issuetitle():
    assert ab3.issuetitle == 'Law, Economics and Behavioural Sciences'
    assert ab8.issuetitle is None


def test_language():
    assert ab1.language == 'eng'
    assert ab8.language is None


def test_openaccess():
    assert ab5.openaccess == 2
    assert ab6.openaccess == 1
    assert ab7.openaccess == 0
    assert ab8.openaccess is None


def test_openaccessFlag():
    assert ab5.openaccessFlag is None
    assert ab6.openaccessFlag == True
    assert ab7.openaccessFlag == False
    assert ab8.openaccessFlag is None


def test_pageRange():
    assert ab1.pageRange == '3894-3899'
    assert ab8.pageRange is None


def test_pii():
    assert ab4.pii == 'S0304407697000183'
    assert ab5.pii is None
    assert ab6.pii is None


def test_publicationName():
    assert ab1.publicationName == 'ACS Catalysis'
    assert ab8.publicationName is None


def test_publisher():
    assert ab1.publisher == 'American Chemical Society'
    assert ab8.publisher is None


def test_publisheraddress():
    assert ab2.publisheraddress == 'Piscataway, NJ, United States'
    assert ab8.publisheraddress is None


def test_pubmed_id():
    assert ab6.pubmed_id == 29284752
    assert ab7.pubmed_id is None


def test_refcount():
    assert ab4.refcount == 18
    assert ab8.refcount == 48
    assert ab11.refcount is None


def test_references_full():
    fields = 'position id doi title authors authors_auid authors_affiliationid '\
             'sourcetitle publicationyear coverDate volume issue first last '\
             'citedbycount type text fulltext'
    ref = namedtuple('Reference', fields)
    fulltext1 = 'Implementing Reproducible Research; Stodden, V.; Leisch, '\
                'F.; Peng, R. D., Eds., Chapman and Hall/CRC: London, 2014.'
    expected1 = ref(position='22', id='85055586929', doi=None, title=None,
        authors='Stodden, V.; Leisch, F.; Peng, R.D.', authors_auid=None,
        authors_affiliationid=None, fulltext=fulltext1, coverDate=None,
        sourcetitle='Implementing Reproducible Research', type=None,
        publicationyear='2014', volume=None, issue=None, first=None,
        last=None, citedbycount=None, text='Eds. Chapman and Hall/CRC: London.')
    expected7 = ref(position='1', id='85050215448', doi=None, title=None,
        authors='', authors_auid=None, authors_affiliationid=None,
        sourcetitle=None, publicationyear=None, coverDate=None, volume=None,
        issue=None, first=None, last=None, citedbycount=None, type=None,
        text='accessed 27 June 2017',
        fulltext='www. hexoskin. com, accessed 27 June 2017')
    assert ab1.references[-1] == expected1
    assert ab2.references is None
    assert ab7.references[0] == expected7


def test_references_ref():
    assert len(ab8.references) == 48
    fields = 'position id doi title authors authors_auid authors_affiliationid '\
             'sourcetitle publicationyear coverDate volume issue first last '\
             'citedbycount type text fulltext'
    ref = namedtuple('Reference', fields)
    expected8 = ref(position='47', id='77953310709',
        doi='10.1109/INFCOM.2010.5462174', text=None, fulltext=None,
        title='Achieving secure, scalable, and fine-grained data access control in cloud computing',
        authors='Yu, Shucheng; Lou, Wenjing; Wang, Cong; Ren, Kui',
        authors_auid='55636591800; 7006030576; 35106222100; 8396435500',
        authors_affiliationid='60011410; 60011410; 60002873; 60002873',
        sourcetitle='Proceedings - IEEE INFOCOM',
        publicationyear=None, coverDate='2010-06-15', volume=None, issue=None,
        first=None, last=None, citedbycount='0', type='resolvedReference')
    assert ab8.references[-2]._replace(citedbycount="0") == expected8
    assert int(ab8.references[-2].citedbycount) >= 0
    assert ab11.references is None


def test_scopus_link():
    expected = 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&'\
        'scp=84930616647&origin=inward'
    assert ab1.scopus_link == expected


def test_self_link():
    expected = 'https://api.elsevier.com/content/abstract/scopus_id/84930616647'
    assert ab1.self_link == expected
    assert ab8.self_link is None


def test_sequencebank():
    received = ab6.sequencebank
    assert isinstance(received, list)
    assert len(received) == 3
    bank = namedtuple('Chemical', 'name sequence_number type')
    expected = bank(name='GENBANK', sequence_number='MG272373',
                    type='referenced')
    assert expected in received
    assert ab3.sequencebank is None
    assert ab8.sequencebank is None


def test_source_id():
    assert ab1.source_id == 19700188320
    assert ab8.source_id is None


def test_sourcetitle_abbreviation():
    assert ab1.sourcetitle_abbreviation == 'ACS Catal.'
    assert ab8.sourcetitle_abbreviation is None


def test_srctype():
    assert ab1.srctype == 'j'
    assert ab2.srctype == 'p'
    assert ab8.srctype is None


def test_startingPage():
    assert ab1.startingPage == '3894'
    assert ab8.startingPage is None


def test_subject_areas():
    area = namedtuple('Area', 'area abbreviation code')
    expected = [area(area='Catalysis', abbreviation='CENG', code=1503),
                area(area='Chemistry (all)', abbreviation='CHEM', code=1600)]
    assert ab1.subject_areas == expected
    assert ab8.subject_areas is None
    expected = [area(area='Nuclear and High Energy Physics',
                     abbreviation='PHYS', code=3106)]
    assert ab9.subject_areas == expected


def test_subtype():
    assert ab1.subtype == "re"
    assert ab2.subtype == "cp"
    assert ab5.subtype == "bk"
    assert ab6.subtype == "ar"
    assert ar10.subtype is None


def test_subtypedescription():
    assert ab1.subtypedescription == "Review"
    assert ab2.subtypedescription == "Conference Paper"
    assert ab5.subtypedescription == "Book"
    assert ab6.subtypedescription == "Article"
    assert ar10.subtypedescription is None


def test_title():
    expected = 'Examples of effective data sharing in scientific publishing'
    assert ab1.title == expected
    assert ab8.title is None
    assert ar10.title is None


def test_url():
    expected = 'https://api.elsevier.com/content/abstract/scopus_id/84930616647'
    assert ab1.url == expected
    assert ab8.url is None


def test_volume():
    assert ab1.volume == '5'
    assert ab8.volume is None


def test_website():
    assert ab1.website == 'http://pubs.acs.org/page/accacs/about.html'
    assert ab2.website is None
    assert ab8.website is None
