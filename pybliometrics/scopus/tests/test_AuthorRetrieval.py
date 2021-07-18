#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `scopus.AuthorRetrieval` module."""

import warnings
from collections import Counter, namedtuple
from nose.tools import assert_equal, assert_true

from pybliometrics.scopus import AuthorRetrieval

warnings.simplefilter("always")

metrics = AuthorRetrieval("7004212771", refresh=30, view="METRICS")
light = AuthorRetrieval("7004212771", refresh=30, view="LIGHT")
standard = AuthorRetrieval("7004212771", refresh=30, view="STANDARD")
enhanced = AuthorRetrieval("7004212771", refresh=30, view="ENHANCED")


def test_affiliation_current():
    assert_equal(metrics.affiliation_current, None)
    assert_equal(light.affiliation_current, None)
    order = 'id parent type relationship afdispname preferred_name '\
            'parent_preferred_name country_code country address_part city '\
            'state postal_code org_domain org_URL'
    aff = namedtuple('Affiliation', order)
    expected = aff(id=110785688, parent=60027950, type='dept',
        relationship='author', afdispname=None, country='United States',
        preferred_name='Department of Chemical Engineering',
        parent_preferred_name='Carnegie Mellon University', country_code='usa',
        address_part='5000 Forbes Avenue', city='Pittsburgh', state='PA',
        postal_code='15213-3890', org_domain='cmu.edu',
        org_URL='https://www.cmu.edu/')
    for a in (standard, enhanced):
        received = a.affiliation_current
        assert_true(isinstance(received, list))
        assert_true(len(received) >= 1)
        assert_true(expected in received)


def test_affiliation_history():
    assert_equal(metrics.affiliation_history, None)
    assert_equal(light.affiliation_history, None)
    order = 'id parent type relationship afdispname preferred_name '\
            'parent_preferred_name country_code country address_part city '\
            'state postal_code org_domain org_URL'
    aff = namedtuple('Affiliation', order)
    expected = aff(id=60008644, parent=None, type='parent',
        relationship='author', afdispname=None,
        preferred_name='Fritz Haber Institute of the Max Planck Society',
        parent_preferred_name=None, country_code='deu', country='Germany',
        address_part='Faradayweg 4-6', city='Berlin', state=None,
        postal_code='14195', org_domain='fhi.mpg.de',
        org_URL='https://www.fhi.mpg.de/')
    for a in (standard, enhanced):
        received = a.affiliation_history
        assert_true(isinstance(received, list))
        assert_true(len(received) >= 10)
        assert_true(expected in received)


def test_alias():
    assert_equal(metrics.alias, None)
    assert_equal(light.alias, None)
    assert_equal(standard.alias, None)
    assert_equal(enhanced.alias, None)


def test_citation_count():
    expected = 13600
    assert_true(metrics.citation_count >= expected)
    assert_true(light.citation_count >= expected)
    assert_true(standard.citation_count >= expected)
    assert_true(enhanced.citation_count >= expected)


def test_cited_by_count():
    expected = 10900
    assert_true(metrics.cited_by_count >= expected)
    assert_true(light.cited_by_count >= expected)
    assert_true(standard.cited_by_count >= expected)
    assert_true(enhanced.cited_by_count >= expected)


def test_classificationgroup():
    assert_equal(metrics.classificationgroup, None)
    assert_equal(light.classificationgroup, None)
    for a in (standard, enhanced):
        received = a.classificationgroup
        assert_true(isinstance(received, list))
        assert_true(len(received) > 0)
        assert_true((1906, 1) in received)  # frequency might differ


def test_coauthor_count():
    assert_equal(light.coauthor_count, None)
    assert_equal(standard.coauthor_count, None)
    expected = 175
    assert_true(metrics.coauthor_count >= expected)
    assert_true(enhanced.coauthor_count >= expected)


def test_coauthor_link():
    assert_equal(metrics.coauthor_link, None)
    assert_equal(light.coauthor_link, None)
    assert_equal(standard.coauthor_link, None)
    expected = 'http://api.elsevier.com/content/search/author?co-author=7004212771'
    assert_equal(enhanced.coauthor_link, expected)


def test_date_created():
    assert_equal(metrics.date_created, None)
    assert_equal(light.date_created, None)
    assert_equal(standard.date_created, (2005, 12, 3))
    assert_equal(enhanced.date_created, (2005, 12, 3))


def test_document_count():
    expected = 106
    assert_true(light.document_count >= expected)
    assert_true(standard.document_count >= expected)
    assert_true(metrics.document_count >= expected)
    assert_true(enhanced.document_count >= expected)


def test_eid():
    assert_equal(metrics.eid, None)
    assert_equal(light.eid, '9-s2.0-7004212771')
    assert_equal(standard.eid, '9-s2.0-7004212771')
    assert_equal(enhanced.eid, '9-s2.0-7004212771')


def test_estimate_uniqueness():
    expected = 2
    assert_equal(metrics.estimate_uniqueness(), 0)
    assert_equal(light.estimate_uniqueness(), 0)
    assert_equal(standard.estimate_uniqueness(), expected)
    assert_equal(enhanced.estimate_uniqueness(), expected)


def test_given_name():
    assert_equal(metrics.given_name, None)
    assert_equal(light.given_name, None)
    assert_equal(standard.given_name, 'John R.')
    assert_equal(enhanced.given_name, 'John R.')


