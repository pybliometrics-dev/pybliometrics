#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `AuthorSearch` module."""

from collections import namedtuple
from nose.tools import assert_equal, raises

import scopus

s1 = scopus.AuthorSearch('authlast(selten) and authfirst(reinhard)',
                        refresh=True)
s2 = scopus.AuthorSearch('authlast(selten)', refresh=True, download=False)


def test_authors():
    order = 'eid surname initials givenname affiliation documents '\
            'affiliation_id city country areas'
    Author = namedtuple('Author', order)
    expected = [Author(eid='9-s2.0-6602907525', surname='Selten',
        initials='R.', givenname='Reinhard', affiliation='Universität Bonn',
        documents='73', affiliation_id='60007493', city='Bonn',
        country='Germany', areas='ECON (71); MATH (19); BUSI (15)')]
    assert_equal(s1.authors, expected)


@raises(AttributeError)
def test_authors_error():
    recieved = s2.authors


def test_results_size():
    assert_equal(s1.get_results_size(), 1)
    assert_equal(s2.get_results_size(), 25)
