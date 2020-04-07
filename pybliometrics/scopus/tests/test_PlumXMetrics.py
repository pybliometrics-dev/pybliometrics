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
    expected = set(['name', 'total'])
    assert_equal(m3.category_totals, None)
    for plumx in (m1, m2, m4, m5, m6, m7):
        assert_true(isinstance(plumx.category_totals, list))
        cats = [i.name for i in plumx.category_totals]
        if plumx in (m2, m5):
            assert_true('socialMedia' not in cats)
        else:
            assert_true('socialMedia' in cats)
        if plumx in (m1, m2, m5):
            assert_true('citation' in cats)
        else:
            assert_true('citation' not in cats)
        if plumx != m2:
            assert_true('usage' in cats)
        else:
            assert_true('usage' not in cats)
        if plumx != m7:
            assert_true('capture' in cats)
        else:
            assert_true('capture' not in cats)
        if plumx in (m2, m7):
            assert_true(len(plumx.category_totals) >= 3)
        elif plumx in (m4, m5, m6):
            assert_true(len(plumx.category_totals) >= 4)
        else:
            assert_true(len(plumx.category_totals) >= 5)
        m_fields = set(field for ntup in plumx.category_totals for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.category_totals if i.total <= 0]
        assert_equal(zero_totals, [])


def test_capture():
    expected = set(['name', 'total'])
    for plumx in (m3, m7):
        assert_equal(plumx.capture, None)
    for plumx in (m1, m2, m4, m5, m6):
        assert_true(isinstance(plumx.capture, list))
        assert_true(len(plumx.capture) > 0)
        m_fields = set(field for ntup in plumx.capture for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.capture if i.total <= 0] 
        assert_equal(zero_totals, [])


def test_citation():
    expected = set(['name', 'total'])
    for plumx in (m3, m4, m6, m7):
        assert_equal(plumx.citation, None)
    for plumx in (m1, m2, m5):
        assert_true(isinstance(plumx.citation, list))
        assert_true(len(plumx.citation) > 0)
        m_fields = set(field for ntup in plumx.citation for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.citation if i.total <= 0]
        assert_equal(zero_totals, [])


def test_mention():
    expected = set(['name', 'total'])
    assert_equal(m3.mention, None)
    for plumx in (m1, m2, m4, m5, m6, m7):
        assert_true(isinstance(plumx.mention, list))
        assert_true(len(plumx.mention) > 0)
        m_fields = set(field for ntup in plumx.mention for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.mention if i.total <= 0]
        assert_equal(zero_totals, [])


def test_social_media():
    expected = set(['name', 'total'])
    for plumx in (m2, m3, m5):
        assert_equal(plumx.social_media, None)
    for plumx in (m1, m4, m6, m7):
        assert_true(isinstance(plumx.social_media, list))
        assert_true(len(plumx.social_media) > 0)
        m_fields = set(field for ntup in plumx.social_media for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.social_media if i.total <= 0]
        assert_equal(zero_totals, [])


def test_usage():
    expected = set(['name', 'total'])
    for plumx in (m2, m3):
        assert_equal(plumx.usage, None)
    for plumx in (m1, m4, m5, m6, m7):
        assert_true(isinstance(plumx.usage, list))
        assert_true(len(plumx.usage) > 0)
        m_fields = set(field for ntup in plumx.usage for field in ntup._fields)
        assert_equal(m_fields, expected)
        zero_totals = [i.total for i in plumx.usage if i.total <= 0]
        assert_equal(zero_totals, [])


