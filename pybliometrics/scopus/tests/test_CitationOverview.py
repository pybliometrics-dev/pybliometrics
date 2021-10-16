#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.CitationOverview` module."""

from collections import namedtuple
from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import CitationOverview


co_eid = CitationOverview(["85068268027", "84930616647"],
                          refresh=30, start=2016, end=2020)
co_doi = CitationOverview(["10.1016/j.softx.2019.100263"],
                          id_type="doi", refresh=30, start=2016, end=2020)

def test_authors():
    Author = namedtuple('Author', 'name surname initials id url')
    url = 'https://api.elsevier.com/content/author/author_id/7004212771'
    john = Author(name='Kitchin J.R.', surname='Kitchin',
                  initials='J.R.', id='7004212771', url=url)
    assert_equal(co_eid.authors[0][1], john)
    assert_equal(co_eid.authors[1], [john])
    assert_equal(co_doi.authors[0][1], john)


def test_cc():
    expected0 = [(2016, 0), (2017, 0), (2018, 0), (2019, 0), (2020, 6)]
    expected1 = [(2016, 4), (2017, 2), (2018, 2), (2019, 2), (2020, 2)]
    assert_equal(co_eid.cc, [expected0, expected1])
    assert_equal(co_doi.cc, [expected0])


def test_citationType_long():
    assert_equal(co_eid.citationType_long, ['Article', 'Review'])
    assert_equal(co_doi.citationType_long, ['Article'])


def test_citationType_short():
    assert_equal(co_eid.citationType_short, ['ar', 're'])
    assert_equal(co_doi.citationType_short, ['ar'])


def test_columnTotal():
    assert_equal(co_eid.columnTotal, [4, 2, 2, 2, 8])
    assert_equal(co_doi.columnTotal, [0, 0, 0, 0, 6])


def test_doi():
    expected = ['10.1016/j.softx.2019.100263', '10.1021/acscatal.5b00538']
    assert_equal(co_eid.doi, expected)
    assert_equal(co_doi.doi, [expected[0]])


def test_endingPage():
    assert_equal(co_eid.endingPage, [None, '3899'])
    assert_equal(co_doi.endingPage, None)


def test_grandTotal():
    assert_true(co_eid.grandTotal >= 29)
    assert_true(co_doi.grandTotal >= 16)


def test_h_index():
    assert_equal(co_eid.h_index, 2)
    assert_equal(co_doi.h_index, 1)


def test_issn():
    expected = ['2352-7110', '2155-5435']
    assert_equal(co_eid.issn, expected)
    assert_equal(co_doi.issn, [expected[0]])


def test_issueIdentifier():
    assert_equal(co_eid.issueIdentifier, [None, '6'])
    assert_equal(co_doi.issueIdentifier, None)


def test_laterColumnTotal():
    assert_true(co_eid.laterColumnTotal >= 18)
    assert_true(co_doi.laterColumnTotal >= 16)


def test_lcc():
    assert_true(co_eid.lcc[0] >= 1)
    assert_true(co_eid.lcc[1] >= 1)
    assert_true(co_doi.lcc[0] >= 1)


def test_pcc():
    assert_true(co_eid.pcc == [0, 0])
    assert_true(co_doi.pcc == [0])


def test_pii():
    expected = ['S2352711019300573', None]
    assert_equal(co_eid.pii, expected)
    assert_equal(co_doi.pii, [expected[0]])


def prevColumnTotal():
    assert_equal(co_eid.prevColumnTotal, 0)
    assert_equal(co_doi.prevColumnTotal, 0)


def test_publicationName():
    expected = ['SoftwareX', 'ACS Catalysis']
    assert_equal(co_eid.publicationName, expected)
    assert_equal(co_doi.publicationName, [expected[0]])


def test_rangeColumnTotal():
    assert_equal(co_eid.rangeColumnTotal, 18)
    assert_equal(co_doi.rangeColumnTotal, 6)


def test_rangeCount():
    assert_true(co_eid.rangeCount[0] >= 6)
    assert_true(co_eid.rangeCount[1] >= 6)
    assert_true(co_doi.rangeCount[0] >= 6)


def test_rowTotal():
    assert_true(co_eid.rowTotal[0] >= 10)
    assert_true(co_eid.rowTotal[1] >= 10)
    assert_true(co_doi.rowTotal[0] >= 10)


def test_scopus_id():
    expected = [85068268027, 84930616647]
    assert_equal(co_eid.scopus_id, expected)
    assert_equal(co_doi.scopus_id, [expected[0]])


def test_startingPage():
    assert_equal(co_eid.startingPage, [None, '3894'])
    assert_equal(co_doi.startingPage, None)


def test_title():
    expected = ['pybliometrics: Scriptable bibliometrics using a Python interface to Scopus',
                'Examples of effective data sharing in scientific publishing']
    assert_equal(co_eid.title, expected)
    assert_equal(co_doi.title, [expected[0]])


def test_url():
    expected = ['https://api.elsevier.com/content/abstract/scopus_id/85068268027',
                'https://api.elsevier.com/content/abstract/scopus_id/84930616647']
    assert_equal(co_eid.url, expected)
    assert_equal(co_doi.url, [expected[0]])


def test_volume():
    assert_equal(co_eid.volume, ['10', '5'])
    assert_equal(co_doi.volume, ['10'])
