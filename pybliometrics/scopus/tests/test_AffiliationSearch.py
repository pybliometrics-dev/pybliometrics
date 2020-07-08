#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.AffiliationSearch` module."""

from collections import namedtuple

from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import AffiliationSearch

s1 = AffiliationSearch('AF-ID(60021784)', refresh=30)
s2 = AffiliationSearch('AFFIL(Max Planck Munich)', download=False)


def test_affiliations():
    received1 = s1.affiliations
    assert_true(isinstance(received1, list))
    order = 'eid name variant documents city country parent'
    Affiliation = namedtuple('Affiliation', order)
    expected = Affiliation(eid='10-s2.0-60021784', name='New York University',
        variant='', documents='0', city='New York', country='United States',
        parent='0')
    assert_true(int(received1[0].documents) >= 90_000)
    assert_equal(received1[0]._replace(documents="0"), expected)


def test_affiliations_nodownload():
    assert_equal(s2.affiliations, None)


def test_get_results_size():
    received1 = s1.get_results_size()
    assert_true(received1 >= 1)
    received2 = s2.get_results_size()
    assert_true(received2 >= 80)