def get_coauthors():
    assert_equal(metrics.get_coauthors(), None)
    assert_equal(light.get_coauthors(), None)
    assert_equal(standard.get_coauthors(), None)
    received = enhanced.get_coauthors()
    assert_true(isinstance(received, list))
    assert_true(len(received) > 155)
    fields = 'surname given_name id areas affiliation_id name city country'
    coauth = namedtuple('Coauthor', fields)
    expected = coauth(surname='Rose', given_name='Michael E.', id=57209617104,
        areas='Computer Science (all)', affiliation_id=60105007,
        name='Max-Planck-Institut für Innovation und Wettbewerb',
        city='Munich', country='Germany')
    assert_true(expected in received)


def test_get_documents():
    subtypes = {'re', 'ed', 'no'}
    received = enhanced.get_documents(subtypes)
    assert_equal(len(received), 7)


def test_get_document_eids():
    expected = 100
    assert_true(len(enhanced.get_document_eids()) >= expected)


def test_h_index():
    assert_equal(light.h_index, None)
    assert_equal(standard.h_index, None)
    expected = 34
    assert_true(metrics.h_index >= expected)
    assert_true(enhanced.h_index >= expected)


def test_historical_identifier():
    assert_equal(metrics.historical_identifier, None)
    assert_equal(light.historical_identifier, None)
    assert_equal(standard.historical_identifier, None)
    expected = [35787230500, 36488127000, 54974425600, 55004143700,
                55004143800, 57057263700, 56641032000, 36747787600,
                57206217299, 57219840256]
    assert_equal(enhanced.historical_identifier, expected)


def test_identifier():
    expected = 7004212771
    assert_equal(metrics.identifier, expected)
    assert_equal(light.identifier, expected)
    assert_equal(standard.identifier, expected)
    assert_equal(enhanced.identifier, expected)


def test_indexed_name():
    assert_equal(metrics.indexed_name, None)
    assert_equal(light.indexed_name, None)
    assert_equal(standard.indexed_name, 'Kitchin J.')
    assert_equal(enhanced.indexed_name, 'Kitchin J.')


def test_initials():
    assert_equal(metrics.initials, None)
    assert_equal(light.initials, None)
    assert_equal(standard.initials, 'J.R.')
    assert_equal(enhanced.initials, 'J.R.')


def test_name_variants():
    assert_equal(metrics.name_variants, None)
    assert_equal(light.name_variants, None)
    expected = "<class 'pybliometrics.scopus.author_retrieval.Variant'>"
    for a in (standard, enhanced):
        received = a.name_variants
        assert_true(isinstance(received, list))
        assert_true(len(received) > 0)
        assert_equal(str(type(received[0])), expected)


def test_orcid():
    assert_equal(metrics.orcid, None)
    assert_equal(light.orcid, '0000-0003-2625-9232')
    assert_equal(standard.orcid, '0000-0003-2625-9232')
    assert_equal(enhanced.orcid, '0000-0003-2625-9232')


def test_publication_range():
    assert_equal(metrics.publication_range, None)
    assert_equal(light.publication_range, None)
    for a in (standard, enhanced):
        assert_equal(a.publication_range[0], 1995)
        assert_true(a.publication_range[1] >= 2021)


def test_scopus_author_link():
    assert_equal(metrics.scopus_author_link, None)
    expected = 'http://api.elsevier.com/content/author/author_id/7004212771'
    assert_equal(light.scopus_author_link, expected)
    assert_equal(standard.scopus_author_link, expected)
    assert_equal(enhanced.scopus_author_link, expected)


def test_search_link():
    assert_equal(metrics.search_link, None)
    expected = 'http://api.elsevier.com/content/search/scopus?query='\
               'au-id%287004212771%29'
    assert_equal(light.search_link, expected)
    assert_equal(standard.search_link, expected)
    assert_equal(enhanced.search_link, expected)


def test_self_link():
    assert_equal(metrics.self_link, None)
    expected = 'https://www.scopus.com/authid/detail.uri?partnerID=HzOxMe3b&'\
               'authorId=7004212771&origin=inward'
    assert_equal(light.self_link, expected)
    assert_equal(standard.self_link, expected)
    assert_equal(enhanced.self_link, expected)


def test_status():
    assert_equal(metrics.status, None)
    assert_equal(light.status, None)
    expected = "update"
    assert_equal(standard.status, expected)
    assert_equal(enhanced.status, expected)


def test_subject_areas():
    assert_equal(metrics.subject_areas, None)
    assert_equal(light.subject_areas, None)
    expected = "<class 'pybliometrics.scopus.author_retrieval.Subjectarea'>"
    for a in (standard, enhanced):
        received = a.subject_areas
        assert_true(isinstance(received, list))
        assert_true(len(received) > 0)
        assert_equal(str(type(received[0])), expected)


def test_surname():
    assert_equal(metrics.surname, None)
    assert_equal(light.surname, None)
    assert_equal(standard.surname, 'Kitchin')
    assert_equal(enhanced.surname, 'Kitchin')


def test_url():
    expected = 'http://api.elsevier.com/content/author/author_id/7004212771'
    assert_equal(metrics.url, expected)
    assert_equal(light.url, expected)
    assert_equal(standard.url, expected)
    assert_equal(enhanced.url, expected)


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
    assert_equal(auth_id, 36854449200)
