#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for `ScopusAbstract` module."""

from nose.tools import assert_equal, assert_true

import scopus


ab = scopus.ScopusAbstract("2-s2.0-84930616647", view="FULL", refresh=True)


def test_affiliations():
    affs = ab.affiliations
    assert_true(len(affs) == 1)
    aff = affs[0]
    assert_true(isinstance(aff, scopus.scopus_api._ScopusAffiliation))
    assert_equal(aff.id, '60027950')
    assert_equal(aff.affilname, 'Carnegie Mellon University')
    assert_equal(aff.city, 'Pittsburgh')
    assert_equal(aff.country, 'United States')
    link = 'https://api.elsevier.com/content/affiliation/affiliation_id/60027950'
    assert_equal(aff.href, link)


def test_aggregationType():
    assert_equal(ab.aggregationType, 'Journal')


def test_article_number():
    pass


def test_authors():
    assert_true(isinstance(ab.authors[0], scopus.scopus_api._ScopusAuthor))


def test_bibtex():
    expected = '@article{Kitchin2015ExamplesPublishing,\n  author = \
{John R. Kitchin},\n  title = {Examples of effective data sharing in \
scientific publishing},\n  journal = {ACS Catalysis},\n  year = {2015},\n  \
volume = {5},\n  number = {6},\n  pages = {3894-3899},\n  doi = {10.1021/\
acscatal.5b00538}\n}\n\n'
    assert_equal(ab.bibtex, expected)


def test_citationLanguage():
    assert_equal(ab.citationLanguage, 'English')


def test_citationType():
    assert_equal(ab.citationType, 're')


def test_citedby_count():
    expected = 5
    assert_true(ab.citedby_count >= expected)


def test_citedby_url():
    expected = 'https://www.scopus.com/inward/citedby.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward'
    assert_equal(ab.citedby_url, expected)


def test_coverDate():
    assert_equal(ab.coverDate, '2015-06-05')


def test_doi():
    assert_equal(ab.doi, '10.1021/acscatal.5b00538')


def test_endingPage():
    assert_equal(ab.endingPage, '3899')


def test_html():
    expected = '<a href="https://www.scopus.com/authid/detail.url?origin=\
AuthorProfile&authorId=7004212771">John R. Kitchin</a>, <a href="https://www.\
scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&\
origin=inward">Examples of effective data sharing in scientific \
publishing</a>, <a href="https://www.scopus.com/source/sourceInfo.url?\
sourceId=19700188320">ACS Catalysis</a>, <b>5(6)</b>, p. 3894-3899, \
(2015-06-05). <a href="https://doi.org/10.1021/acscatal.5b00538">\
doi:10.1021/acscatal.5b00538</a>.'
    assert_equal(ab.html, expected)


def test_issn():
    assert_equal(ab.issn, '21555435')


def test_issueIdentifier():
    assert_equal(ab.issueIdentifier, '6')


def test_latex():
    expected = 'John R. Kitchin, \\textit{Examples of effective data sharing \
in scientific publishing}, ACS Catalysis, \\textbf{5(6)}, p. 3894-3899, \
(2015-06-05). \\href{https://doi.org/10.1021/acscatal.5b00538}{doi:10.1021/\
acscatal.5b00538}, \\href{https://www.scopus.com/inward/record.uri?partnerID=\
HzOxMe3b&scp=84930616647&origin=inward}{scopus:2-s2.0-84930616647}.'
    assert_equal(ab.latex, expected)


def test_nauthors():
    assert_equal(ab.nauthors, 1)


def test_pageRange():
    assert_equal(ab.pageRange, '3894-3899')


def test_publicationName():
    assert_equal(ab.publicationName, 'ACS Catalysis')


def test_publisher():
    assert_equal(ab.publisher, '\nAmerican Chemical Society\nservice@acs.org\n')


def test_refcount():
    assert_equal(ab.refcount, '22')


def test_references():
    expected = [
        '2-s2.0-84881394200', '2-s2.0-84896585411', '2-s2.0-84949115648',
        '2-s2.0-84908637059', '2-s2.0-84901638552', '2-s2.0-84896380535',
        '2-s2.0-84923164062', '2-s2.0-84923164062', '2-s2.0-84930667693',
        '2-s2.0-79952591087', '2-s2.0-84923165709', '2-s2.0-0036572216',
        '2-s2.0-84924117832', '2-s2.0-84930624433', '2-s2.0-79955561198',
        '2-s2.0-84930642229', '2-s2.0-0010630518', '2-s2.0-84861337169',
        '2-s2.0-34247481878', '2-s2.0-79958260504', '2-s2.0-58149108944',
        '2-s2.0-84917679308']
    assert_equal(ab.references, expected)


def test_ris():
    expected = 'TY  - JOUR\n\
TI  - Examples of effective data sharing in scientific publishing\n\
JO  - ACS Catalysis\nVL  - 5\nDA  - 2015-06-05\nSP  - 3894-3899\n\
PY  - 2015\nDO  - 10.1021/acscatal.5b00538\nUR  - https://doi.org/10.1021/\
acscatal.5b00538\nAU  - Kitchin J.R.\nIS  - 6\nER  - \n\n'
    assert_equal(ab.ris, expected)


def test_scopus_url():
    expected = 'https://www.scopus.com/inward/record.uri?partnerID=HzOxMe3b&scp=84930616647&origin=inward'
    assert_equal(ab.scopus_url, expected)


def test_source_id():
    assert_equal(ab.source_id, '19700188320')


def test_srctype():
    assert_equal(ab.srctype, 'j')


def test_startingPage():
    assert_equal(ab.startingPage, '3894')


def test_subjectAreas():
    assert_equal(ab.subjectAreas, ['Catalysis'])


def test_title():
    expected = 'Examples of effective data sharing in scientific publishing'
    assert_equal(ab.title, expected)


def test_url():
    expected = 'https://api.elsevier.com/content/abstract/scopus_id/84930616647'
    assert_equal(ab.url, expected)


def test_volume():
    assert_equal(ab.volume, '5')


def test_website():
    assert_equal(ab.website, 'http://pubs.acs.org/page/accacs/about.html')


def test_authkeywords():
    ab2 = scopus.ScopusAbstract("2-s2.0-0000212165", view="FULL", refresh=True)
    authkeywords = ab2.authkeywords
    assert_true(len(authkeywords) == 3)
    assert_equal(authkeywords[0], 'Fuzzy clustering')
    assert_equal(authkeywords[1], 'Fuzzy modelling')
    assert_equal(authkeywords[2], 'Unsupervised learning')
