#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `scopus.SerialSearch` module."""

from nose.tools import assert_equal

from pybliometrics.scopus import SerialSearch, SerialTitle


# A journal search by issn. Exact match, 1 result.
ser1 = SerialSearch({'issn':'1468-0262'}, refresh=30)
# Search by title displaying only publisher field (ignoring prism url and empty subject area fields).
ser2 = SerialSearch({'title':'computational', 'field':'dc:publisher'},
                    refresh=30)
# Search by subject area code. Namedtuples with at least 18 fields.
ser3  = SerialSearch({'subjCode':'2612'}, refresh=30)
# Search by subject abbreviation with specific date range for historic data.
ser4 = SerialSearch({'subj':'COMP', 'date':'2015-2015'}, refresh=30)


def test_serials():
    assert_equal(len(ser1.results), 1)
    assert_equal(ser1.results[0].dc_title, 'Econometrica')
    mirror = SerialTitle('1468-0262', refresh=30)
    assert_equal(ser1.results[0].source_id, mirror.source_id)
    expected_fields = set(['dc_publisher',
                           'prism_url',
                           'subject_area_abbrevs',
                           'subject_area_codes',
                           'subject_area_names'])
    ser2_fields = set(j for i in ser2.results for j in i._fields)
    assert_equal(ser2_fields, expected_fields)
    assert_equal(set(len(i) >= 18 for i in ser3.results), set([True]))
    ser3_subj_codes = set(i.subject_area_codes for i in ser3.results)
    assert_equal(set('2612' in i for i in ser3_subj_codes), set([True]))
    ser4_subj_abbs = set(i.subject_area_abbrevs for i in ser4.results)
    assert_equal(set('COMP' in i for i in ser4_subj_abbs), set([True]))
    ser4_sjr_fields = set(j for i in ser4.results for j in i._fields if 'SJR' in j)
    assert_equal(set(['SJR_2015']), ser4_sjr_fields)
