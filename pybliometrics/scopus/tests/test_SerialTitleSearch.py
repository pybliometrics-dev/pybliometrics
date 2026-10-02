"""Tests for `scopus.SerialTitleSearch` module."""

from pybliometrics.scopus import SerialTitleSearch, init

init()


# Search by title
ser1 = SerialTitleSearch({'title': 'SoftwareX'}, refresh=30)
# Search by ISSN
ser2 = SerialTitleSearch({'issn': '1468-0262'}, refresh=30)
# Search by publisher
ser3 = SerialTitleSearch({'pub': 'Stellenbosch'}, refresh=30)
# Search by subject area code
ser4 = SerialTitleSearch(query={'subjCode': '2708', 'content': 'journal'}, refresh=30)

def test_deprecated_class():
    from pytest import deprecated_call
    from pybliometrics.scopus import SerialSearch

    with deprecated_call():
        _ = SerialSearch({'title': 'SoftwareX'}, refresh=30)


def test_results_title():
    assert len(ser1.results) == 1
    assert ser1.results[0]['title'] == 'SoftwareX'
    assert ser1.get_results_size() == 1


def test_results_issn():
    assert len(ser2.results) == 1
    assert ser2.results[0]['title'] == 'Econometrica'
    assert ser1.get_results_size() == 1


def test_results_pub():
    assert len(ser3.results) == 4
    assert ser3.results[0]['title'] == 'Akroterion'
    assert ser3.get_results_size() == 4


def test_results_subjcode():
    ser4_subj_codes = set(i['subject_area_codes'] for i in ser4.results)
    assert False not in ['2708' in i for i in ser4_subj_codes]
    assert ser4.get_results_size() >= 260
