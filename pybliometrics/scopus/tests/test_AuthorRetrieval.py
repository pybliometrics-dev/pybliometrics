"""Tests for `scopus.AuthorRetrieval` module."""

from collections import Counter, namedtuple

from pybliometrics.scopus import AuthorRetrieval, init

init()

metrics = AuthorRetrieval("7004212771", refresh=30, view="METRICS")
light = AuthorRetrieval("7004212771", refresh=30, view="LIGHT")
standard = AuthorRetrieval("7004212771", refresh=30, view="STANDARD")
enhanced = AuthorRetrieval("7004212771", refresh=30, view="ENHANCED")
entitled = AuthorRetrieval(36009348900, view='ENTITLED')


def test_affiliation_current():
    assert metrics.affiliation_current is None

    order = 'id parent type relationship afdispname preferred_name '\
            'parent_preferred_name country_code country address_part city '\
            'state postal_code org_domain org_URL'
    aff = namedtuple('Affiliation', order, defaults=(None,) * len(order.split()))

    expected_std_enh = aff(id=60027950, parent=None, type='parent',
        relationship='author', afdispname=None, preferred_name='Carnegie Mellon University',
        parent_preferred_name=None, country_code='usa', country='United States',
        address_part='5000 Forbes Avenue', city='Pittsburgh', state='PA',
        postal_code='15213-3890', org_domain='cmu.edu', org_URL='https://www.cmu.edu/')

    expected_lgh = aff(id=None, parent=None, type=None,
        relationship=None, afdispname=None, preferred_name='Carnegie Mellon University',
        parent_preferred_name=None, country_code=None, country='United States',
        address_part=None, city='Pittsburgh', state=None,
        postal_code=None, org_domain=None, org_URL=None)

    for a in (standard, enhanced, light):
        received = a.affiliation_current
        assert isinstance(received, list)
        assert len(received) >= 1

    for a in (standard, enhanced):
        received = a.affiliation_current
        assert expected_std_enh in received

    assert expected_lgh in light.affiliation_current


def test_affiliation_history():
    assert metrics.affiliation_history is None
    assert light.affiliation_history is None
    order = 'id parent type relationship afdispname preferred_name '\
            'parent_preferred_name country_code country address_part city '\
            'state postal_code org_domain org_URL'
    aff = namedtuple('Affiliation', order)
    expected = aff(id=60008644, parent=None, type='parent',
        relationship='author', afdispname=None,
        preferred_name='Fritz Haber Institute of the Max Planck Society',
        parent_preferred_name=None, country_code='deu', country='Germany',
        address_part='Faradayweg 4-6', city='Berlin', state=None,
        postal_code='14195', org_domain='fhi.mpg.de',
        org_URL='https://www.fhi.mpg.de/')
    for a in (standard, enhanced):
        received = a.affiliation_history
        assert isinstance(received, list)
        assert len(received) >= 10
        assert expected in received


def test_alias():
    assert metrics.alias is None
    assert light.alias is None
    assert standard.alias is None
    assert enhanced.alias is None


def test_citation_count():
    expected = 13600
    assert metrics.citation_count >= expected
    assert light.citation_count >= expected
    assert standard.citation_count >= expected
    assert enhanced.citation_count >= expected


def test_cited_by_count():
    expected = 10900
    assert metrics.cited_by_count >= expected
    assert light.cited_by_count >= expected
    assert standard.cited_by_count >= expected
    assert enhanced.cited_by_count >= expected


def test_classificationgroup():
    assert metrics.classificationgroup is None
    assert light.classificationgroup is None
    for a in (standard, enhanced):
        received = a.classificationgroup
        assert isinstance(received, list)
        assert len(received) > 0
        assert (1906, 1) in received  # frequency might differ


def test_coauthor_count():
    assert light.coauthor_count is None
    assert standard.coauthor_count is None
    expected = 175
    assert metrics.coauthor_count >= expected
    assert enhanced.coauthor_count >= expected


def test_coauthor_link():
    assert metrics.coauthor_link is None
    assert light.coauthor_link is None
    assert standard.coauthor_link is None
    expected = 'http://api.elsevier.com/content/search/author?co-author=7004212771'
    assert enhanced.coauthor_link == expected


def test_date_created():
    assert metrics.date_created is None
    assert light.date_created is None
    assert standard.date_created, (2005, 12, 3)
    assert enhanced.date_created, (2005, 12, 3)


def test_document_count():
    expected = 106
    assert light.document_count >= expected
    assert standard.document_count >= expected
    assert metrics.document_count >= expected
    assert enhanced.document_count >= expected


def test_eid():
    assert metrics.eid is None
    assert light.eid, '9-s2.0-7004212771'
    assert standard.eid, '9-s2.0-7004212771'
    assert enhanced.eid, '9-s2.0-7004212771'


def test_estimate_uniqueness():
    assert metrics.estimate_uniqueness() == 2
    assert light.estimate_uniqueness() == 2
    assert standard.estimate_uniqueness() == 1
    assert enhanced.estimate_uniqueness() == 1


