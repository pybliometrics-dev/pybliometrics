"""Tests for `scopus.SerialTitleSearch` module."""

from pybliometrics.scopus import SerialTitleSearch, init

init()


# Search by title
ser1 = SerialTitleSearch({'title': 'SoftwareX'}, refresh=30)
# Search by ISSN
ser2 = SerialTitleSearch({'issn': '1468-0262'}, refresh=30)
# Search by publisher
ser3 = SerialTitleSearch({'pub': 'Stellenbosch'}, refresh=30)
# Search by subject abbreviation
ser4 = SerialTitleSearch({'subj': 'COMP'}, refresh=30)
# Search by subject area code
ser5 = SerialTitleSearch({'subjCode': '2612'}, refresh=30)


def test_deprecated_class():
    from pytest import deprecated_call
    from pybliometrics.scopus import SerialSearch

    with deprecated_call():
        _ = SerialSearch({'title': 'SoftwareX'}, refresh=30)


def test_results_title():
    assert len(ser1.results) == 1
    assert ser1.results[0]['title'] == 'SoftwareX'


def test_results_issn():
    assert len(ser2.results) == 1
    assert ser2.results[0]['title'] == 'Econometrica'


def test_results_pub():
    assert len(ser3.results) == 5
    assert ser3.results[0]['title'] == 'African Finance Journal'


def test_results_subj():
    ser4_subj_abbs = set(i['subject_area_abbrevs'] for i in ser4.results)
    assert False not in ['COMP' in i for i in ser4_subj_abbs]


def test_results_subjcode():
    ser5_subj_codes = set(i['subject_area_codes'] for i in ser5.results)
    assert False not in ['2612' in i for i in ser5_subj_codes]
