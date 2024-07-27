"""Tests for `scopus.CitationOverview` module."""

from collections import namedtuple

from pybliometrics.scopus import CitationOverview, init

init()


co_eid = CitationOverview(["85068268027", "84930616647"],
                          refresh=30, date="2016-2020")
co_doi = CitationOverview(["10.1016/j.softx.2019.100263"],
                          id_type="doi", refresh=30, date="2016-2020")

def test_authors():
    Author = namedtuple('Author', 'name surname initials id url')
    url = 'https://api.elsevier.com/content/author/author_id/7004212771'
    john = Author(name='Kitchin J.R.', surname='Kitchin',
                  initials='J.R.', id='7004212771', url=url)
    assert co_eid.authors[0][1] == john
    assert co_eid.authors[1] == [john]
    assert co_doi.authors[0][1] == john


def test_cc():
    expected0 = [(2016, 0), (2017, 0), (2018, 0), (2019, 0), (2020, 6)]
    expected1 = [(2016, 4), (2017, 2), (2018, 3), (2019, 2), (2020, 2)]
    assert co_eid.cc == [expected0, expected1]
    assert co_doi.cc == [expected0]


def test_citationType_long():
    assert co_eid.citationType_long == ['Article', 'Review']
    assert co_doi.citationType_long == ['Article']


def test_citationType_short():
    assert co_eid.citationType_short == ['ar', 're']
    assert co_doi.citationType_short == ['ar']


def test_columnTotal():
    assert co_eid.columnTotal == [4, 2, 3, 2, 8]
    assert co_doi.columnTotal == [0, 0, 0, 0, 6]


def test_doi():
    expected = ['10.1016/j.softx.2019.100263', '10.1021/acscatal.5b00538']
    assert co_eid.doi == expected
    assert co_doi.doi == [expected[0]]


def test_endingPage():
    assert co_eid.endingPage == [None, '3899']
    assert co_doi.endingPage is None


def test_grandTotal():
    assert co_eid.grandTotal >= 29
    assert co_doi.grandTotal >= 16


def test_h_index():
    assert co_eid.h_index == 2
    assert co_doi.h_index == 1


def test_issn():
    expected = ['2352-7110', '2155-5435']
    assert co_eid.issn == expected
    assert co_doi.issn == [expected[0]]


def test_issueIdentifier():
    assert co_eid.issueIdentifier == [None, '6']
    assert co_doi.issueIdentifier is None


def test_laterColumnTotal():
    assert co_eid.laterColumnTotal >= 18
    assert co_doi.laterColumnTotal >= 16


def test_lcc():
    assert co_eid.lcc[0] >= 1
    assert co_eid.lcc[1] >= 1
    assert co_doi.lcc[0] >= 1


def test_pcc():
    assert co_eid.pcc == [0, 0]
    assert co_doi.pcc == [0]


def test_pii():
    expected = ['S2352711019300573', None]
    assert co_eid.pii == expected
    assert co_doi.pii == [expected[0]]


def prevColumnTotal():
    assert co_eid.prevColumnTotal == 0
    assert co_doi.prevColumnTotal == 0


def test_rangeColumnTotal():
    assert co_eid.rangeColumnTotal == 19
    assert co_doi.rangeColumnTotal == 6


def test_rangeCount():
    assert co_eid.rangeCount[0] >= 6
    assert co_eid.rangeCount[1] >= 6
    assert co_doi.rangeCount[0] >= 6


def test_rowTotal():
    assert co_eid.rowTotal[0] >= 10
    assert co_eid.rowTotal[1] >= 10
    assert co_doi.rowTotal[0] >= 10


def test_scopus_id():
    expected = [85068268027, 84930616647]
    assert co_eid.scopus_id == expected
    assert co_doi.scopus_id == [expected[0]]


def test_startingPage():
    assert co_eid.startingPage == [None, '3894']
    assert co_doi.startingPage == None


def test_sortTitle():
    expected = ['SoftwareX', 'ACS Catalysis']
    assert co_eid.sortTitle == expected
    assert co_doi.sortTitle == [expected[0]]


def test_title():
    expected = ['pybliometrics: Scriptable bibliometrics using a Python interface to Scopus',
                'Examples of effective data sharing in scientific publishing']
    assert co_eid.title == expected
    assert co_doi.title == [expected[0]]


def test_url():
    expected = ['https://api.elsevier.com/content/abstract/scopus_id/85068268027',
                'https://api.elsevier.com/content/abstract/scopus_id/84930616647']
    assert co_eid.url == expected
    assert co_doi.url == [expected[0]]


def test_volume():
    assert co_eid.volume == ['10', '5']
    assert co_doi.volume == ['10']
