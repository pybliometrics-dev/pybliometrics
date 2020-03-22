#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.CitationOverview` module."""

from collections import namedtuple
from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import CitationOverview


co = CitationOverview("2-s2.0-84930616647", refresh=30, start=2015, end=2018)


def test_authors():
    Author = namedtuple('Author', 'name surname initials id url')
    url = 'https://api.elsevier.com/content/author/author_id/7004212771'
    expected = [Author(name='Kitchin J.R.', surname='Kitchin',
                initials='J.R.', id='7004212771',
                url=url)]
    assert_equal(co.authors, expected)


def test_cc():
    assert_equal(co.cc, [(2015, '0'), (2016, '4'), (2017, '2'), (2018, '2')])


def test_citationType_long():
    assert_equal(co.citationType_long, 'Review')


def test_citationType_short():
    assert_equal(co.citationType_short, 're')


def test_doi():
    assert_equal(co.doi, '10.1021/acscatal.5b00538')


def test_endingPage():
    assert_equal(co.endingPage, '3899')


def test_h_index():
    assert_equal(co.h_index, '1')


def test_issn():
    assert_equal(co.issn, '2155-5435')


def test_issueIdentifier():
    assert_equal(co.issueIdentifier, '6')


def test_lcc():
    assert_true(int(co.lcc) >= 0)


def test_pcc():
    assert_equal(co.pcc, '0')


def test_pii():
    assert_equal(co.pii, None)


def test_publicationName():
    assert_equal(co.publicationName, 'ACS Catalysis')


def test_rangeCount():
    assert_true(int(co.rangeCount) >= 7)


def test_rowTotal():
    assert_true(int(co.rowTotal) >= 7)


def test_scopus_id():
    assert_equal(co.scopus_id, '84930616647')


def test_startingPage():
    assert_equal(co.startingPage, '3894')


def test_title():
    expected = 'Examples of effective data sharing in scientific publishing'
    assert_equal(co.title, expected)


def test_url():
    expected = 'https://api.elsevier.com/content/abstract/scopus_id/84930616647'
    assert_equal(co.url, expected)


def test_volume():
    assert_equal(co.volume, '5')
