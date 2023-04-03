#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.SerialTitle` module."""

from collections import namedtuple
from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import SerialTitle

# SoftwareX
# sofwarex = SerialTitle("2352-7110", refresh=30, years="2019-2020")
sofwarex = SerialTitle("2352-7110", refresh=30)
# OECD Economic Studies
oecd = SerialTitle("0255-0822", refresh=30)


def test_aggregation_type():
    assert_equal(sofwarex.aggregation_type, "journal")
    assert_equal(oecd.aggregation_type, "journal")


def test_citescoreyearinfolist():
    expected1 = [(2021, 4.1), (2022, 5.0)]
    assert_equal(sofwarex.citescoreyearinfolist, expected1)
    assert_equal(oecd.citescoreyearinfolist, None)


def test_eissn():
    assert_equal(sofwarex.eissn, "2352-7110")
    assert_equal(oecd.eissn, "1609-7491")


def test_issn():
    assert_equal(sofwarex.issn, None)
    assert_equal(oecd.issn, "0255-0822")


def test_oaallowsauthorpaid():
    assert_equal(sofwarex.oaallowsauthorpaid, None)
    assert_equal(oecd.oaallowsauthorpaid, None)


def test_openaccess():
    assert_equal(sofwarex.openaccess, 1)
    assert_equal(oecd.openaccess, None)


def test_openaccessstartdate():
    assert_equal(sofwarex.openaccessstartdate, None)
    assert_equal(oecd.openaccessstartdate, None)


def test_openaccesstype():
    assert_equal(sofwarex.openaccesstype, None)
    assert_equal(oecd.openaccesstype, None)


def test_openaccessarticle():
    assert_equal(sofwarex.openaccessarticle, True)
    assert_equal(oecd.openaccessarticle, None)


def test_openarchivearticle():
    assert_equal(sofwarex.openarchivearticle, None)
    assert_equal(oecd.openarchivearticle, None)


def test_openaccesssponsorname():
    assert_equal(sofwarex.openaccesssponsorname, None)
    assert_equal(oecd.openaccesssponsorname, None)


def test_openaccessuserlicense():
    assert_equal(sofwarex.openaccessuserlicense, None)
    assert_equal(oecd.openaccessuserlicense, None)


def test_publisher():
    assert_equal(sofwarex.publisher, "Elsevier BV")
    assert_equal(oecd.publisher, "OECD")


def test_scopus_source_link():
    expected1 = "https://www.scopus.com/source/sourceInfo.url?sourceId=21100422153"
    assert_equal(sofwarex.scopus_source_link, expected1)
    expected2 = "https://www.scopus.com/source/sourceInfo.url?sourceId=24107"
    assert_equal(oecd.scopus_source_link, expected2)


def test_self_link():
    expected1 = "https://api.elsevier.com/content/serial/title/issn/23527110"
    assert_equal(sofwarex.self_link, expected1)
    expected2 = "https://api.elsevier.com/content/serial/title/issn/02550822"
    assert_equal(oecd.self_link, expected2)

def test_sjrlist():
    assert_equal(sofwarex.sjrlist, [(2021, 0.644)])
    assert_equal(oecd.sjrlist, [(1999, 2.723)])


def test_sniplist():
    assert_equal(sofwarex.sniplist, [(2021, 1.458)])
    assert_equal(oecd.sniplist, None)


def test_source_id():
    assert_equal(sofwarex.source_id, 21100422153)
    assert_equal(oecd.source_id, 24107)


def test_subject_area():
    area = namedtuple('Subjectarea', 'area abbreviation code')
    expected1 = [
        area(area='Computer Science Applications', abbreviation='COMP', code=1706),
        area(area='Software', abbreviation='COMP', code=1712)
    ]
    assert_equal(sofwarex.subject_area, expected1)
    expected2 = [
        area(area='Geography, Planning and Development', abbreviation='SOCI', code=3305)
    ]
    assert_equal(oecd.subject_area, expected2)


def test_title():
    assert_equal(sofwarex.title, "SoftwareX")
    assert_equal(oecd.title, "OECD Economic Studies")


def test_yearly_data():
    assert_true(type(sofwarex.yearly_data) == list)
    assert_equal(len(sofwarex.yearly_data), 28)
    fields = 'year publicationcount revpercent zerocitessce '\
             'zerocitespercentsce citecountsce'
    dat = namedtuple('Yearlydata', fields)
    expected1_2020 = dat(year=2020, publicationcount=163, revpercent=0.0,
        zerocitessce=16, zerocitespercentsce=9.815950920245398774,
        citecountsce=2554)
    assert_equal(sofwarex.yearly_data[24], expected1_2020)
    expected2_1996 = dat(year=1996, publicationcount=4, revpercent=0.0,
        zerocitessce=0, zerocitespercentsce=0, citecountsce=33)
    assert_equal(oecd.yearly_data[0], expected2_1996)
