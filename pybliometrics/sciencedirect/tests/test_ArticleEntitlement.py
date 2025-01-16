"""Tests for sciencedirect.ArticleEntitlement"""

from pybliometrics.sciencedirect import ArticleEntitlement, init

init()

ae_1 = ArticleEntitlement('10.1016/j.reseneeco.2015.06.001', view='FULL', id_type='doi', refresh=30)
ae_2 = ArticleEntitlement('S0140988320302814', view='FULL', refresh=30)


def test_all_fields():
    """Test all propoerties of ArticleEntitlement."""
    assert ae_1.doi == '10.1016/j.reseneeco.2015.06.001'
    assert ae_1.eid == '1-s2.0-S092876551500038X'
    assert ae_1.entitled is True
    assert ae_1.identifier == 'http://dx.doi.org/10.1016/j.reseneeco.2015.06.001'
    assert ae_1.link == 'https://www.sciencedirect.com/science/article/pii/S092876551500038X'
    assert ae_1.message == 'Requestor is entitled to the requested resource'
    assert ae_1.pii == 'S0928-7655(15)00038-X'
    assert ae_1.pii_norm == 'S092876551500038X'
    assert ae_1.pubmed_id is None
    assert ae_1.scopus_id == '84935028440'
    assert ae_1.status == 'found'
    assert ae_1.url == 'https://api.elsevier.com/content/article/pii/S092876551500038X'


def test_str():
    """Test print message."""
    expected_str = 'Requestor is entitled to the requested resource with doi: 10.1016/j.eneco.2020.104941'
    assert ae_2.__str__() == expected_str
