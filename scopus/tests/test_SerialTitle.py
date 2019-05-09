#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `SerialTitle` module."""

from collections import namedtuple
from nose.tools import assert_equal, assert_true

import scopus

# SoftwareX
sofwarex = scopus.SerialTitle("2352-7110", refresh=False)
# ISA
isa = scopus.SerialTitle("5617-1099", refresh=False)


def test_aggregation_type():
    assert_equal(sofwarex.aggregation_type, "journal")
    assert_equal(isa.aggregation_type, "conferenceproceeding")


def test_citescoreyearinfolist():
    assert_equal(sofwarex.citescoreyearinfolist,
        [('2017', '10.13'), ('2018', '11.54')])
    assert_equal(isa.citescoreyearinfolist, None)


def test_eissn():
    assert_equal(sofwarex.eissn, "2352-7110")
    assert_equal(isa.eissn, None)


def test_issn():
    assert_equal(sofwarex.issn, None)
    assert_equal(isa.issn, "5617-1099")


def test_oaallowsauthorpaid():
    assert_equal(sofwarex.oaallowsauthorpaid, None)
    assert_equal(isa.oaallowsauthorpaid, None)


def test_openaccess():
    assert_equal(sofwarex.openaccess, '1')
    assert_equal(isa.openaccess, None)


def test_openaccessstartdate():
    assert_equal(sofwarex.openaccessstartdate, None)
    assert_equal(isa.openaccessstartdate, None)


def test_openaccesstype():
    assert_equal(sofwarex.openaccesstype, None)
    assert_equal(isa.openaccesstype, None)


def test_openaccessarticle():
    assert_equal(sofwarex.openaccessarticle, True)
    assert_equal(isa.openaccessarticle, None)


def test_openarchivearticle():
    assert_equal(sofwarex.openarchivearticle, None)
    assert_equal(isa.openarchivearticle, None)


def test_openaccesssponsorname():
    assert_equal(sofwarex.openaccesssponsorname, None)
    assert_equal(isa.openaccesssponsorname, None)


def test_openaccessuserlicense():
    assert_equal(sofwarex.openaccessuserlicense, None)
    assert_equal(isa.openaccessuserlicense, None)


def test_publisher():
    assert_equal(sofwarex.publisher, "Elsevier BV")
    assert_equal(isa.publisher, "Instrument Society of America")


def test_scopus_source_link():
    assert_equal(sofwarex.scopus_source_link,
        "https://www.scopus.com/source/sourceInfo.url?sourceId=21100422153")
    assert_equal(isa.scopus_source_link,
        "https://www.scopus.com/source/sourceInfo.url?sourceId=110387")


def test_self_link():
    assert_equal(sofwarex.self_link,
        "https://api.elsevier.com/content/serial/title/issn/23527110")
    assert_equal(isa.self_link,
        "https://api.elsevier.com/content/serial/title/issn/56171099")

def test_sjrlist():
    assert_equal(sofwarex.sjrlist, ('2017', '3.724'))
    assert_equal(isa.sjrlist, ('2006', '0.101'))


def test_sniplist():
    assert_equal(sofwarex.sniplist, ('2017', '5.022'))
    assert_equal(isa.sniplist, ('2006', '0'))


def test_source_id():
    assert_equal(sofwarex.source_id, "21100422153")
    assert_equal(isa.source_id, "110387")


def test_subject_area():
    area = namedtuple('Subjectarea', 'area abbreviation code')
    expected1 = [
        area(area='Software', abbreviation='COMP', code='1712'),
        area(area='Computer Science Applications', abbreviation='COMP', code='1706')
    ]
    assert_equal(sofwarex.subject_area, expected1)
    expected2 = [
        area(area='Instrumentation', abbreviation='PHYS', code='3105'),
        area(area='Condensed Matter Physics', abbreviation='PHYS', code='3104')
    ]
    assert_equal(isa.subject_area, expected2)


def test_title():
    assert_equal(sofwarex.title, "SoftwareX")
    assert_equal(isa.title,
        "Annual ISA Analysis Division Symposium - Proceedings")
