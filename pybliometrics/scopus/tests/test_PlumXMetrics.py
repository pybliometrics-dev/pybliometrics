#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.PlumXMetrics` module."""

from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import PlumXMetrics

# A published paper. All PlumX Metrics categories are present.
m1 = PlumXMetrics('2-s2.0-34249753618', 'elsevierId', refresh=30)
# A published paper. No Usage and Social Media metrics.
m2 = PlumXMetrics('10.2307/2281868', 'doi', refresh=30)
# A published paper. No PlumX Metrics.
m3 = PlumXMetrics('2-s2.0-84950369844', 'elsevierId', refresh=30)
# An arXiv paper. No Citation metrics.
m4 = PlumXMetrics('1507.02672', 'arxivId', refresh=30)
# A published book. No Social Media metrics.
m5 = PlumXMetrics('9783540783893', 'isbn', refresh=30)
# A GitHub repository. No Citation metrics.
m6 = PlumXMetrics('tensorflow/tensorflow', 'githubRepoId', refresh=30)
# A YouTube video. No Capture and Citation metrics.
m7 = PlumXMetrics('dQw4w9WgXcQ', 'youtubeVideoId', refresh=30)


def test_category_totals():
    m1_received = sorted([c.name  for c in m1.category_totals])
    m1_expected = ['capture', 'citation', 'mention', 'socialMedia', 'usage']
    assert_equal(m1_received, m1_expected)
    m2_received = sorted([c.name  for c in m2.category_totals])
    m2_expected = ['capture', 'citation', 'mention']
    assert_equal(m2_received, m2_expected)
    assert_equal(m3.category_totals, None)
    m4_received = sorted([c.name  for c in m4.category_totals])
    m4_expected = ['capture', 'mention', 'socialMedia']
    assert_equal(m4_received, m4_expected)
    m6_received = sorted([c.name  for c in m6.category_totals])
    m6_expected = ['capture', 'mention', 'socialMedia', 'usage']
    assert_equal(m6_received, m6_expected)
    m7_received = sorted([c.name  for c in m7.category_totals])
    m7_expected = ['mention', 'socialMedia', 'usage']
    assert_equal(m7_received, m7_expected)
    for plumx in (m1, m2, m4, m5, m6, m7):
        m_fields = set(field for ntup in plumx.category_totals for field in ntup._fields)
        assert_equal(m_fields, {'name', 'total'})
        zero_totals = [i.total for i in plumx.category_totals if i.total <= 0]
        assert_equal(zero_totals, [])


def test_capture():
    assert_equal(m3.capture, None)
    assert_equal(m7.capture, None)
    expected = {'name', 'total'}
    for plumx in (m1, m2, m4, m5, m6):
        assert_true(isinstance(plumx.capture, list))
        assert_true(len(plumx.capture) > 0)
        m_fields = set(field for ntup in plumx.capture for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.capture if i.total <= 0] 
        assert_equal(zero_totals, [])


def test_citation():
    assert_equal(m4.citation, None)
    assert_equal(m4.citation, None)
    assert_equal(m6.citation, None)
    assert_equal(m7.citation, None)
    expected = {'name', 'total'}
    for plumx in (m1, m2, m5):
        assert_true(isinstance(plumx.citation, list))
        assert_true(len(plumx.citation) > 0)
        m_fields = set(field for ntup in plumx.citation for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.citation if i.total <= 0]
        assert_equal(zero_totals, [])


def test_mention():
    assert_equal(m3.mention, None)
    expected = {'name', 'total'}
    for plumx in (m1, m2, m4, m5, m6, m7):
        assert_true(isinstance(plumx.mention, list))
        assert_true(len(plumx.mention) > 0)
        m_fields = set(field for ntup in plumx.mention for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.mention if i.total <= 0]
        assert_equal(zero_totals, [])


def test_social_media():
    assert_equal(m2.social_media, None)
    assert_equal(m3.social_media, None)
    assert_equal(m5.social_media, None)
    expected = {'name', 'total'}
    for plumx in (m1, m4, m6, m7):
        assert_true(isinstance(plumx.social_media, list))
        assert_true(len(plumx.social_media) > 0)
        m_fields = set(field for ntup in plumx.social_media for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.social_media if i.total <= 0]
        assert_equal(zero_totals, [])


def test_usage():
    assert_equal(m2.usage, None)
    assert_equal(m3.usage, None)
    assert_equal(m4.usage, None)
    expected = {'name', 'total'}
    for plumx in (m1, m5, m6, m7):
        assert_true(isinstance(plumx.usage, list))
        assert_true(len(plumx.usage) > 0)
        m_fields = set(field for ntup in plumx.usage for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.usage if i.total <= 0]
        assert_equal(zero_totals, [])
