"""Offline tests for `abstract_retrieval._get_ris_type()`; they require
neither an API key nor a network connection.
"""

import pytest

from pybliometrics.scopus.abstract_retrieval import _get_ris_type


@pytest.mark.parametrize(
    "aggregation_type, subtype, expected",
    [
        ("Journal", "ar", "JOUR"),
        ("Journal", "re", "JOUR"),
        ("Trade Journal", "ar", "JOUR"),
        ("Report", None, "RPRT"),
        ("Conference Proceeding", "cp", "CPAPER"),
        ("Conference Proceeding", None, "CPAPER"),
        ("Book", "bk", "BOOK"),
        ("Book", "ch", "CHAP"),
        ("Book", None, "CHAP"),
        ("Book Series", "ch", "CHAP"),
        ("Book Series", None, "CHAP"),
        (None, "cp", "CPAPER"),
        (None, "bk", "BOOK"),
        (None, "ch", "CHAP"),
        ("Other", "xx", "GEN"),
        (None, None, "GEN"),
    ],
)
def test_get_ris_type(aggregation_type, subtype, expected):
    assert _get_ris_type(aggregation_type, subtype) == expected
