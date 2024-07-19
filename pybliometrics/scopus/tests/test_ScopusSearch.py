"""Tests for `scopus.ScopusSearch` module."""

from collections import namedtuple

from pybliometrics.scopus import ScopusSearch, init

init()

order = 'eid doi pii pubmed_id title subtype subtypeDescription creator '\
        'afid affilname  affiliation_city affiliation_country author_count '\
        'author_names author_ids author_afids coverDate coverDisplayDate '\
        'publicationName issn source_id eIssn aggregationType volume '\
        'issueIdentifier article_number pageRange description authkeywords '\
        'citedby_count openaccess freetoread freetoreadLabel fund_acr '\
        'fund_no fund_sponsor'
doc = namedtuple('Document', order)

# Set to refresh=False because of citation count
s_au = ScopusSearch('AU-ID(24320488600)', unescape=False, refresh=30)
s_j = ScopusSearch('SOURCE-ID(22900) AND PUBYEAR IS 2010', unescape=True, refresh=30)
s_d = ScopusSearch("DOI(10.1038/s41556-022-01034-3)", unescape=False, refresh=30)
q_empty = 'SOURCE-ID(19700188323) AND PUBYEAR IS 1900'
s_empty = ScopusSearch(q_empty, unescape=False, refresh=30)


def test_get_eids_author():
    expected = ['2-s2.0-85193728453', '2-s2.0-85117005558',
                '2-s2.0-84937325266', '2-s2.0-26444452434']
    assert s_au.get_eids() == expected


def test_get_eids_journal():
    assert len(s_j.get_eids()) == 118


def test_get_results_size():
    assert s_au.get_results_size() == 4
    assert s_j.get_results_size() == 118
    assert s_empty.get_results_size() == 0


def test_results_author():
    received = s_au.results[-1]
    expected = doc(eid='2-s2.0-26444452434', doi='10.1016/0014-2921(92)90085-B',
        pii='001429219290085B', pubmed_id=None,
        title='Economists as policymakers: A round-table discussion. Introduction',
        subtype='ar', subtypeDescription='Article', creator='Draghi M.',
        afid=None, affilname=None, affiliation_city=None, affiliation_country=None,
        author_count='1', author_names='Draghi, Mario', author_ids='24320488600',
        author_afids=None, coverDate='1992-01-01', coverDisplayDate='April 1992',
        publicationName='European Economic Review', issn='00142921',
        source_id='20749', eIssn=None, aggregationType='Journal', volume='36',
        issueIdentifier='2-3', article_number=None, pageRange='307-309',
        description=None, authkeywords=None, citedby_count=0, openaccess=0,
        freetoread=None, freetoreadLabel=None, fund_acr=None,
        fund_no='undefined', fund_sponsor=None)
    assert int(received.citedby_count) > 0
    assert received._replace(citedby_count=0) == expected


def test_results_journal():
    received = s_j.results[-1]
    abstract = 'This paper investigates the determinants of R&D investment '\
        'at the national level with an emphasis on the roles of patent '\
        'rights protection, international technology transfer through trade '\
        'and FDI, and economic growth, in addition to the essentials of '\
        'human capital accumulation and the number of scientific '\
        'researchers. The Extreme-Bounds-Analysis (EBA) approach is applied '\
        'to examine the robustness and sensitivity of these factors. The '\
        'results of the EBA tests on data from 26 OECD countries from 1996 '\
        'to 2006 showed that tertiary education and the proportion of '\
        'scientific researchers in a country were robust determinants that '\
        'had positive effects on R&D intensity. Foreign technology inflows '\
        'had a robust and negative impact on domestic R&D. Patent rights '\
        'protection and the income growth rate are fragile determinants of '\
        'R&D investment. © 2009 Elsevier B.V. All rights reserved.'
    keywords = 'Extreme-Bounds-Analysis (EBA) | Patent rights protection | '\
        'R&D investment | Technology transfer'
    title = 'Determinants of R&D investment: The Extreme-Bounds-'\
            'Analysis approach applied to 26 OECD countries'
    expected = doc(eid='2-s2.0-74249121335', doi='10.1016/j.respol.2009.11.010',
        pii='S0048733309002145', pubmed_id=None, title=title, subtype='ar',
        subtypeDescription='Article', creator='Wang E.', afid='60007954',
        affilname='National Chung Cheng University',
        affiliation_city='Min-Hsiung', affiliation_country='Taiwan',
        author_count='1', author_names='Wang, Eric C.',
        author_ids='7403414138', author_afids='60007954',
        coverDate='2010-01-01', coverDisplayDate='2010',
        publicationName='Research Policy', issn='00487333', source_id='22900',
        eIssn=None, aggregationType='Journal', volume='39', issueIdentifier='1',
        article_number=None, pageRange='103-116', description=abstract,
        authkeywords=keywords, citedby_count=0, openaccess=0, freetoread=None,
        freetoreadLabel=None, fund_acr='MOST', fund_no='NSC94-2415-H-194-001',
        fund_sponsor='Ministry of Science and Technology, Taiwan')
    assert int(received.citedby_count) > 60
    assert received._replace(citedby_count=0) == expected


def test_results_empty():
    assert s_empty.results is None


def test_results_unescape():
    assert s_d.results[0].afid.count(";") == 14
    assert '&amp;' in s_d.results[0].affilname
