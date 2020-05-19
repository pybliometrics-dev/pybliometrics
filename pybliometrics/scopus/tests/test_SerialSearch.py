#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `scopus.SerialSearch` module."""

from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import SerialSearch


# Search by ISSN
ser1 = SerialSearch({'issn':'1468-0262'}, refresh=30)
# Search by title displaying only publisher field
ser2 = SerialSearch({'title':'computational', 'field':'dc:publisher'},
                    refresh=30)
# Search by subject area code
ser3  = SerialSearch({'subjCode':'2612'}, refresh=30)
# Search by subject abbreviation with specific date range for historic data
ser4 = SerialSearch({'subj':'COMP', 'date':'2015-2020'}, refresh=30)


def test_results_issn():
    assert_equal(len(ser1.results), 1)
    assert_equal(ser1.results[0]['title'], 'Econometrica')


def test_results_title():
    expected_fields = set(['publisher', 'url'])
    ser2_fields = set(j for i in ser2.results for j in i.keys())
    assert_equal(ser2_fields, expected_fields)


def test_results_subjcode():
    ser3_subj_codes = set(i['subject_area_codes'] for i in ser3.results)
    assert_equal(set('2612' in i for i in ser3_subj_codes), set([True]))


def test_results_date():
    ser4_subj_abbs = set(i['subject_area_abbrevs'] for i in ser4.results)
    assert_true(False not in ['COMP' in i for i in ser4_subj_abbs])
    ser4_sjr_fields = set(j for i in ser4.results for j in i.keys() if 'SJR' in j)
    assert_true('SJR_2017' in ser4_sjr_fields)
