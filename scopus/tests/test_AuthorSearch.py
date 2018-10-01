#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `AuthorSearch` module."""

from collections import namedtuple
from nose.tools import assert_equal

import scopus

s = scopus.AuthorSearch('authlast(selten) and authfirst(reinhard)',
                        refresh=True)


def test_authors():
    order = 'eid surname initials givenname affiliation documents '\
            'affiliation_id city country areas'
    Author = namedtuple('Author', order)
    expected = [Author(eid='9-s2.0-6602907525', surname='Selten',
                initials='R.', givenname='Reinhard',
                affiliation='Universitat Bonn', documents='73',
                affiliation_id='60007493', city='Bonn', country='Germany',
                areas='ECON (71); MATH (19); BUSI (15)')]
    assert_equal(s.authors, expected)
