from collections import namedtuple

from pybliometrics.scival import init, InstitutionMetrics

init()

# Test cases with actual institution IDs from the response examples
single_institution_all = InstitutionMetrics("505023", by_year=False, refresh=30)
multiple_institutions_all = InstitutionMetrics([309054, 309086], by_year=True, refresh=30)
empty_metrics = InstitutionMetrics("0000000")


# Auxiliary function to check if a MetricData namedtuple has all required fields
def has_all_fields(metric_data):
    """Check if the metric data has all required fields."""
    required_fields = ['entity_id', 'entity_name', 'metric',
                       'metric_type', 'year', 'value', 'percentage',
                       'threshold']
    return all(hasattr(metric_data, field) for field in required_fields)


def test_academic_corporate_collaboration():
    """Test AcademicCorporateCollaboration property for all test cases."""
    result = single_institution_all.AcademicCorporateCollaboration
    assert has_all_fields(result[0])
    assert result[0].entity_id == 505023
    assert result[0].entity_name == 'Universidad Nacional Autónoma de México'
    assert result[0].metric == 'Academic-corporate collaboration'
    assert result[0].metric_type == 'AcademicCorporateCollaboration'
    assert result[0].year == 'all'
    assert result[0].value >= 900
    assert result[0].percentage > 2
    assert result[0].threshold is None

    result_multi = multiple_institutions_all.AcademicCorporateCollaboration
    assert has_all_fields(result_multi[0])
    assert result_multi[0].entity_id == 309054
    assert result_multi[0].entity_name == 'Technical University of Munich'
    assert result_multi[0].metric == 'Academic-corporate collaboration'
    assert result_multi[0].metric_type == 'AcademicCorporateCollaboration'
    assert result_multi[0].year == '2024'
    assert result_multi[0].value >= 1000
    assert result_multi[0].percentage > 9
    assert result_multi[0].threshold is None


def test_academic_corporate_collaboration_impact():
    """Test AcademicCorporateCollaborationImpact property for all test cases."""
    result = single_institution_all.AcademicCorporateCollaborationImpact
    assert has_all_fields(result[0])


def test_institutions():
    """Test the institutions property for all test cases."""
    Institution = namedtuple('Institution', 'id name uri')

    # Test single institution
    institutions = single_institution_all.institutions
    assert len(institutions) == 1
    expected_institution = Institution(id=505023,
                                        name='Universidad Nacional Autónoma de México',
                                        uri='Institution/505023')
    assert institutions[0] == expected_institution

    # Test multiple institutions
    institutions_multi = multiple_institutions_all.institutions
    assert len(institutions_multi) == 2

    expected_institution_1 = Institution(id=309054,
                                            name='Technical University of Munich',
                                            uri='Institution/309054')
    assert institutions_multi[0] == expected_institution_1

    # Test empty metrics
    assert empty_metrics.institutions is None


def test_citation_count():
    """Test CitationCount property for all test cases."""
    result = single_institution_all.CitationCount
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.CitationCount
    assert has_all_fields(result_multi[0])


def test_citations_per_publication():
    """Test CitationsPerPublication property for all test cases."""
    result = single_institution_all.CitationsPerPublication
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.CitationsPerPublication
    assert has_all_fields(result_multi[0])


def test_cited_publications():
    """Test CitedPublications property for all test cases."""
    result = single_institution_all.CitedPublications
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.CitedPublications
    assert has_all_fields(result_multi[0])


def test_collaboration():
    """Test Collaboration property for all test cases."""
    result = single_institution_all.Collaboration
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.Collaboration
    assert has_all_fields(result_multi[0])


def test_collaboration_impact():
    """Test CollaborationImpact property for all test cases."""
    result = single_institution_all.CollaborationImpact
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.CollaborationImpact
    assert has_all_fields(result_multi[0])


def test_empty_metrics():
    """Test handling of empty metrics."""
    assert empty_metrics.institutions is None 
    assert empty_metrics.CitationCount is None
    assert empty_metrics.CitationsPerPublication is None
    assert empty_metrics.CitedPublications is None
    assert empty_metrics.Collaboration is None
    assert empty_metrics.CollaborationImpact is None


def test_field_weighted_citation_impact():
    """Test FieldWeightedCitationImpact property for all test cases."""
    result = single_institution_all.FieldWeightedCitationImpact
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.FieldWeightedCitationImpact
    assert has_all_fields(result_multi[0])


def test_outputs_in_top_citation_percentiles():
    """Test OutputsInTopCitationPercentiles property for all test cases."""
    result = single_institution_all.OutputsInTopCitationPercentiles
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.OutputsInTopCitationPercentiles
    
    assert has_all_fields(result_multi[0])


def test_publications_in_top_journal_percentiles():
    """Test PublicationsInTopJournalPercentiles property for all test cases."""
    result = single_institution_all.PublicationsInTopJournalPercentiles
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.PublicationsInTopJournalPercentiles
    assert has_all_fields(result_multi[0])


def test_scholarly_output():
    """Test ScholarlyOutput property for all test cases."""
    result = single_institution_all.ScholarlyOutput
    assert has_all_fields(result[0])

    result_multi = multiple_institutions_all.ScholarlyOutput
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
