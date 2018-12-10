#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `AffiliationSearch` module."""

from collections import namedtuple

from nose.tools import assert_equal, assert_true

import scopus

s = scopus.AffiliationSearch('af-id(60021784)', refresh=True)


def test_affiliations():
    received = s.affiliations
    assert_true(isinstance(received, list))

    order = 'eid name variant documents city country parent'
    Affiliation = namedtuple('Affiliation', order)
    expected = [Affiliation(eid='10-s2.0-60021784', name='New York University',
                variant='', documents='100532', city='New York',
                country='United States', parent='0')]
    assert_equal(received, expected)
