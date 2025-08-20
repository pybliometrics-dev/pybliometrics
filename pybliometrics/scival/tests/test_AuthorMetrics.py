from collections import namedtuple

from pybliometrics.scival.author_metrics import AuthorMetrics
from pybliometrics.utils.startup import init

init()

# Test cases as specified
single_author_all = AuthorMetrics("6602819806", by_year=False, refresh=30)
single_author_h_index = AuthorMetrics("6602819806", metric_types=["HIndices"], by_year=False, refresh=30)
multiple_authors_all = AuthorMetrics([7201667143, 6603480302], by_year=True, refresh=30)
empty_metrics = AuthorMetrics("0000000000")


def test_academic_corporate_collaboration():
    """Test AcademicCorporateCollaboration property for all test cases."""
    result = single_author_all.AcademicCorporateCollaboration

    assert has_all_fields(result[0])
    assert single_author_h_index.AcademicCorporateCollaboration is None

    result_multi = multiple_authors_all.AcademicCorporateCollaboration
    assert has_all_fields(result_multi[0])


def test_academic_corporate_collaboration_impact():
    """Test AcademicCorporateCollaborationImpact property for all test cases."""
    result = single_author_all.AcademicCorporateCollaborationImpact
    assert has_all_fields(result[0])
    assert single_author_h_index.AcademicCorporateCollaborationImpact is None

    result_multi = multiple_authors_all.AcademicCorporateCollaborationImpact
    assert has_all_fields(result_multi[0])


def test_all_metrics():
    """Test all_metrics property for all test cases."""
    MetricData = namedtuple('MetricData',
                            'entity_id entity_name metric metric_type year value percentage threshold',
                            defaults=(None, None, None, None, "all", None, None, None))

    single_author_all_metrics = single_author_all.all_metrics
    assert len(single_author_all_metrics) == 29
    expected_first_metric = MetricData(entity_id=6602819806,
                                       entity_name='Algül, Hana',
                                       metric='Academic-corporate collaboration',
                                       metric_type='AcademicCorporateCollaboration',
                                       year='all',
                                       value=12,
                                       percentage=22.64151,
                                       threshold=None)
    assert expected_first_metric == single_author_all_metrics[0]


    single_author_h_index_all_metrics = single_author_h_index.all_metrics
    assert len(single_author_h_index_all_metrics) == 1
    expected_h_index = MetricData(entity_id=6602819806,
                                  entity_name='Algül, Hana',
                                  metric='h-index',
                                  metric_type='HIndices',
                                  year='all', value=46.0,
                                  percentage=None,
                                  threshold=None)
    assert expected_h_index == single_author_h_index_all_metrics[0]


    multiple_authors_all_metrics = multiple_authors_all.all_metrics
    assert len(multiple_authors_all_metrics) == 280
    expected_multi_metric = MetricData(entity_id=6603480302,
                                       entity_name='Vogel-Heuser, Birgit',
                                       metric='Academic-corporate collaboration',
                                       metric_type='AcademicCorporateCollaboration',
                                       year='2024',
                                       value=8,
                                       percentage=21.052631,
                                       threshold=None)
    assert expected_multi_metric == multiple_authors_all_metrics[10]


def test_authors():
    """Test the authors property for all test cases with actual values."""
    # Test single author with all metrics
    authors = single_author_all.authors
    assert len(authors) == 1
    assert authors[0].id == 6602819806
    assert authors[0].name == "Algül, Hana"
    assert authors[0].uri == "Author/6602819806"

    # Test single author with H-indices only
    authors_h = single_author_h_index.authors
    assert len(authors_h) == 1
    assert authors_h[0].id == 6602819806
    assert authors_h[0].name == "Algül, Hana"
    assert authors_h[0].uri == "Author/6602819806"

    # Test multiple authors with actual names and IDs
    authors_multi = multiple_authors_all.authors
    assert len(authors_multi) == 2

    # Sort by ID and test
    authors_sorted = sorted(authors_multi, key=lambda x: x.id)

    assert authors_sorted[0].id == 6603480302
    assert authors_sorted[0].name == "Vogel-Heuser, Birgit"
    assert authors_sorted[0].uri == "Author/6603480302"

    assert authors_sorted[1].id == 7201667143
    assert authors_sorted[1].name == "Wolff, Klaus Dietrich"
    assert authors_sorted[1].uri == "Author/7201667143"


def has_all_fields(metric_data):
    """Check if the metric data has all required fields."""
    required_fields = ['entity_id', 'entity_name', 'metric', 'metric_type', 'year', 'value', 'percentage', 'threshold']
    return all(hasattr(metric_data, field) for field in required_fields)


