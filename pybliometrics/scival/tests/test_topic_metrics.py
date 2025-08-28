from pytest import approx
from pybliometrics.scival import TopicMetrics, init

init()

topic = TopicMetrics("9549", by_year=False, refresh=30)
topics_by_year = TopicMetrics("110, 1438, 1012", by_year=True, refresh=30)
topics_not_by_year = TopicMetrics(["3909", "4374"], by_year=False, refresh=30)
specific_metrics = TopicMetrics("1516, 2848",
                                metric_types=["AuthorCount", "CitationCount"],
                                by_year=False, refresh=30)
non_existing = TopicMetrics("9999999999", by_year=False, refresh=30)

def test_topics():
    """Tests topics property"""
    expected_fields = ("id", "name", "uri", "prominencePercentile", "scholarlyOutput")

    assert len(topic.topics) == 1
    assert topic.topics[0]._fields == expected_fields
    assert topic.topics[0].id == 9549
    assert topic.topics[0].name == "Quantum States and Entanglement in Many-Body Systems"
    assert topic.topics[0].uri == "Topic/9549"
    assert topic.topics[0].prominencePercentile == approx(94, abs=10)
    assert topic.topics[0].scholarlyOutput == approx(822, rel=0.1)

    assert len(topics_by_year.topics) == 3
    assert topics_by_year.topics[0]._fields == expected_fields

    assert len(topics_not_by_year.topics) == 2
    assert topics_not_by_year.topics[0]._fields == expected_fields

    assert len(specific_metrics.topics) == 2
    assert specific_metrics.topics[0]._fields == expected_fields

    assert len(non_existing.topics) == 0

def test_author_count():
    """Test AuthorCount property"""
    expected_fields = ("entity_id", "entity_name", "metric", "year", "value", "percentage", "threshold")

    assert len(topic.AuthorCount) == 1
    assert topic.AuthorCount[0]._fields == expected_fields

    assert len(topics_by_year.AuthorCount) == 15
    assert topics_by_year.AuthorCount[0]._fields == expected_fields
    assert topics_by_year.AuthorCount[0].entity_id == 110
    assert topics_by_year.AuthorCount[0].entity_name == "Photoacoustic Imaging Techniques for Enhanced Tissue Analysis"
    assert topics_by_year.AuthorCount[0].metric == "AuthorCount"
    assert topics_by_year.AuthorCount[0].year == "2020"
    assert topics_by_year.AuthorCount[0].value == approx(1997, rel=0.1)
    assert topics_by_year.AuthorCount[0].percentage is None
    assert topics_by_year.AuthorCount[0].threshold is None

    assert len(topics_not_by_year.AuthorCount) == 2
    assert topics_not_by_year.AuthorCount[0]._fields == expected_fields

    assert len(specific_metrics.AuthorCount) == 2
    assert specific_metrics.AuthorCount[0]._fields == expected_fields

    assert non_existing.AuthorCount is None


def test_citation_count():
    """Test CitationCount property"""
    expected_fields = ("entity_id", "entity_name", "metric", "year", "value", "percentage", "threshold")

    assert len(topic.CitationCount) == 1
    assert topic.CitationCount[0]._fields == expected_fields

    assert len(topics_by_year.CitationCount) == 15
    assert topics_by_year.CitationCount[0]._fields == expected_fields

    assert len(topics_not_by_year.CitationCount) == 2
    assert topics_not_by_year.CitationCount[0]._fields == expected_fields
    assert topics_not_by_year.CitationCount[0].entity_id == 3909
    assert topics_not_by_year.CitationCount[0].entity_name == "Point Cloud Semantic Segmentation"
    assert topics_not_by_year.CitationCount[0].metric == "CitationCount"
    assert topics_not_by_year.CitationCount[0].year == "all"
    assert topics_not_by_year.CitationCount[0].value == approx(84184, rel=0.1)
    assert topics_not_by_year.CitationCount[0].percentage is None
    assert topics_not_by_year.CitationCount[0].threshold is None

    assert len(specific_metrics.CitationCount) == 2
    assert specific_metrics.CitationCount[0]._fields == expected_fields

    assert non_existing.CitationCount is None


