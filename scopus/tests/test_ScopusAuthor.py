#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `ScopusAuthor` module."""

from collections import Counter
from nose.tools import assert_equal, assert_true

import scopus


au = scopus.ScopusAuthor("7004212771", refresh=True)


def test_affiliation_history():
    affs = au.affiliation_history
    assert_true(len(affs) >= 16)
    assert_true(isinstance(affs[0], scopus.scopus_affiliation.ScopusAffiliation))


def test_author_id():
    assert_equal(au.author_id, "7004212771")


def test_author_impact_factor():
    (ncites, npapers, aif) = au.author_impact_factor(refresh=False)
    expected = (504, 11, 45.81818181818182)
    assert_true(expected[0] <= ncites)
    assert_true(expected[1] <= npapers)
    assert_true(expected[2] <= aif)


def test_citation_count():
    expected = 5514
    assert_true(au.citation_count >= expected)


def test_coauthor_url():
    expected = 'http://api.elsevier.com/content/search/author?co-author=7004212771'
    assert_equal(au.coauthor_url, expected)


def test_current_affiliation():
    expected = 'Carnegie Mellon University, Department of Chemical Engineering'
    assert_equal(au.current_affiliation, expected)


def test_date_created():
    assert_equal(au.date_created, (2005, 12, 3))


def test_firstname():
    assert_equal(au.firstname, 'John R.')


def test_get_abstracts():
    abstracts = au.get_abstracts(refresh=False)
    assert_true(len(abstracts) >= 90)
    assert_true(isinstance(abstracts[0], scopus.scopus_api.ScopusAbstract))


def test_get_coauthors():
    coauthors = au.get_coauthors()
    assert_true(len(coauthors) >= 158)


def test_get_document_summary():
    pass


def n_last_author_papers():
    expected = 44
    assert_true(au.n_last_author_papers(refresh=False) >= 44)


def test_hindex():
    expected = 22
    assert_true(au.hindex >= expected)


def test_lastname():
    assert_equal(au.lastname, 'Kitchin')


def test_name():
    assert_equal(au.name, 'John R. Kitchin')


def test_ncited_by():
    expected = 4335
    assert_true(au.ncited_by >= expected)


def test_ncoauthors():
    expected = 153
    assert_true(au.ncoauthors >= expected)


def test_ndocuments():
    expected = 90
    assert_true(au.ndocuments >= expected)


def test_n_first_author_papers():
    expected = 12
    assert_true(au.n_first_author_papers(refresh=False) >= 12)


def test_n_journal_articles():
    jour_arts = au.n_journal_articles(refresh=False)
    expected = 72
    assert_true(jour_arts >= 72)


def test_n_yearly_publications():
    yearly_pubs = au.n_yearly_publications(refresh=False)
    assert_true(isinstance(yearly_pubs, Counter))


def test_orcid():
    assert_equal(au.orcid, '0000-0003-2625-9232')


def publication_history():
    hist = au.publication_history
    assert_true(isinstance(areas, list))
    assert_true(len(areas) > 0)
    expected = ('ACS Catalysis', 'ACS Catal.', 'j', '21555435')
    assert_true(expected in areas)


def test_scopus_url():
    expected = 'https://www.scopus.com/authid/detail.uri?\
partnerID=HzOxMe3b&authorId=7004212771&origin=inward'
    assert_equal(au.scopus_url, expected)


def test_subject_areas():
    areas = au.subject_areas
    assert_true(isinstance(areas, list))
    assert_true(len(areas) > 0)
    expected = ('Analytical Chemistry', 1, 'CHEM', '1602')
    # Frequency might differ
    assert_true(expected in areas)