def test_citation_count():
    """Test CitationCount property for all test cases."""
    result = single_author_all.CitationCount
    assert has_all_fields(result[0])
    assert single_author_h_index.CitationCount is None

    result_multi = multiple_authors_all.CitationCount
    assert has_all_fields(result_multi[0])


def test_citations_per_publication():
    """Test CitationsPerPublication property for all test cases."""
    result = single_author_all.CitationsPerPublication
    assert has_all_fields(result[0])
    assert single_author_h_index.CitationsPerPublication is None

    result_multi = multiple_authors_all.CitationsPerPublication
    assert has_all_fields(result_multi[0])


def test_cited_publications():
    """Test CitedPublications property for all test cases."""
    result = single_author_all.CitedPublications
    assert has_all_fields(result[0])
    assert single_author_h_index.CitedPublications is None

    result_multi = multiple_authors_all.CitedPublications
    assert has_all_fields(result_multi[0])


def test_collaboration():
    """Test Collaboration property for all test cases."""
    result = single_author_all.Collaboration
    assert has_all_fields(result[0])
    assert single_author_h_index.Collaboration is None

    result_multi = multiple_authors_all.Collaboration
    assert has_all_fields(result_multi[0])


def test_collaboration_impact():
    """Test CollaborationImpact property for all test cases."""
    result = single_author_all.CollaborationImpact
    assert has_all_fields(result[0])
    assert single_author_h_index.CollaborationImpact is None

    result_multi = multiple_authors_all.CollaborationImpact
    assert has_all_fields(result_multi[0])


def test_empty_metrics():
    """Test handling of empty metric_types."""
    assert empty_metrics.all_metrics is None
    assert empty_metrics.authors is None 
    assert empty_metrics.CitationCount is None
    assert empty_metrics.CitationsPerPublication is None
    assert empty_metrics.CitedPublications is None
    assert empty_metrics.Collaboration is None
    assert empty_metrics.CollaborationImpact is None


def test_field_weighted_citation_impact():
    """Test FieldWeightedCitationImpact property for all test cases."""
    result = single_author_all.FieldWeightedCitationImpact
    assert has_all_fields(result[0])
    assert single_author_h_index.FieldWeightedCitationImpact is None

    result_multi = multiple_authors_all.FieldWeightedCitationImpact
    assert has_all_fields(result_multi[0])


def test_h_indices():
    """Test HIndices property for all test cases."""
    result = single_author_all.HIndices
    assert has_all_fields(result[0])

    result_h = single_author_h_index.HIndices
    assert has_all_fields(result_h[0])

    # HIndices are not available by year
    assert multiple_authors_all.HIndices is None


def test_outputs_in_top_citation_percentiles():
    """Test OutputsInTopCitationPercentiles property for all test cases."""
    result = single_author_all.OutputsInTopCitationPercentiles
    assert has_all_fields(result[0])
    assert single_author_h_index.OutputsInTopCitationPercentiles is None

    result_multi = multiple_authors_all.OutputsInTopCitationPercentiles
    assert has_all_fields(result_multi[0])


def test_publications_in_top_journal_percentiles():
    """Test PublicationsInTopJournalPercentiles property for all test cases."""
    result = single_author_all.PublicationsInTopJournalPercentiles
    assert has_all_fields(result[0])
    assert single_author_h_index.PublicationsInTopJournalPercentiles is None

    result_multi = multiple_authors_all.PublicationsInTopJournalPercentiles
    assert has_all_fields(result_multi[0])


def test_scholarly_output():
    """Test ScholarlyOutput property for all test cases."""
    result = single_author_all.ScholarlyOutput
    assert has_all_fields(result[0])
    assert single_author_h_index.ScholarlyOutput is None

    result_multi = multiple_authors_all.ScholarlyOutput
    assert has_all_fields(result_multi[0])


def test_str_representation():
    """Test the string representation of AuthorMetrics objects using actual results."""
    # Test single author with all metrics
    str_single = str(single_author_all)
    expected_single = "AuthorMetrics for 1 author(s):\n- Algül, Hana (ID: 6602819806)"
    assert str_single == expected_single

    # Test single author with H-indices only
    str_h_index = str(single_author_h_index)
    expected_h_index = "AuthorMetrics for 1 author(s):\n- Algül, Hana (ID: 6602819806)"
    assert str_h_index == expected_h_index

    # Test multiple authors
    str_multiple = str(multiple_authors_all)
    expected_multiple = "AuthorMetrics for 2 author(s):\n- Wolff, Klaus Dietrich (ID: 7201667143)\n- Vogel-Heuser, Birgit (ID: 6603480302)"
    assert str_multiple == expected_multiple

    # Test empty metrics
    str_empty = str(empty_metrics)
    expected_empty = "No authors found"
    assert str_empty == expected_empty
