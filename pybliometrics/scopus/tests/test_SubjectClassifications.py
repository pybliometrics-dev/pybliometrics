"""Tests for `scopus.SubjectClassifications` module."""

from pybliometrics.scopus import SubjectClassifications, init

init()


# Search by words in subject description
sub1 = SubjectClassifications({'description': 'Physics'}, refresh=30)
# Search by subject code
sub2 = SubjectClassifications({'code': '2613'}, refresh=30)
# Search by words in subject detail
sub3 = SubjectClassifications({'detail': 'Processes'}, refresh=30)
# Search by subject abbreviation
sub4 = SubjectClassifications({'abbrev': 'MATH'}, refresh=30)
# Search by multiple criteria
sub5 = SubjectClassifications({'description': 'Engineering', 'detail': 'Fluid'}, refresh=30)
# Search by multiple criteria, subset returned fields
sub6 = SubjectClassifications({'detail': 'Analysis', 'description': 'Mathematics'},
                              fields=['description', 'detail'], refresh=30)


def test_results_desc():
    assert len(sub1.results) > 0
    assert all(['Physics' in res.description for res in sub1.results])


def test_results_code():
    assert len(sub2.results) == 1
    assert sub2.results[0].code == '2613'
    

def test_results_detail():
    assert len(sub3.results) > 0
    assert all(['Processes' in res.detail for res in sub3.results])


def test_results_abbrev():
    assert len(sub4.results) > 0
    assert all(['MATH' in res.abbrev for res in sub4.results])


def test_results_multi():
    assert len(sub5.results) > 0
    assert all(['Engineering' in res.description for res in sub5.results])
    assert all(['Fluid' in res.detail for res in sub5.results])
    

def test_results_fields():
    assert len(sub6.results) > 0
    assert all(['Mathematics' in res.description for res in sub6.results])
    assert all(['Analysis' in res.detail for res in sub6.results])
    assert all([set(res._fields) == set(['description', 'detail']) for res in sub6.results])
