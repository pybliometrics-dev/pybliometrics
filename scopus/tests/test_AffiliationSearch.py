#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `AffiliationSearch` module."""

from collections import namedtuple

from nose.tools import assert_equal, assert_true, raises

import scopus

s1 = scopus.AffiliationSearch('af-id(60021784)', refresh=True)
s2 = scopus.AffiliationSearch('affil(Max Planck Munich)',
                              refresh=False, download=False)


def test_affiliations():
    received1 = s1.affiliations
    assert_true(isinstance(received1, list))
    order = 'eid name variant documents city country parent'
    Affiliation = namedtuple('Affiliation', order)
    expected = Affiliation(eid='10-s2.0-60021784', name='New York University',
        variant='', documents='0', city='New York', country='United States',
        parent='0')
    assert_true(int(received1[0].documents) >= 101148)
    assert_equal(received1[0]._replace(documents="0"), expected)


@raises(AttributeError)
def test_affiliations_error():
    received2 = s2.affiliations


def test_get_results_size():
    received1 = s1.get_results_size()
    assert_true(received1 >= 1)
    received2 = s2.get_results_size()
    assert_true(received2 >= 100)
