#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `ScopusSearch` module."""

from collections import namedtuple
from nose.tools import assert_equal

import scopus


s = scopus.ScopusSearch('AU-ID(24320488600)', refresh=True)


def test_get_eids():
    assert_equal(s.get_eids(), ['2-s2.0-26444452434'])


def test_results():
    order = 'eid doi pii title subtype creator authname authid afid '\
            'coverDate coverDisplayDate publicationName issn source_id '\
            'aggregationType volume issueIdentifier pageRange citedby_count '\
            'openaccess'
    doc = namedtuple('Document', order)
    expected = doc(eid='2-s2.0-26444452434', doi='10.1016/0014-2921(92)90085-B',
        pii='001429219290085B', title='Economists as policymakers: A round-table discussion. Introduction',
        subtype='ar', creator='Draghi M.', authname='Draghi M.',
        authid='24320488600', afid=None, coverDate='1992-01-01',
        coverDisplayDate='April 1992', publicationName='European Economic Review',
        issn='00142921', source_id='20749', aggregationType='Journal',
        volume='36', issueIdentifier='2-3', pageRange='307-309',
        citedby_count='1', openaccess='0')
    assert_equal(s.results[-1], expected)
