#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.AffiliationRetrieval` module."""

from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import AffiliationRetrieval


light = AffiliationRetrieval('60000356', refresh=30, view="LIGHT")
standard = AffiliationRetrieval('60000356', refresh=30, view="STANDARD")


def test_address():
    assert_equal(light.address, 'Private Bag X3, Rondebosch')
    assert_equal(standard.address, 'Private Bag X3, Rondebosch')


def test_affiliation_name():
    assert_equal(light.affiliation_name, 'University of Cape Town')
    assert_equal(standard.affiliation_name, 'University of Cape Town')


def test_author_count():
    expected = '12900'
    assert_true(light.author_count >= expected)
    assert_true(standard.author_count >= expected)


def test_city():
    assert_equal(light.city, 'Cape Town')
    assert_equal(standard.city, 'Cape Town')


def test_country():
    assert_equal(light.country, 'South Africa')
    assert_equal(standard.country, 'South Africa')


def test_date_created():
    assert_equal(light.date_created, None)
    assert_equal(standard.date_created, (2008, 2, 2))


def test_document_count():
    expected = '73581'
    assert_true(light.document_count >= expected)
    assert_true(standard.document_count >= expected)


def test_eid():
    assert_equal(light.eid, '10-s2.0-60000356')
    assert_equal(standard.eid, '10-s2.0-60000356')


def test_identifier():
    assert_equal(light.identifier, '60000356')
    assert_equal(standard.identifier, '60000356')


def test_name_variants():
    expected = "<class 'pybliometrics.scopus.affiliation_retrieval.Variant'>"
    assert_equal(str(type(light.name_variants[0])), expected)
    assert_equal(str(type(standard.name_variants[0])), expected)


def test_org_domain():
    assert_equal(light.org_domain, None)
    assert_equal(standard.org_domain, 'uct.ac.za')


def test_org_type():
    assert_equal(light.org_type, None)
    assert_equal(standard.org_type, 'univ')


def test_org_URL():
    assert_equal(light.org_URL, None)
    assert_equal(standard.org_URL, 'http://www.uct.ac.za')


def test_postal_code():
    assert_equal(light.postal_code, None)
    assert_equal(standard.postal_code, '7701')


def test_scopus_affiliation_link():
    expected = 'https://www.scopus.com/affil/profile.uri?afid='\
               '60000356&partnerID=HzOxMe3b&origin=inward'
    assert_equal(light.scopus_affiliation_link, expected)
    assert_equal(standard.scopus_affiliation_link, expected)


def test_self_link():
    expected = 'https://api.elsevier.com/content/affiliation/affiliation_id/60000356'
    assert_equal(light.self_link, expected)
    assert_equal(standard.self_link, expected)


def test_search_link():
    expected = 'https://api.elsevier.com/content/search/scopus?query=af-id%2860000356%29'
    assert_equal(light.search_link, expected)
    assert_equal(standard.search_link, expected)


def test_state():
    assert_equal(light.state, None)
    assert_equal(standard.state, 'Western Cape')


def sort_name():
    assert_equal(light.sort_name, None)
    assert_equal(standard.sort_name, 'Cape Town, University of')


def url():
    expected = 'https://api.elsevier.com/content/affiliation/affiliation_id/60000356'
    assert_equal(light.url, expected)
    assert_equal(standard.url, expected)
