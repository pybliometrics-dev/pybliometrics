#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.AuthorSearch` module."""

from collections import namedtuple
from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import AuthorSearch

s1 = AuthorSearch('authlast(selten) and authfirst(reinhard)', refresh=30)
s2 = AuthorSearch('authlast(selten)', download=False)


def test_authors():
    assert_true(isinstance(s1.authors, list))
    assert_true(len(s1.authors) >= 2)
    order = 'eid surname initials givenname affiliation documents '\
            'affiliation_id city country areas'
    Author = namedtuple('Author', order)
    expected = Author(eid='9-s2.0-6602907525', surname='Selten',
        initials='R.', givenname='Reinhard', affiliation='Universität Bonn',
        documents='74', affiliation_id='60007493', city='Bonn',
        country='Germany', areas='ECON (73); MATH (19); BUSI (16)')
    assert_equal(s1.authors[0], expected)


def test_authors_nodownload():
    # Only works if query hasn't been cached
    assert_equal(s2.authors, None)


def test_results_size():
    received1 = s1.get_results_size()
    assert_true(received1 >= 1)
    received2 = s2.get_results_size()
    assert_true(received2 >= 25)
