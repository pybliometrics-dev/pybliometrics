#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.AuthorRetrieval` module."""

import warnings
from collections import Counter, namedtuple
from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import AuthorRetrieval

warnings.simplefilter("always")

au = AuthorRetrieval("7004212771", refresh=30)


def test_affiliation_current():
    received = au.affiliation_current
    assert_true(isinstance(received, list))
    assert_true(len(received) >= 1)
    order = 'id parent type relationship afdispname preferred_name '\
            'parent_preferred_name country_code country address_part city '\
            'state postal_code org_domain org_URL'
    aff = namedtuple('Affiliation', order)
    expected = aff(id='110785688', parent='60027950', type='dept',
        relationship='author', afdispname=None, country='United States',
        preferred_name='Department of Chemical Engineering',
        parent_preferred_name='Carnegie Mellon University', country_code='usa',
        address_part='5000 Forbes Avenue', city='Pittsburgh', state='PA',
        postal_code='15213-3890', org_domain='cmu.edu',
        org_URL='https://www.cmu.edu/')
    assert_true(expected in received)


def test_affiliation_history():
    received = au.affiliation_history
    assert_true(isinstance(received, list))
    assert_true(len(received) >= 10)
    order = 'id parent type relationship afdispname preferred_name '\
            'parent_preferred_name country_code country address_part city '\
            'state postal_code org_domain org_URL'
    aff = namedtuple('Affiliation', order)
    expected = aff(id='60008644', parent=None, type='parent',
        relationship='author', afdispname=None,
        preferred_name='Fritz Haber Institute of the Max Planck Society',
        parent_preferred_name=None, country_code='deu', country='Germany',
        address_part='Faradayweg 4-6', city='Berlin', state=None,
        postal_code='14195', org_domain='fhi.mpg.de',
        org_URL='https://www.fhi.mpg.de/')
    assert_true(expected in received)


def test_citation_count():
    assert_true(int(au.citation_count) >= 7584)


def test_cited_by_count():
    assert_true(int(au.cited_by_count) >= 6066)


def test_classificationgroup():
    groups = au.classificationgroup
    assert_true(isinstance(groups, list))
    assert_true(len(groups) > 0)
    assert_true(('1906', '1') in groups)  # frequency might differ


def test_coauthor_count():
    assert_true(int(au.coauthor_count) >= 164)


def test_coauthor_link():
    expected = 'http://api.elsevier.com/content/search/author?co-author=7004212771'
    assert_equal(au.coauthor_link, expected)


def test_date_created():
    assert_equal(au.date_created, (2005, 12, 3))


def test_document_count():
    assert_true(int(au.document_count) >= 98)


def test_eid():
    assert_equal(au.eid, '9-s2.0-7004212771')


def test_estimate_uniqueness():
    assert_equal(au.estimate_uniqueness(), 2)


def test_given_name():
    assert_equal(au.given_name, 'John R.')


def get_coauthors():
    received = au.get_coauthors()
    assert_true(isinstance(received, list))
    assert_true(len(received) > 155)
    fields = 'surname given_name id areas affiliation_id name city country'
    coauth = namedtuple('Coauthor', fields)
    expected = coauth(surname='Rose', given_name='Michael E.', id='57209617104',
        areas='Computer Science (all)', affiliation_id='60105007',
        name='Max-Planck-Institut für Innovation und Wettbewerb',
        city='Munich', country='Germany')
    assert_true(expected in received)


def test_get_documents():
    subtypes = {'re', 'ed', 'no'}
    received = au.get_documents(subtypes)
    assert_equal(len(received), 7)


def test_get_document_eids():
    assert_true(len(au.get_document_eids()) >= 99)


def test_h_index():
    assert_true(int(au.h_index) >= 27)


def test_historical_identifier():
    expected = ['35787230500', '36488127000', '54974425600', '55004143700',
                '55004143800', '57057263700', '56641032000', '36747787600']
    assert_equal(au.historical_identifier, expected)


def test_identifier():
    assert_equal(au.identifier, "7004212771")


def test_indexed_name():
    assert_equal(au.indexed_name, 'Kitchin J.')


def test_initials():
    assert_equal(au.initials, 'J.R.')


def test_name_variants():
    names = au.name_variants
    assert_true(isinstance(names, list))
    assert_true(len(names) > 0)
    expected = "<class 'pybliometrics.scopus.author_retrieval.Variant'>"
    assert_equal(str(type(names[0])), expected)


def test_orcid():
    assert_equal(au.orcid, '0000-0003-2625-9232')


def test_publication_range():
    assert_equal(au.publication_range[0], '1995')
    assert_true(int(au.publication_range[1]) >= 2018)


def test_scopus_author_link():
    expected = 'http://api.elsevier.com/content/author/author_id/7004212771'
    assert_equal(au.scopus_author_link, expected)


def test_search_link():
    expected = 'http://api.elsevier.com/content/search/scopus?query='\
               'au-id%287004212771%29'
    assert_equal(au.search_link, expected)


def test_self_link():
    expected = 'https://www.scopus.com/authid/detail.uri?partnerID=HzOxMe3b&'\
               'authorId=7004212771&origin=inward'
    assert_equal(au.self_link, expected)


def test_status():
    assert_equal(au.status, "update")


def test_subject_areas():
    areas = au.subject_areas
    assert_true(isinstance(areas, list))
    assert_true(len(areas) > 0)
    expected = "<class 'pybliometrics.scopus.author_retrieval.Subjectarea'>"
    assert_equal(str(type(areas[0])), expected)


def test_surname():
    assert_equal(au.surname, 'Kitchin')


def test_url():
    expected = 'http://api.elsevier.com/content/author/author_id/7004212771'
    assert_equal(au.url, expected)


def test_warning_without_forwarding():
    with warnings.catch_warnings(record=True) as w:
        au = AuthorRetrieval("24079538400", refresh=False)
        assert_equal(len(w), 1)
        assert_true(issubclass(w[-1].category, UserWarning))
        assert_true("24079538400" in str(w[-1].message))


def test_warning_with_forwarding():
    au = AuthorRetrieval("57191449583", refresh=False)
    with warnings.catch_warnings(record=True) as w:
        auth_id = au.identifier
        assert_equal(len(w), 1)
        assert_true(issubclass(w[-1].category, UserWarning))
        assert_true("57191449583" in str(w[-1].message))
    assert_equal(auth_id, '36854449200')
