#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.PlumXMetrics` module."""

from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import PlumXMetrics

# All PlumX Metrics categories are present
m1 = PlumXMetrics('2-s2.0-34249753618', refresh=30)
# No Social Media metrics
m2 = PlumXMetrics('2-s2.0-84925623234', refresh=30)
# No PlumX Metrics
m3 = PlumXMetrics('2-s2.0-84950369844', refresh=30)


def test_category_totals():
    assert_true(isinstance(m1.category_totals, list))
    assert_true(isinstance(m2.category_totals, list))
    assert_equal(m3.category_totals, None)
    cats1 = [i.name for i in m1.category_totals]
    cats2 = [i.name for i in m2.category_totals]
    assert_true('socialMedia' in cats1)
    assert_true('socialMedia' not in cats2)
    assert_true(len(m1.category_totals) >= 5)
    assert_true(len(m2.category_totals) >= 4)
    expected = set(['name', 'total'])
    m1_fields = set(field for ntup in m1.category_totals for field in ntup._fields)
    m2_fields = set(field for ntup in m2.category_totals for field in ntup._fields)
    assert_equal(m1_fields, expected)
    assert_equal(m2_fields, expected)
    assert_equal([i.total for i in m1.category_totals if i.total <= 0], [])
    assert_equal([i.total for i in m2.category_totals if i.total <= 0], [])


def test_capture():
    assert_true(isinstance(m1.capture, list))
    assert_true(isinstance(m2.capture, list))
    assert_equal(m3.capture, None)
    assert_true(len(m1.capture) > 0)
    assert_true(len(m2.capture) > 0)
    expected = set(['name', 'total'])
    m1_fields = set(field for ntup in m1.capture for field in ntup._fields)
    m2_fields = set(field for ntup in m2.capture for field in ntup._fields)
    assert_equal(m1_fields, expected)
    assert_equal(m2_fields, expected)
    assert_equal([i.total for i in m1.capture if i.total <= 0], [])
    assert_equal([i.total for i in m2.capture if i.total <= 0], [])


def test_citation():
    assert_true(isinstance(m1.citation, list))
    assert_true(isinstance(m2.citation, list))
    assert_equal(m3.citation, None)
    assert_true(len(m1.citation) > 0)
    assert_true(len(m2.citation) > 0)
    expected = set(['name', 'total'])
    m1_fields = set(field for ntup in m1.citation for field in ntup._fields)
    m2_fields = set(field for ntup in m2.citation for field in ntup._fields)
    assert_equal(m1_fields, expected)
    assert_equal(m2_fields, expected)
    assert_equal([i.total for i in m1.citation if i.total <= 0], [])
    assert_equal([i.total for i in m2.citation if i.total <= 0], [])


def test_mention():
    assert_true(isinstance(m1.mention, list))
    assert_true(isinstance(m2.mention, list))
    assert_equal(m3.mention, None)
    assert_true(len(m1.mention) > 0)
    assert_true(len(m2.mention) > 0)
    expected = set(['name', 'total'])
    m1_fields = set(field for ntup in m1.mention for field in ntup._fields)
    m2_fields = set(field for ntup in m2.mention for field in ntup._fields)
    assert_equal(m1_fields, expected)
    assert_equal(m2_fields, expected)
    assert_equal([i.total for i in m1.mention if i.total <= 0], [])
    assert_equal([i.total for i in m2.mention if i.total <= 0], [])


def test_social_media():
    assert_true(isinstance(m1.social_media, list))
    assert_equal(m2.social_media, None)
    assert_equal(m3.social_media, None)
    assert_true(len(m1.social_media) > 0)
    expected = set(['name', 'total'])
    m1_fields = set(field for ntup in m1.social_media for field in ntup._fields)
    assert_equal(m1_fields, expected)
    assert_equal([i.total for i in m1.social_media if i.total <= 0], [])


def test_usage():
    assert_true(isinstance(m1.usage, list))
    assert_true(isinstance(m2.usage, list))
    assert_equal(m3.usage, None)
    assert_true(len(m1.usage) > 0)
    assert_true(len(m2.usage) > 0)
    expected = set(['name', 'total'])
    m1_fields = set(field for ntup in m1.usage for field in ntup._fields)
    m2_fields = set(field for ntup in m2.usage for field in ntup._fields)
    assert_equal(m1_fields, expected)
    assert_equal(m2_fields, expected)
    assert_equal([i.total for i in m1.usage if i.total <= 0], [])
    assert_equal([i.total for i in m2.usage if i.total <= 0], [])

