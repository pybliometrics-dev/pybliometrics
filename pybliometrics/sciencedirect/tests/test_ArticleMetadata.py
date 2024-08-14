"""Tests for sciencedirect.ArticleMetadata"""
from collections import namedtuple

from pybliometrics.exception import Scopus400Error
from pybliometrics.sciencedirect import ArticleMetadata, init

init()

am_standard = ArticleMetadata('TITLE("Bayesian Network") AND YEAR(2015)',
                              view="STANDARD",
                              refresh=30)
am_complete = ArticleMetadata('AFFIL("MIT") AND YEAR("2023") AND DOI(10.1016/B978-0-32-399851-2.00030-2)',
                              view="COMPLETE",
                              refresh=30)
am_empty = ArticleMetadata('TITLE("Not a very realistic title")', view="STANDARD", refresh=30)


def test_empty_results():
    assert am_empty.results is None
    assert am_empty._n == 0


def test_all_fields():
    fields = (
        "authorKeywords authors available_online_date first_author abstract_text "
        "doi title eid link openArchiveArticle openaccess_status openaccessArticle "
        "openaccessUserLicense pii aggregationType copyright coverDate coverDisplayDate "
        "edition endingPage isbn publicationName startingPage teaser api_link publicationType "
        "vor_available_online_date"
    )
    doc = namedtuple("Document", fields)

    expected_complete_doc = doc(
        authorKeywords="Large scale learning | Few shot learning | Meta learning",
        authors="Balaji, Yogesh",
        available_online_date="2022-09-30",
        first_author="Sankaranarayanan, Swami",
        abstract_text="Meta learning techniques have been successfully used to mitigate issues such as distribution shift in neural network training. However, the proposed approaches remain complex to train and less scalable. In this chapter, we discuss some recent approaches that have successfully demonstrated the use of meta learning based techniques in a big data setting such as Imagenet and beyond.",
        doi="10.1016/B978-0-32-399851-2.00030-2",
        title="Meta learning in the big data regime Applications to transfer learning and few shot learning",
        eid="3-s2.0-B9780323998512000302",
        link="https://www.sciencedirect.com/science/article/pii/B9780323998512000302",
        openArchiveArticle=False,
        openaccess_status="0",
        openaccessArticle=False,
        openaccessUserLicense=None,
        pii="B978-0-32-399851-2.00030-2",
        aggregationType="EBook",
        copyright="Copyright © 2023 Elsevier Inc. All rights reserved.",
        coverDate="2023-12-31",
        coverDisplayDate="2023",
        edition=None,
        endingPage="393",
        isbn="9780323998512",
        publicationName="Meta Learning With Medical Imaging and Health Informatics Applications",
        startingPage="385",
        teaser="Meta learning techniques have been successfully used to mitigate issues such as distribution shift in neural network training. However, the proposed approaches remain complex to train and less scalable....",
        api_link="https://api.elsevier.com/content/article/pii/B9780323998512000302",
        publicationType="chp",
        vor_available_online_date="2022-09-30",
    )
    assert am_complete.results[0] == expected_complete_doc

    expected_standard_doc = doc(
        authorKeywords=None,
        authors="Zhong, Lu;Haijun, Zeng",
        available_online_date="2015-02-14",
        first_author="Kang, Chen",
        abstract_text=None,
        doi="10.1016/j.proeng.2014.12.523",
        title="Research on Probabilistic Safety Analysis Approach of Flight Control System Based on Bayesian Network",
        eid="1-s2.0-S1877705814036376",
        link="https://www.sciencedirect.com/science/article/pii/S1877705814036376",
        openArchiveArticle=False,
        openaccess_status="1",
        openaccessArticle=True,
        openaccessUserLicense="http://creativecommons.org/licenses/by-nc-nd/4.0/",
        pii="S1877-7058(14)03637-6",
        aggregationType=None,
        copyright=None,
        coverDate="2015-12-31",
        coverDisplayDate="2015",
        edition=None,
        endingPage="184",
        isbn=None,
        publicationName="Procedia Engineering",
        startingPage="180",
        teaser="Traditional probabilistic safety analysis methods are not suitable for modern flight control system with multi-state probability. In this papera Bayesian Network based probabilistic safety model is...",
        api_link="https://api.elsevier.com/content/article/pii/S1877705814036376",
        publicationType="fla",
        vor_available_online_date=None,
    )
    assert am_standard.results[0] == expected_standard_doc


def test_field_consistency():
    am_wrong_field = ArticleMetadata('TITLE("Bayesian Network") AND YEAR(2015)',
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
    assert len(am_standard.results) == am_standard._n
    assert len(am_complete.results) == am_complete._n


def test_string():
    part_of_str = 'Search \'AFFIL("MIT") AND YEAR("2023") AND DOI(10.1016/B978-0-32-399851-2.00030-2)\' yielded 1 document as of'
    assert part_of_str in am_complete.__str__()


def test_wrong_query():
    try:
        ArticleMetadata(
            'TITLE("Bayesian Network") AND YEAR(2015', view="STANDARD", refresh=30
        )
    except Scopus400Error:
        pass
    except Exception as e:
        raise AssertionError(f"Unexpected exception type: {type(e).__name__}")
    else:
        raise AssertionError("Expected Scopus400Error but no exception was raised")
