#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `ScopusSearch` module."""

from collections import namedtuple
from nose.tools import assert_equal

import scopus


order = 'eid doi pii title subtype creator authname authid afid coverDate '\
        'coverDisplayDate publicationName issn source_id aggregationType '\
        'volume issueIdentifier pageRange citedby_count openaccess'
doc = namedtuple('Document', order)

s_au = scopus.ScopusSearch('AU-ID(24320488600)', refresh=False)
s_j = scopus.ScopusSearch('SOURCE-ID(22900) AND PUBYEAR IS 2010', refresh=False)


def test_get_eids_author():
    assert_equal(s_au.get_eids(), ['2-s2.0-26444452434'])


def test_get_eids_journal():
    assert_equal(len(s_j.get_eids()), 118)


def test_results_author():
    expected = doc(eid='2-s2.0-26444452434', doi='10.1016/0014-2921(92)90085-B',
        pii='001429219290085B', title='Economists as policymakers: A round-table discussion. Introduction',
        subtype='ar', creator='Draghi M.', authname='Draghi M.',
        authid='24320488600', afid=None, coverDate='1992-01-01',
        coverDisplayDate='April 1992', publicationName='European Economic Review',
        issn='00142921', source_id='20749', aggregationType='Journal',
        volume='36', issueIdentifier='2-3', pageRange='307-309',
        citedby_count='1', openaccess='0')
    assert_equal(s_au.results[-1], expected)


def test_results_journal():
    expected = doc(eid='2-s2.0-77955426868', doi='10.1016/j.respol.2010.05.009',
        pii='S0048733310001332', title='Technology policy and global warming: Why new innovation models are needed',
        subtype='le', creator='Hargadon A.', authname=None, authid=None,
        afid=None, coverDate='2010-01-01', coverDisplayDate='October 2010',
        publicationName='Research Policy', issn='00487333', source_id='22900',
        aggregationType='Journal', volume='39', issueIdentifier='8',
        pageRange='1024-1026', citedby_count='14', openaccess='0')
    assert_equal(s_j.results[-1], expected)
