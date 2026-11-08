"""Offline tests for `scopus.AbstractRetrieval().get_ris()`.

These tests build `AbstractRetrieval` objects from minimal, hand-written
JSON instead of downloading them, so they require neither an API key nor
a network connection.
"""

from pybliometrics.scopus import AbstractRetrieval


def _make_abstract(coredata, authors=None, head=None):
    """Create an AbstractRetrieval object from a minimal JSON response."""
    ab = AbstractRetrieval.__new__(AbstractRetrieval)
    ab._json = {'coredata': coredata}
    if authors is not None:
        ab._json['authors'] = {'author': authors}
    ab._head = head or {}
    return ab


AUTHORS = [{'@auid': '7004212771', 'ce:indexed-name': 'Kitchin J.R.',
            'ce:surname': 'Kitchin'}]


def test_get_ris_journal():
    ab = _make_abstract({
        'prism:aggregationType': 'Journal',
        'subtype': 'ar',
        'dc:title': 'Examples of effective data sharing in scientific '
                    'publishing',
        'prism:publicationName': 'ACS Catalysis',
        'prism:coverDate': '2015-06-05',
        'prism:doi': '10.1021/acscatal.5b00538',
        'prism:volume': '5',
        'prism:issueIdentifier': '6',
        'prism:pageRange': '3894-3899',
    }, authors=AUTHORS)
    expected = (
        "TY  - JOUR\nTI  - Examples of effective data sharing in scientific "
        "publishing\nJO  - ACS Catalysis\nDA  - 2015-06-05\nPY  - "
        "2015\nAU  - Kitchin J.R.\nDO  - 10.1021/acscatal.5b00538\n"
        "UR  - https://doi.org/10.1021/acscatal.5b00538\nVL  - 5\n"
        "IS  - 6\nSP  - 3894-3899\nER  - \n\n"
    )
    assert ab.get_ris() == expected


def test_get_ris_book():
    ab = _make_abstract({
        'prism:aggregationType': 'Book',
        'subtype': 'bk',
        'dc:title': 'Handbook of Things',
        'prism:publicationName': 'Handbook of Things',
        'prism:coverDate': '2009-01-01',
    }, authors=AUTHORS, head={'source': {
        'isbn': [{'$': '0203881486'}, {'$': '9780203881484'}],
        'publisher': {'publishername': 'Taylor and Francis'},
    }})
    expected = (
        "TY  - BOOK\nTI  - Handbook of Things\nDA  - 2009-01-01\n"
        "PY  - 2009\nAU  - Kitchin J.R.\nSN  - 0203881486\n"
        "SN  - 9780203881484\nPB  - Taylor and Francis\nER  - \n\n"
    )
    assert ab.get_ris() == expected


def test_get_ris_book_chapter():
    ab = _make_abstract({
        'prism:aggregationType': 'Book',
        'subtype': 'ch',
        'dc:title': 'A chapter on things',
        'prism:publicationName': 'Handbook of Things',
        'prism:coverDate': '2009-01-01',
        'prism:doi': '10.1000/chapter',
        'prism:pageRange': '11-42',
    }, authors=AUTHORS, head={'source': {'isbn': {'$': '9780203881484'}}})
    expected = (
        "TY  - CHAP\nTI  - A chapter on things\nT2  - Handbook of Things\n"
        "DA  - 2009-01-01\nPY  - 2009\nAU  - Kitchin J.R.\n"
        "DO  - 10.1000/chapter\nUR  - https://doi.org/10.1000/chapter\n"
        "SP  - 11-42\nSN  - 9780203881484\nER  - \n\n"
    )
    assert ab.get_ris() == expected


def test_get_ris_conference_paper():
    ab = _make_abstract({
        'prism:aggregationType': 'Conference Proceeding',
        'subtype': 'cp',
        'dc:title': 'A conference paper',
        'prism:publicationName': 'Proceedings of the Conference',
        'prism:coverDate': '1995-12-01',
        'prism:volume': '2',
        'prism:pageRange': '1-4',
    }, authors=AUTHORS, head={'source': {
        'publisher': {'publishername': 'IEEE'},
    }})
    expected = (
        "TY  - CPAPER\nTI  - A conference paper\n"
        "T2  - Proceedings of the Conference\nDA  - 1995-12-01\n"
        "PY  - 1995\nAU  - Kitchin J.R.\nVL  - 2\nSP  - 1-4\n"
        "PB  - IEEE\nER  - \n\n"
    )
    assert ab.get_ris() == expected


def test_get_ris_conference_paper_in_book_series():
    ab = _make_abstract({
        'prism:aggregationType': 'Book Series',
        'subtype': 'cp',
        'dc:title': 'A conference paper',
        'prism:publicationName': 'Lecture Notes in Things',
        'prism:coverDate': '2020-01-01',
    }, authors=AUTHORS)
    assert ab.get_ris().startswith("TY  - CPAPER\nTI  - A conference paper\n"
                                   "T2  - Lecture Notes in Things\n")


def test_get_ris_missing_aggregation_type():
    ab = _make_abstract({
        'subtype': 'ar',
        'subtypeDescription': 'Article',
        'dc:title': 'An article without aggregation type',
        'prism:publicationName': 'Some Source',
    })
    expected = (
        "TY  - GEN\nTI  - An article without aggregation type\n"
        "T2  - Some Source\nER  - \n\n"
    )
    assert ab.get_ris() == expected

    ab = _make_abstract({'subtype': 'ch', 'dc:title': 'A chapter'})
    assert ab.get_ris() == "TY  - CHAP\nTI  - A chapter\nER  - \n\n"
