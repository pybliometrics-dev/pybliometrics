#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `ScopusAffiliation` module."""

from nose.tools import assert_equal, assert_true

import scopus


aff = scopus.ScopusAffiliation('60000356', refresh=True)


def test_address():
    assert_equal(aff.address, 'Private Bag X3')


def test_affiliation_id():
    assert_equal(aff.affiliation_id, '60000356')


def test_city():
    assert_equal(aff.city, 'Cape Town')


def test_country():
    assert_equal(aff.country, 'South Africa')


def test_date_created():
    assert_equal(aff.date_created, (2008, 2, 2))


def test_name():
    assert_equal(aff.name, 'University of Cape Town')


def test_nauthors():
    expected = '10473'
    assert_true(aff.nauthors >= expected)


def test_ndocuments():
    expected = '47841'
    assert_true(aff.ndocuments >= expected)


def test_org_type():
    assert_equal(aff.org_type, 'univ')


def test_org_domain():
    assert_equal(aff.org_domain, 'uct.ac.za')


def test_org_url():
    assert_equal(aff.org_url, 'http://www.uct.ac.za')


def test_state():
    assert_equal(aff.state, None)


def test_url():
    expected = 'https://www.scopus.com/affil/profile.uri?afid=\
60000356&partnerID=HzOxMe3b&origin=inward'
    assert_equal(aff.url, expected)
