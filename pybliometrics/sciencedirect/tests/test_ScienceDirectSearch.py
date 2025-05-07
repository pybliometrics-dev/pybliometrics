"""Tests for sciencedirect.ScienceDirectSearch"""
from collections import namedtuple

import pytest

from pybliometrics.exception import ScopusQueryError
from pybliometrics.sciencedirect import ScienceDirectSearch, init

init()

one_article_query = {'title': 'Assessing LLMs in malicious code deobfuscation of real-world malware campaigns',
                     'date': '2024'}
sds_standard = ScienceDirectSearch(one_article_query, refresh=30)

empty_query = {'title': 'Not a realistic title', 'date': '2012'}
sds_empty = ScienceDirectSearch(empty_query, view="STANDARD", refresh=30)

huge_query = {'qs': 'Neural Networks', 'date': '2015-2020'}
sds_huge = ScienceDirectSearch(huge_query, view="STANDARD", download=False, refresh=30)

pagination_query = {'qs': '"Neural Networks" AND "Shapley"', 'date': '2020'}
sds_pagination = ScienceDirectSearch(pagination_query, view="STANDARD", refresh=30)

def test_all_fields():
    fields = 'authors doi loadDate openAccess first_page last_page pii publicationDate ' \
             'sourceTitle title uri volumeIssue'
    doc = namedtuple('Document', fields)

    expected_standard_doc = doc(
        authors='Constantinos Patsakis; Fran Casino; Nikolaos Lykousas',
        doi='10.1016/j.eswa.2024.124912',
        loadDate="2024-07-31T00:00:00.000Z",
        openAccess=True,
        first_page=124912,
        last_page=None,
        pii='S0957417424017792',
        publicationDate='2024-12-05',
        sourceTitle='Expert Systems with Applications',
        title='Assessing LLMs in malicious code deobfuscation of real-world malware campaigns',
        uri='https://www.sciencedirect.com/science/article/pii/S0957417424017792?dgcid=api_sd_search-api-endpoint',
        volumeIssue='Volume 256'
    )

    assert sds_standard.results[0] == expected_standard_doc

    expected_last_document = doc(
        authors='Elhadji Amadou Oury Diallo; Ayumi Sugiyama; Toshiharu Sugawara',
        doi='10.1016/j.neucom.2018.08.094',
        loadDate='2019-04-25T00:00:00.000Z',
        openAccess=False,
        first_page=230,
        last_page=240,
        pii='S0925231219304424',
        publicationDate='2020-07-05',
        sourceTitle='Neurocomputing',
        title='Coordinated behavior of cooperative agents using deep reinforcement learning',
        uri='https://www.sciencedirect.com/science/article/pii/S0925231219304424?dgcid=api_sd_search-api-endpoint',
        volumeIssue='Volume 396'
    )
    assert sds_pagination.results[-1] == expected_last_document


def test_empty_results():
    assert sds_empty.results is None
    assert sds_empty._n == 0


def test_field_consistency():
    am_wrong_field = ScienceDirectSearch(one_article_query,
                                 integrity_fields=["notExistingField"],
                                 integrity_action="warn",
                                 view="STANDARD",
                                 refresh=30)
    with pytest.raises(ValueError):
        _ = am_wrong_field.results


def test_large_results():
    with pytest.raises(ScopusQueryError):
        _ = ScienceDirectSearch(huge_query, view="STANDARD", download=True, refresh=30)


def test_length():
    assert len(sds_standard.results) == sds_standard._n
    assert len(sds_standard.results) == sds_standard._n
    assert sds_huge.get_results_size() > 156_000
    assert len(sds_pagination.results) == 127


def test_string():
    expected_str = "Search '{'title': 'Assessing LLMs in malicious code deobfuscation of real-world malware campaigns', 'date': '2024'}' yielded 1 document as of 2025-05-07:\n    10.1016/j.eswa.2024.124912"
    assert str(sds_standard) == expected_str
