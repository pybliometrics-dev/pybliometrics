#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.ContentAffiliationRetrieval` module."""

from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import ContentAffiliationRetrieval


aff = ContentAffiliationRetrieval('60000356', refresh=30)


def test_address():
    assert_equal(aff.address, 'Private Bag X3, Rondebosch')


def test_affiliation_name():
    assert_equal(aff.affiliation_name, 'University of Cape Town')


def test_author_count():
    expected = '10951'
    assert_true(aff.author_count >= expected)


def test_city():
    assert_equal(aff.city, 'Cape Town')


def test_country():
    assert_equal(aff.country, 'South Africa')


def test_date_created():
    assert_equal(aff.date_created, (2008, 2, 2))


def test_document_count():
    expected = '53261'
    assert_true(aff.document_count >= expected)


def test_eid():
    assert_equal(aff.eid, '10-s2.0-60000356')


def test_identifier():
    assert_equal(aff.identifier, '60000356')


def test_name_variants():
    variants = aff.name_variants
    expected = "<class 'pybliometrics.scopus.affiliation_retrieval.Variant'>"
    assert_equal(str(type(variants[0])), expected)


def test_org_domain():
    assert_equal(aff.org_domain, 'uct.ac.za')


def test_org_type():
    assert_equal(aff.org_type, 'univ')


def test_org_URL():
    assert_equal(aff.org_URL, 'http://www.uct.ac.za')


def test_postal_code():
    assert_equal(aff.postal_code, '7701')


def test_scopus_affiliation_link():
    expected = 'https://www.scopus.com/affil/profile.uri?afid=\
60000356&partnerID=HzOxMe3b&origin=inward'
    assert_equal(aff.scopus_affiliation_link, expected)


def test_self_link():
    expected = 'https://api.elsevier.com/content/affiliation/affiliation_id/60000356'
    assert_equal(aff.self_link, expected)


def test_search_link():
    expected = 'https://api.elsevier.com/content/search/scopus?query=af-id%2860000356%29'
    assert_equal(aff.search_link, expected)


def test_state():
    assert_equal(aff.state, 'Western Cape')


def sort_name():
    assert_equal(aff.sort_name, 'Cape Town, University of')


def url():
    expected = 'https://api.elsevier.com/content/affiliation/affiliation_id/60000356'
    assert_equal(aff.url, expected)
