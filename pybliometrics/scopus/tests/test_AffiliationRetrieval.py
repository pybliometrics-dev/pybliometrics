"""Tests for `scopus.AffiliationRetrieval` module."""

from pybliometrics.scopus import AffiliationRetrieval, init

init()


light = AffiliationRetrieval('60000356', refresh=30, view="LIGHT")
standard = AffiliationRetrieval('60000356', refresh=30, view="STANDARD")
entitled = AffiliationRetrieval('60000356', refresh=30, view='ENTITLED')


def test_address():
    assert light.address == 'Private Bag X3'
    assert standard.address == 'Private Bag X3'
    assert entitled.address is None


def test_affiliation_name():
    assert light.affiliation_name == 'University of Cape Town'
    assert standard.affiliation_name == 'University of Cape Town'
    assert entitled.affiliation_name is None


def test_author_count():
    expected = 12800
    assert light.author_count >= expected
    assert standard.author_count >= expected
    assert entitled.author_count is None


def test_city():
    assert light.city == 'Cape Town'
    assert standard.city == 'Cape Town'
    assert entitled.city is None


def test_country():
    assert light.country == 'South Africa'
    assert standard.country == 'South Africa'
    assert entitled.country is None


def test_date_created():
    assert light.date_created is None
    assert standard.date_created == (2008, 2, 2)
    assert entitled.date_created is None


def test_document_count():
    expected = 73581
    assert light.document_count >= expected
    assert standard.document_count >= expected
    assert entitled.document_count is None


def test_eid():
    assert light.eid == '10-s2.0-60000356'
    assert standard.eid == '10-s2.0-60000356'
    assert entitled.eid is None


def test_entitlement():
    assert standard.document_entitlement_status is None
    assert light.document_entitlement_status is None
    assert entitled.document_entitlement_status == 'ENTITLED'


def test_identifier():
    assert light.identifier == 60000356
    assert standard.identifier == 60000356
    assert entitled.identifier is None


def test_name_variants():
    expected = "<class 'pybliometrics.scopus.affiliation_retrieval.Variant'>"
    assert str(type(light.name_variants[0])) == expected
    assert str(type(standard.name_variants[0])) == expected
    assert entitled.name_variants is None


def test_org_domain():
    assert light.org_domain is None
    assert standard.org_domain == 'uct.ac.za'
    assert entitled.org_domain is None


def test_org_type():
    assert light.org_type is None
    assert standard.org_type == 'univ'
    assert entitled.org_type is None


def test_org_URL():
    assert light.org_URL is None
    assert standard.org_URL == 'http://www.uct.ac.za'
    assert entitled.org_URL is None


def test_postal_code():
    assert light.postal_code is None
    assert standard.postal_code == '7701'
    assert entitled.postal_code is None


def test_scopus_affiliation_link():
    expected = 'https://www.scopus.com/affil/profile.uri?afid='\
               '60000356&partnerID=HzOxMe3b&origin=inward'
    assert light.scopus_affiliation_link == expected
    assert standard.scopus_affiliation_link == expected
    assert entitled.scopus_affiliation_link is None


def test_self_link():
    expected = 'https://api.elsevier.com/content/affiliation/affiliation_id/60000356'
    assert light.self_link == expected
    assert standard.self_link == expected
    assert entitled.self_link is None


def test_search_link():
    expected = 'https://api.elsevier.com/content/search/scopus?query=af-id%2860000356%29'
    assert light.search_link== expected
    assert standard.search_link== expected
    assert entitled.search_link is None


def test_state():
    assert light.state is None
    assert standard.state == 'Western Cape'
    assert entitled.state is None


def test_status():
    assert light.status is None
    assert standard.status == "update"
    assert entitled.status is None


def sort_name():
    assert light.sort_name is None
    assert standard.sort_name== 'Cape Town, University of'
    assert entitled.sort_name is None


def url():
    expected = 'https://api.elsevier.com/content/affiliation/affiliation_id/60000356'
    assert light.url== expected
    assert standard.url== expected
    assert entitled.url is None