def test_core_papers():
    """Test CorePapers property"""
    expected_fields = ('entity_id', 'entity_name', 'publication_id')

    assert len(topic.CorePapers) == 10
    assert topic.CorePapers[0]._fields == expected_fields

    assert topics_by_year.CorePapers is None

    assert len(topics_not_by_year.CorePapers) == 20
    assert topics_not_by_year.CorePapers[0]._fields == expected_fields
    assert topics_not_by_year.CorePapers[0].entity_id == 3909
    assert topics_not_by_year.CorePapers[0].entity_name == "Point Cloud Semantic Segmentation"
    assert topics_not_by_year.CorePapers[0].publication_id == 85092710521

    assert specific_metrics.CorePapers is None

    assert non_existing.CorePapers is None

def test_field_weighted_citation_impact():
    """Test FieldWeightedCitationImpact property"""
    expected_fields = ("entity_id", "entity_name", "metric", "year", "value", "percentage", "threshold")

    assert len(topic.FieldWeightedCitationImpact) == 1
    assert topic.FieldWeightedCitationImpact[0]._fields == expected_fields

    assert len(topics_by_year.FieldWeightedCitationImpact) == 15
    assert topics_by_year.FieldWeightedCitationImpact[0]._fields == expected_fields

    assert len(topics_not_by_year.FieldWeightedCitationImpact) == 2
    assert topics_not_by_year.FieldWeightedCitationImpact[0]._fields == expected_fields
    assert topics_not_by_year.FieldWeightedCitationImpact[0].entity_id == 3909
    assert topics_not_by_year.FieldWeightedCitationImpact[0].entity_name == "Point Cloud Semantic Segmentation"
    assert topics_not_by_year.FieldWeightedCitationImpact[0].metric == "FieldWeightedCitationImpact"
    assert topics_not_by_year.FieldWeightedCitationImpact[0].year == "all"
    assert topics_not_by_year.FieldWeightedCitationImpact[0].value == approx(1.7, rel=0.1)
    assert topics_not_by_year.FieldWeightedCitationImpact[0].percentage is None
    assert topics_not_by_year.FieldWeightedCitationImpact[0].threshold is None

    assert specific_metrics.FieldWeightedCitationImpact is None

    assert non_existing.FieldWeightedCitationImpact is None

def test_institution_count():
    """Test InstitutionCount property"""
    expected_fields = ("entity_id", "entity_name", "metric", "year", "value", "percentage", "threshold")

    assert len(topic.InstitutionCount) == 1
    assert topic.InstitutionCount[0]._fields == expected_fields

    assert len(topics_by_year.InstitutionCount) == 18
    assert topics_by_year.InstitutionCount[0]._fields == expected_fields

    assert len(topics_not_by_year.InstitutionCount) == 2
    assert topics_not_by_year.InstitutionCount[0]._fields == expected_fields
    assert topics_not_by_year.InstitutionCount[0].entity_id == 3909
    assert topics_not_by_year.InstitutionCount[0].entity_name == "Point Cloud Semantic Segmentation"
    assert topics_not_by_year.InstitutionCount[0].metric == "InstitutionCount"
    assert topics_not_by_year.InstitutionCount[0].year == "all"
    assert topics_not_by_year.InstitutionCount[0].value == approx(1551, rel=0.1)
    assert topics_not_by_year.InstitutionCount[0].percentage is None
    assert topics_not_by_year.InstitutionCount[0].threshold is None

    assert specific_metrics.InstitutionCount is None

    assert non_existing.InstitutionCount is None


def test_most_recently_published_papers():
    """Test MostRecentlyPublishedPapers property"""
    expected_fields = ('entity_id', 'entity_name', 'publication_id')

    assert len(topic.MostRecentlyPublishedPapers) == approx(822, rel=0.1)
    assert topic.MostRecentlyPublishedPapers[0]._fields == expected_fields

    assert topics_by_year.MostRecentlyPublishedPapers is None

    assert len(topics_not_by_year.MostRecentlyPublishedPapers) == approx(5862, rel=0.1)
    assert topics_not_by_year.MostRecentlyPublishedPapers[0]._fields == expected_fields
    assert topics_not_by_year.MostRecentlyPublishedPapers[0].entity_id == 3909
    assert topics_not_by_year.MostRecentlyPublishedPapers[0].entity_name == "Point Cloud Semantic Segmentation"
    assert topics_not_by_year.MostRecentlyPublishedPapers[0].publication_id == 105011703758

    assert specific_metrics.MostRecentlyPublishedPapers is None

    assert non_existing.MostRecentlyPublishedPapers is None


