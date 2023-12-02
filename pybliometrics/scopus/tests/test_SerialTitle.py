#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.SerialTitle` module."""

import datetime

from collections import namedtuple
from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import SerialTitle


# SoftwareX
# softwarex = SerialTitle("2352-7110", refresh=30, years="2019-2020")
softwarex = SerialTitle("2352-7110", refresh=30)
# OECD Economic Studies
oecd = SerialTitle("0255-0822", refresh=30)
# Neural Networks
neural_networks = SerialTitle('1879-2782', view='CITESCORE')


def test_aggregation_type():
    assert_equal(softwarex.aggregation_type, "journal")
    assert_equal(oecd.aggregation_type, "journal")


def test_citescoreyearinfolist():
    info_fields = 'year citescore'
    info = namedtuple('Citescoreinfolist', info_fields)

    # Test softwarex
    expected_named_tuple = [info(year=2022, citescore=5.1),
                            info(year=2023, citescore=4.9)]
    assert_equal(softwarex.citescoreyearinfolist, expected_named_tuple)

    # Test oecd
    assert_equal(oecd.citescoreyearinfolist[0], None)
    assert_equal(oecd.citescoreyearinfolist[1], None)

    # Test CITESCORE view
    this_year = datetime.date.today().year
    assert_equal(neural_networks.citescoreyearinfolist[0].year, this_year)
    assert_true(type(neural_networks.citescoreyearinfolist[3].citationcount) is int)


def test_eissn():
    assert_equal(softwarex.eissn, "2352-7110")
    assert_equal(oecd.eissn, "1609-7491")


def test_issn():
    assert_equal(softwarex.issn, None)
    assert_equal(oecd.issn, "0255-0822")


def test_oaallowsauthorpaid():
    assert_equal(softwarex.oaallowsauthorpaid, None)
    assert_equal(oecd.oaallowsauthorpaid, None)


def test_openaccess():
    assert_equal(softwarex.openaccess, 1)
    assert_equal(oecd.openaccess, None)


def test_openaccessstartdate():
    assert_equal(softwarex.openaccessstartdate, None)
    assert_equal(oecd.openaccessstartdate, None)


def test_openaccesstype():
    assert_equal(softwarex.openaccesstype, None)
    assert_equal(oecd.openaccesstype, None)


def test_openaccessarticle():
    assert_equal(softwarex.openaccessarticle, True)
    assert_equal(oecd.openaccessarticle, None)


def test_openarchivearticle():
    assert_equal(softwarex.openarchivearticle, None)
    assert_equal(oecd.openarchivearticle, None)


def test_openaccesssponsorname():
    assert_equal(softwarex.openaccesssponsorname, None)
    assert_equal(oecd.openaccesssponsorname, None)


def test_openaccessuserlicense():
    assert_equal(softwarex.openaccessuserlicense, None)
    assert_equal(oecd.openaccessuserlicense, None)


def test_publisher():
    assert_equal(softwarex.publisher, "Elsevier BV")
    assert_equal(oecd.publisher, "OECD")


def test_scopus_source_link():
    expected1 = "https://www.scopus.com/source/sourceInfo.url?sourceId=21100422153"
    assert_equal(softwarex.scopus_source_link, expected1)
    expected2 = "https://www.scopus.com/source/sourceInfo.url?sourceId=24107"
    assert_equal(oecd.scopus_source_link, expected2)


def test_self_link():
    expected1 = "https://api.elsevier.com/content/serial/title/issn/23527110"
    assert_equal(softwarex.self_link, expected1)
    expected2 = "https://api.elsevier.com/content/serial/title/issn/02550822"
    assert_equal(oecd.self_link, expected2)


def test_sjrlist():
    assert_equal(softwarex.sjrlist, [(2022, 0.574)])
    assert_equal(oecd.sjrlist, [(1999, 2.723)])


def test_sniplist():
    assert_equal(softwarex.sniplist, [(2022, 1.426)])
    assert_equal(oecd.sniplist, None)


def test_source_id():
    assert_equal(softwarex.source_id, 21100422153)
    assert_equal(oecd.source_id, 24107)


def test_subject_area():
    area = namedtuple('Subjectarea', 'area abbreviation code')
    expected1 = [
        area(area='Software', abbreviation='COMP', code=1712),
        area(area='Computer Science Applications', abbreviation='COMP', code=1706)
    ]
    assert_equal(softwarex.subject_area, expected1)
    expected2 = [
        area(area='Geography, Planning and Development', abbreviation='SOCI', code=3305)
    ]
    assert_equal(oecd.subject_area, expected2)


def test_title():
    assert_equal(softwarex.title, "SoftwareX")
    assert_equal(oecd.title, "OECD Economic Studies")


def test_yearly_data():
    assert_true(type(softwarex.yearly_data) == list)
    assert_equal(len(softwarex.yearly_data), 28)
    fields = 'year publicationcount revpercent zerocitessce '\
             'zerocitespercentsce citecountsce'
    dat = namedtuple('Yearlydata', fields)
    expected1_2020 = dat(year=2020, publicationcount=164, revpercent=0.0,
        zerocitessce=10, zerocitespercentsce=6.097560975609756,
        citecountsce=2571)
    assert_equal(softwarex.yearly_data[24], expected1_2020)
    expected2_1996 = dat(year=1996, publicationcount=4, revpercent=0.0,
        zerocitessce=0, zerocitespercentsce=0, citecountsce=33)
    assert_equal(oecd.yearly_data[0], expected2_1996)
