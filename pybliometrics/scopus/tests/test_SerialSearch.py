#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests for `scopus.SerialSearch` module."""

from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import SerialSearch


# Search by title
ser1 = SerialSearch({'title': 'SoftwareX'}, refresh=30)
# Search by ISSN
ser2 = SerialSearch({'issn': '1468-0262'}, refresh=30)
# Search by publisher
ser3 = SerialSearch({'pub': 'Stellenbosch'}, refresh=30)
# Search by subject abbreviation
ser4 = SerialSearch({'subj': 'COMP'}, refresh=30)
# Search by subject area code
ser5 = SerialSearch({'subjCode': '2612'}, refresh=30)


def test_results_title():
    assert_equal(len(ser1.results), 1)
    assert_equal(ser1.results[0]['title'], 'SoftwareX')


def test_results_issn():
    assert_equal(len(ser2.results), 1)
    assert_equal(ser2.results[0]['title'], 'Econometrica')


def test_results_pub():
    assert_equal(len(ser3.results), 5)
    assert_equal(ser3.results[0]['title'], 'African Finance Journal')


def test_results_subj():
    ser4_subj_abbs = set(i['subject_area_abbrevs'] for i in ser4.results)
    assert_true(False not in ['COMP' in i for i in ser4_subj_abbs])


def test_results_subjcode():
    ser5_subj_codes = set(i['subject_area_codes'] for i in ser5.results)
    assert_true(False not in ['2612' in i for i in ser5_subj_codes])