def test_related_topics():
    """Test RelatedTopics property"""
    expected_fields = ('entity_id', 'entity_name', 'related_topic_id', 'related_topic_name', 'related_topic_uri', 'prominencePercentile', 'relationScore', 'relatedTopicRank')

    assert len(topic.RelatedTopics) == 50
    assert topic.RelatedTopics[0]._fields == expected_fields

    assert topics_by_year.RelatedTopics is None

    assert len(topics_not_by_year.RelatedTopics) == 100
    assert topics_not_by_year.RelatedTopics[0]._fields == expected_fields
    assert topics_not_by_year.RelatedTopics[0].entity_id == 3909
    assert topics_not_by_year.RelatedTopics[0].entity_name == "Point Cloud Semantic Segmentation"
    assert topics_not_by_year.RelatedTopics[0].related_topic_id == 10013
    assert topics_not_by_year.RelatedTopics[0].related_topic_name == "Sensor Fusion and Object Detection in Autonomous Driving"
    assert topics_not_by_year.RelatedTopics[0].related_topic_uri == "Topic/10013"
    assert topics_not_by_year.RelatedTopics[0].prominencePercentile == 0
    assert topics_not_by_year.RelatedTopics[0].relationScore == 0
    assert topics_not_by_year.RelatedTopics[0].relatedTopicRank == 0

    assert specific_metrics.RelatedTopics is None

    assert non_existing.RelatedTopics is None


def test_scholarly_output():
    """Test ScholarlyOutput property"""
    expected_fields = ("entity_id", "entity_name", "metric", "year", "value", "percentage", "threshold")

    assert len(topic.ScholarlyOutput) == 1
    assert topic.ScholarlyOutput[0]._fields == expected_fields

    assert len(topics_by_year.ScholarlyOutput) == 15
    assert topics_by_year.ScholarlyOutput[0]._fields == expected_fields

    assert len(topics_not_by_year.ScholarlyOutput) == 2
    assert topics_not_by_year.ScholarlyOutput[0]._fields == expected_fields
    assert topics_not_by_year.ScholarlyOutput[0].entity_id == 3909
    assert topics_not_by_year.ScholarlyOutput[0].entity_name == "Point Cloud Semantic Segmentation"
    assert topics_not_by_year.ScholarlyOutput[0].metric == "ScholarlyOutput"
    assert topics_not_by_year.ScholarlyOutput[0].year == "all"
    assert topics_not_by_year.ScholarlyOutput[0].value == approx(5275, rel=0.1)
    assert topics_not_by_year.ScholarlyOutput[0].percentage is None
    assert topics_not_by_year.ScholarlyOutput[0].threshold is None

    assert specific_metrics.ScholarlyOutput is None

    assert non_existing.ScholarlyOutput is None


def test_top_authors():
    """Test TopAuthors property"""
    expected_fields = ('entity_id', 'entity_name', 'author_id', 'author_name', 'publicationCount')

    assert len(topic.TopAuthors) == 100
    assert topic.TopAuthors[0]._fields == expected_fields
    assert topic.TopAuthors[0].entity_id == 9549
    assert topic.TopAuthors[0].entity_name == "Quantum States and Entanglement in Many-Body Systems"
    assert topic.TopAuthors[0].author_id == 24773004400
    assert topic.TopAuthors[0].author_name == "Cirac, J. Ignacio"
    assert topic.TopAuthors[0].publicationCount == approx(23, rel=0.1)

    assert topics_by_year.TopAuthors is None

    assert len(topics_not_by_year.TopAuthors) == 200
    assert topics_not_by_year.TopAuthors[0]._fields == expected_fields

    assert non_existing.TopAuthors is None


