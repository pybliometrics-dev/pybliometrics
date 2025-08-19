from collections import namedtuple

from pybliometrics.scival.institution_metrics import InstitutionMetrics
from pybliometrics.utils.startup import init

init()

# Test cases with actual institution IDs from the response examples
single_institution_all = InstitutionMetrics("505023", by_year=False, refresh=30)
multiple_institutions_all = InstitutionMetrics([309054, 309086], by_year=True, refresh=30)
empty_metrics = InstitutionMetrics("0000000")


def test_academic_corporate_collaboration():
    """Test AcademicCorporateCollaboration property for all test cases."""
    result = single_institution_all.AcademicCorporateCollaboration
    
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.AcademicCorporateCollaboration
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_academic_corporate_collaboration_impact():
    """Test AcademicCorporateCollaborationImpact property for all test cases."""
    result = single_institution_all.AcademicCorporateCollaborationImpact
    if result and len(result) > 0:
        assert has_all_fields(result[0])


def test_all_metrics():
    """Test all_metrics property for all test cases."""
    MetricData = namedtuple('MetricData',
                            'entity_id entity_name metric metric_type year value percentage threshold',
                            defaults=(None, None, None, None, "all", None, None, None))

    result = single_institution_all.all_metrics
    expected_result_0 =MetricData(entity_id=505023,
                                  entity_name='Universidad Nacional Autónoma de México',
                                  metric='AcademicCorporateCollaboration',
                                  metric_type='Academic-corporate collaboration',
                                  year='all',
                                  value=951,
                                  percentage=2.31415,
                                  threshold=None)
    assert result[0] == expected_result_0
    assert len(result) >= 28

    result_multi = multiple_institutions_all.all_metrics
    expected_result_multi_last = MetricData(entity_id=309086,
                                            entity_name='Ludwig Maximilian University of Munich',
                                            metric='OutputsInTopCitationPercentiles',
                                            metric_type=None,
                                            year='2023',
                                            value=3792,
                                            percentage=38.50528,
                                            threshold=25)
    assert result_multi[-1] == expected_result_multi_last
    assert len(result_multi) >= 280


def test_institutions():
    """Test the institutions property for all test cases."""
    Institution = namedtuple('Institution', 'id name uri')

    # Test single institution
    institutions = single_institution_all.institutions
    if institutions and len(institutions) > 0:
        assert len(institutions) == 1
        expected_institution = Institution(id=505023,
                                           name='Universidad Nacional Autónoma de México',
                                           uri='Institution/505023')
        assert institutions[0] == expected_institution

    # Test multiple institutions
    institutions_multi = multiple_institutions_all.institutions
    if institutions_multi and len(institutions_multi) > 0:
        assert len(institutions_multi) == 2

        expected_institution_1 = Institution(id=309054,
                                             name='Technical University of Munich',
                                             uri='Institution/309054')
        assert institutions_multi[0] == expected_institution_1

    # Test empty metrics
    assert empty_metrics.institutions is None


def has_all_fields(metric_data):
    """Check if the metric data has all required fields."""
    required_fields = ['entity_id', 'entity_name', 'metric', 'metric_type', 'year', 'value', 'percentage', 'threshold']
    return all(hasattr(metric_data, field) for field in required_fields)


def test_citation_count():
    """Test CitationCount property for all test cases."""
    result = single_institution_all.CitationCount
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.CitationCount
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_citations_per_publication():
    """Test CitationsPerPublication property for all test cases."""
    result = single_institution_all.CitationsPerPublication
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.CitationsPerPublication
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_cited_publications():
    """Test CitedPublications property for all test cases."""
    result = single_institution_all.CitedPublications
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.CitedPublications
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_collaboration():
    """Test Collaboration property for all test cases."""
    result = single_institution_all.Collaboration
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.Collaboration
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_collaboration_impact():
    """Test CollaborationImpact property for all test cases."""
    result = single_institution_all.CollaborationImpact
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.CollaborationImpact
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_empty_metrics():
    """Test handling of empty metrics."""
    assert empty_metrics.all_metrics is None
    assert empty_metrics.institutions is None 
    assert empty_metrics.CitationCount is None
    assert empty_metrics.CitationsPerPublication is None
    assert empty_metrics.CitedPublications is None
    assert empty_metrics.Collaboration is None
    assert empty_metrics.CollaborationImpact is None


def test_field_weighted_citation_impact():
    """Test FieldWeightedCitationImpact property for all test cases."""
    result = single_institution_all.FieldWeightedCitationImpact
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.FieldWeightedCitationImpact
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_outputs_in_top_citation_percentiles():
    """Test OutputsInTopCitationPercentiles property for all test cases."""
    result = single_institution_all.OutputsInTopCitationPercentiles
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.OutputsInTopCitationPercentiles
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_publications_in_top_journal_percentiles():
    """Test PublicationsInTopJournalPercentiles property for all test cases."""
    result = single_institution_all.PublicationsInTopJournalPercentiles
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.PublicationsInTopJournalPercentiles
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_scholarly_output():
    """Test ScholarlyOutput property for all test cases."""
    result = single_institution_all.ScholarlyOutput
    if result and len(result) > 0:
        assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.ScholarlyOutput
    if result_multi and len(result_multi) > 0:
        assert has_all_fields(result_multi[0])


def test_str_representation():
    """Test the string representation of InstitutionMetrics objects."""
    # Test single institution
    str_single = str(single_institution_all)
    expected_str = "InstitutionMetrics for 1 institution(s):\n- Universidad Nacional Autónoma de México (ID: 505023)"
    assert str_single == expected_str

    # Test multiple institutions
    str_multi = str(multiple_institutions_all)
    expected_str_multi = "InstitutionMetrics for 2 institution(s):\n- Technical University of Munich (ID: 309054)\n- Ludwig Maximilian University of Munich (ID: 309086)"
    assert str_multi == expected_str_multi

    # Test empty metrics
    str_empty = str(empty_metrics)
    assert str_empty == "No institutions found"
