"""Tests for sciencedirect.ScienceDirectSearch"""
from collections import namedtuple

from pybliometrics.exception import Scopus400Error
from pybliometrics.sciencedirect import ScienceDirectSearch, init

init()

sds_standard = ScienceDirectSearch('TITLE("Assessing LLMs in malicious code deobfuscation of real-world malware campaigns") AND DATE(2012)', view="STANDARD", refresh=30)
sds_empty = ScienceDirectSearch('TITLE("Not a very realistic title")', view="STANDARD", refresh=30)


def test_empty_results():
    assert sds_empty.results is None
    assert sds_empty._n == 0


def test_all_fields():
    fields = 'authors first_author doi title link load_date openaccess_status pii '\
        'coverDate endingPage publicationName startingPage api_link volume'
    doc = namedtuple("Document", fields)

    expected_standard_doc = doc(
        authors="Constantinos Patsakis;Fran Casino;Nikolaos Lykousas",
        first_author="Constantinos Patsakis",
        doi="10.1016/j.eswa.2024.124912",
        title="Assessing LLMs in malicious code deobfuscation of real-world malware campaigns",
        link="https://www.sciencedirect.com/science/article/pii/S0957417424017792?dgcid=api_sd_search-api-endpoint",
        load_date="2024-07-31T00:00:00.000Z",
        openaccess_status=True,
        pii="S0957417424017792",
        coverDate="2024-12-05",
        endingPage=None,
        publicationName="Expert Systems with Applications",
        startingPage="124912",
        api_link="https://api.elsevier.com/content/article/pii/S0957417424017792",
        volume="256",
    )
    assert sds_standard.results[0] == expected_standard_doc


def test_field_consistency():
    am_wrong_field = ScienceDirectSearch('TITLE("Assessing LLMs in malicious code deobfuscation of real-world malware campaigns") AND DATE(2012)',
                                 integrity_fields=["notExistingField"],
                                 integrity_action="warn",
                                 view="STANDARD",
                                 refresh=30)
    try:
        am_wrong_field.results
    except ValueError:
        pass
    except Exception as e:
        raise AssertionError(f"Unexpected exception type: {type(e).__name__}")
    else:
        raise AssertionError("Expected ValueError but no exception was raised")


def test_length():
    assert len(sds_standard.results) == sds_standard._n
    assert len(sds_standard.results) == sds_standard._n


def test_string():
    str_start = ('Search \'TITLE("Assessing LLMs in malicious code deobfuscation of '
    'real-world malware campaigns") AND DATE(2012)\' yielded 1 document as of')
    assert sds_standard.__str__().startswith(str_start)


def test_wrong_query():
    try:
        ScienceDirectSearch(
            'Th(s querY - has M&ny ( Errors', view="STANDARD", refresh=30
        )
    except Scopus400Error:
        pass
    except Exception as e:
        raise AssertionError(f"Unexpected exception type: {type(e).__name__}")
    else:
        raise AssertionError("Expected Scopus400Error but no exception was raised")