def test_top_cited_publications():
    """Test TopCitedPublications property"""
    expected_fields = ('entity_id', 'entity_name', 'publication_id', 'citationCount')

    assert len(topic.TopCitedPublications) == 100
    assert topic.TopCitedPublications[0]._fields == expected_fields
    assert topic.TopCitedPublications[0].entity_id == 9549
    assert topic.TopCitedPublications[0].entity_name == "Quantum States and Entanglement in Many-Body Systems"
    assert topic.TopCitedPublications[0].publication_id == 85122122728
    assert topic.TopCitedPublications[0].citationCount == approx(455, rel=0.1)

    assert len(topics_by_year.TopCitedPublications) == 300
    assert topics_by_year.TopCitedPublications[0]._fields == expected_fields

    assert len(topics_not_by_year.TopCitedPublications) == 200
    assert topics_not_by_year.TopCitedPublications[0]._fields == expected_fields

    assert non_existing.TopCitedPublications is None


def test_top_institutions():
    """Test TopInstitutions property"""
    expected_fields = ('entity_id', 'entity_name', 'institution_id', 'institution_name', 'publicationCount')

    assert len(topic.TopInstitutions) == 100
    assert topic.TopInstitutions[0]._fields == expected_fields
    assert topic.TopInstitutions[0].entity_id == 9549
    assert topic.TopInstitutions[0].entity_name == "Quantum States and Entanglement in Many-Body Systems"
    assert topic.TopInstitutions[0].institution_id == 309054
    assert topic.TopInstitutions[0].institution_name == "Technical University of Munich"
    assert topic.TopInstitutions[0].publicationCount == approx(90, rel=0.1)

    assert topics_by_year.TopInstitutions is None

    assert len(topics_not_by_year.TopInstitutions) == 200
    assert topics_not_by_year.TopInstitutions[0]._fields == expected_fields

    assert non_existing.TopInstitutions is None


def test_top_journals():
    """Test TopJournals property"""
    expected_fields = ('entity_id', 'entity_name', 'journal_id', 'journal_name', 'publicationCount', 'citationCount', 'authorCount', 'publicationGrowth', 'authorGrowth', 'sjr', 'snip', 'citeScore')

    assert len(topic.TopJournals) == 100
    assert topic.TopJournals[0]._fields == expected_fields
    assert topic.TopJournals[0].entity_id == 9549
    assert topic.TopJournals[0].entity_name == "Quantum States and Entanglement in Many-Body Systems"
    assert topic.TopJournals[0].journal_id == 21100874236
    assert topic.TopJournals[0].journal_name == "Physical Review B"
    assert topic.TopJournals[0].publicationCount == approx(180, rel=0.1)
    assert topic.TopJournals[0].citationCount == approx(1597, rel=0.1)
    assert topic.TopJournals[0].authorCount == approx(396, rel=0.1)
    assert topic.TopJournals[0].publicationGrowth == approx(-37.77778, rel=0.1)
    assert topic.TopJournals[0].authorGrowth == approx(-36.49635, rel=0.1)

    assert topics_by_year.TopJournals is None

    assert len(topics_not_by_year.TopJournals) == 100
    assert topics_not_by_year.TopJournals[0]._fields == expected_fields

    assert non_existing.TopJournals is None


def test_top_keywords():
    """Test TopKeywords property"""
    expected_fields = ('entity_id', 'entity_name', 'keyword_name', 'keyword_uri', 'weight', 'relevance', 'publicationCount', 'publicationGrowth')

    assert len(topic.TopKeywords) == 100
    assert topic.TopKeywords[0]._fields == expected_fields
    assert topic.TopKeywords[0].entity_id == 9549
    assert topic.TopKeywords[0].entity_name == "Quantum States and Entanglement in Many-Body Systems"
    assert topic.TopKeywords[0].keyword_name == "Quantum Entanglement"
    assert topic.TopKeywords[0].keyword_uri == "Keyword/10253440894"
    assert topic.TopKeywords[0].weight == approx(145, rel=0.1)
    assert topic.TopKeywords[0].relevance == approx(1, rel=0.1)
    assert topic.TopKeywords[0].publicationCount == approx(165, rel=0.1)
    assert topic.TopKeywords[0].publicationGrowth == approx(257.14285, rel=0.3)

    assert len(topics_not_by_year.TopKeywords) == 200
    assert topics_not_by_year.TopKeywords[0]._fields == expected_fields

    assert topics_by_year.TopKeywords is None

    assert non_existing.TopKeywords is None
