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
        fund_no=None, fund_sponsor=None)
    assert int(received.citedby_count) > 0
    assert received._replace(citedby_count=0) == expected


def test_results_journal():
    received = s_j.results[104]  # Changed from 105 to 104 due to one less result
    abstract = "The aim of this paper is to empirically test the determinants "\
        "of Research Joint Ventures' (RJVs) group dynamics. We develop a "\
        "model based on learning and transaction cost theories, which "\
        "represent the benefits and costs of RJV participation, respectively. "\
        "According to our framework, firms at each period in time weigh the "\
        "benefits against the costs of being an RJV member. RJV dynamics can "\
        "then be interpreted as a consequence of this evolving trade-off over "\
        "time. We look at entry, turbulence and exit in RJVs that have been "\
        "set up under the US National Cooperative Research Act, which allows "\
        "for certain antitrust exemptions in order to stimulate firms to "\
        "co-operate in R&D. Accounting for unobserved project characteristics "\
        "and controlling for inter-RJV interactions and industry effects, the "\
        "Tobit panel regressions show the importance of group and time "\
        "features for an RJVs evolution. We further identify an average RJVs "\
        "long-term equilibrium size and assess its determining factors. Ours "\
        "is a first attempt to produce robust stylized facts about "\
        "co-operational short- and long-term dynamics, a neglected dimension "\
        "in research co-operations, but an important element in understanding "\
        "how collaborative learning works. © 2010 Elsevier B.V. All rights "\
        "reserved."
    keywords = 'Group processes | Learning | Panel data | Research alliance dynamics | Transaction costs'
    title = 'Learning dynamics in research alliances: A panel data analysis'
    expected = doc(eid='2-s2.0-79952579400', doi='10.1016/j.respol.2010.03.002',
        pii='S0048733310000752', pubmed_id=None, title=title, subtype='ar',
        subtypeDescription='Article', creator='Duso T.', afid='60002483;60000762;60022265',
        affilname='Universiteit van Amsterdam;Humboldt-Universität zu Berlin;Erasmus Universiteit Rotterdam',
        affiliation_city='Amsterdam;Berlin;Rotterdam', affiliation_country='Netherlands;Germany;Netherlands',
        author_count='3', author_names='Duso, Tomaso;Pennings, Enrico;Seldeslachts, Jo',
        author_ids='24281174200;56248433100;25226239100', author_afids='60000762;60022265;60002483',
        coverDate='2010-01-01', coverDisplayDate='July 2010',
        publicationName='Research Policy', issn='00487333', source_id='22900',
        eIssn=None, aggregationType='Journal', volume='39', issueIdentifier='6',
        article_number=None, pageRange='776-789', description=abstract,
        authkeywords=keywords, citedby_count=0, openaccess=0, freetoread=None,
        freetoreadLabel=None, fund_acr='DFG', fund_no='HPRN-CT-2002-00224',
        fund_sponsor='Deutsche Forschungsgemeinschaft')
    assert int(received.citedby_count) >= 1
    assert received._replace(citedby_count=0) == expected


def test_results_empty():
    assert s_empty.results is None


def test_results_unescape():
    assert s_d.results[0].afid.count(";") == 14
    assert '&' in s_d.results[0].affilname