def test_entitlement():
    assert metrics.document_entitlement_status is None
    assert light.document_entitlement_status is None
    assert standard.document_entitlement_status is None
    assert enhanced.document_entitlement_status is None
    assert entitled.document_entitlement_status == 'ENTITLED'


def test_given_name():
    assert metrics.given_name is None
    assert light.given_name is None
    assert standard.given_name == 'John R.'
    assert enhanced.given_name == 'John R.'


def get_coauthors():
    assert metrics.get_coauthors() is None
    assert light.get_coauthors() is None
    assert standard.get_coauthors() is None
    received = enhanced.get_coauthors()
    assert isinstance(received, list)
    assert len(received) > 155
    fields = 'surname given_name id areas affiliation_id name city country'
    coauth = namedtuple('Coauthor', fields)
    expected = coauth(surname='Rose', given_name='Michael E.', id=57209617104,
        areas='Computer Science (all)', affiliation_id=60105007,
        name='Max-Planck-Institut für Innovation und Wettbewerb',
        city='Munich', country='Germany')
    assert expected in received


def test_get_documents():
    subtypes = {'re', 'ed', 'no'}
    received = enhanced.get_documents(subtypes)
    assert len(received) == 8


def test_get_document_eids():
    expected = 100
    assert len(enhanced.get_document_eids()) >= expected


def test_h_index():
    assert light.h_index is None
    assert standard.h_index is None
    expected = 34
    assert metrics.h_index >= expected
    assert enhanced.h_index >= expected
    assert entitled.h_index is None


def test_historical_identifier():
    assert metrics.historical_identifier is None
    assert light.historical_identifier is None
    assert standard.historical_identifier is None
    expected = [35787230500, 36488127000, 54974425600, 55004143700,
                55004143800, 57057263700, 56641032000, 36747787600,
                57206217299, 57219840256, 58343886400]
    assert enhanced.historical_identifier == expected


def test_identifier():
    expected = 7004212771
    assert metrics.identifier == expected
    assert light.identifier == expected
    assert standard.identifier == expected
    assert enhanced.identifier == expected


def test_indexed_name():
    assert metrics.indexed_name is None
    assert light.indexed_name, 'Kitchin J.'
    assert standard.indexed_name, 'Kitchin J.'
    assert enhanced.indexed_name, 'Kitchin J.'


def test_initials():
    assert metrics.initials is None
    assert light.initials is None
    assert standard.initials, 'J.R.'
    assert enhanced.initials, 'J.R.'


def test_name_variants():
    assert metrics.name_variants is None
    assert light.name_variants is None
    expected = "<class 'pybliometrics.scopus.author_retrieval.Variant'>"
    for a in (standard, enhanced):
        received = a.name_variants
        assert isinstance(received, list)
        assert len(received) > 0
        assert str(type(received[0])) == expected
        assert isinstance(received[0].doc_count, int)


def test_orcid():
    assert metrics.orcid is None
    assert light.orcid, '0000-0003-2625-9232'
    assert standard.orcid, '0000-0003-2625-9232'
    assert enhanced.orcid, '0000-0003-2625-9232'


def test_publication_range():
    assert metrics.publication_range is None
    for a in (standard, enhanced, light):
        assert a.publication_range[0], 1995
        assert a.publication_range[1] >= 2021


def test_scopus_author_link():
    assert metrics.scopus_author_link is None
    expected = 'http://api.elsevier.com/content/author/author_id/7004212771'
    assert light.scopus_author_link == expected
    assert standard.scopus_author_link == expected
    assert enhanced.scopus_author_link == expected


def test_search_link():
    assert metrics.search_link is None
    expected = 'http://api.elsevier.com/content/search/scopus?query='\
               'au-id%287004212771%29'
    assert light.search_link == expected
    assert standard.search_link == expected
    assert enhanced.search_link == expected


def test_self_link():
    assert metrics.self_link is None
    expected = 'https://www.scopus.com/authid/detail.uri?partnerID=HzOxMe3b&'\
               'authorId=7004212771&origin=inward'
    assert light.self_link == expected
    assert standard.self_link == expected
    assert enhanced.self_link == expected


def test_status():
    assert metrics.status is None
    assert light.status is None
    expected = "update"
    assert standard.status == expected
    assert enhanced.status == expected


def test_subject_areas():
    assert metrics.subject_areas is None
    assert light.subject_areas is None
    expected = "<class 'pybliometrics.scopus.author_retrieval.Subjectarea'>"
    for a in (standard, enhanced):
        received = a.subject_areas
        assert isinstance(received, list)
        assert len(received) > 0
        assert str(type(received[0])) == expected


def test_surname():
    assert metrics.surname is None
    assert light.surname is None
    assert standard.surname, 'Kitchin'
    assert enhanced.surname, 'Kitchin'


def test_url():
    expected = 'http://api.elsevier.com/content/author/author_id/7004212771'
    assert metrics.url == expected
    assert light.url == expected
    assert standard.url == expected
    assert enhanced.url == expected
