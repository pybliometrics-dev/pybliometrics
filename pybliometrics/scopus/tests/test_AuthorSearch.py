"""Tests for `scopus.AuthorSearch` module."""

from pybliometrics.scopus import AuthorSearch, init
from pybliometrics.scopus.author_search import Author

init()

s1 = AuthorSearch('authlast(selten) and authfirst(reinhard)', refresh=30)
s2 = AuthorSearch('authlast(selten)', download=False, refresh=True)


def test_authors():
    assert isinstance(s1.authors, list)
    assert len(s1.authors) >= 1
    expected = Author(eid='9-s2.0-6602907525', orcid=None, surname='Selten',
        initials='R.', givenname='Reinhard', affiliation='Universität Bonn',
        documents=76, affiliation_id='60007493', city='Bonn',
        country='Germany', areas='ECON (72); BUSI (8)')
    assert s1.authors[0] == expected


def test_authors_nodownload():
    # Only works if query hasn't been cached
    assert s2.authors is None


def test_results_size():
    received1 = s1.get_results_size()
    assert received1 >= 1
    received2 = s2.get_results_size()
    assert received2 >= 25
