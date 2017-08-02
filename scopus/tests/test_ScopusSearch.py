#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `ScopusSearch` module."""

from nose.tools import assert_equal

import scopus


s = scopus.ScopusSearch('AU-ID(24320488600)', refresh=True)


def test_EIDS():
    assert_equal(s.EIDS, ['2-s2.0-26444452434'])


def test_org_summary():
    expected = '1. [[https://www.scopus.com/inward/record.uri?partnerID=\
HzOxMe3b&scp=26444452434&origin=inward][2-s2.0-26444452434]]  Mario Draghi, \
Economists as policymakers: A round-table discussion. Introduction, European \
Economic Review, 36(2-3), p. 307-309, (1992). http://dx.doi.org/None, \
https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=26444452434&\
origin=inward, cited 1 times (Scopus).\n  Affiliations:\n   \n'
    assert_equal(s.org_summary, expected)
