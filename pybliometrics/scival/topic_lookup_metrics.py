from collections import namedtuple
from typing import Union, Optional

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import make_int_if_possible
from pybliometrics.utils.constants import SCIVAL_METRICS
from pybliometrics.utils.parse_metrics import extract_metric_data, extract_metric_lists, MetricData

class TopicLookupMetrics(Retrieval):
    @property
    def topics(self) -> list:
        """A list of namedtuples representing topics and their basic info
        in the form `(id, name, uri, prominencePercentile, scholarlyOutput)`.
        """
        out = []
        Topic = namedtuple('Topic',
                           'id name uri prominencePercentile scholarlyOutput')

        results = self._json.get('results', [])

        for result in results:
            topic_data = result.get('topic', {})
            new = Topic(
                id=make_int_if_possible(topic_data.get('id')),
                name=topic_data.get('name'),
                uri=topic_data.get('uri'),
                prominencePercentile=topic_data.get('prominencePercentile'),
                scholarlyOutput=topic_data.get('scholarlyOutput')
            )
            out.append(new)
        return out

    @property
    def AuthorCount(self) -> Optional[list[MetricData]]:
        """Author count metrics for each topic.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'AuthorCount', self._by_year, "topic")

    @property
    def CitationCount(self) -> Optional[list[MetricData]]:
        """Citation count metrics for each topic.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CitationCount', self._by_year, "topic")

    @property
    def CorePapers(self) -> Optional[list]:
        """Core papers for the topic.
        Returns list of CorePaper namedtuples with structure: (entity_id, entity_name, publication_id)
        """
        CorePaper = namedtuple('CorePaper',
                               'entity_id entity_name publication_id')

        out = []
        for item in extract_metric_lists(self._json, "CorePapers", "topic"):
            entity_id = item.get('entity_id')
            entity_name = item.get('entity_name')

            for paper in item.get('values', []):
                out.append(CorePaper(
                    entity_id=entity_id,
                    entity_name=entity_name,
                    publication_id=paper.get('id')
                ))
        return out or None

    @property
    def FieldWeightedCitationImpact(self) -> Optional[list[MetricData]]:
        """Field weighted citation impact metrics for each topic.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'FieldWeightedCitationImpact', self._by_year, "topic")

    @property
    def InstitutionCount(self) -> Optional[list[MetricData]]:
        """Institution count metrics for each topic.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'InstitutionCount', self._by_year, "topic")

    @property
    def MostRecentlyPublishedPapers(self) -> Optional[list]:
        """Most recently published papers for the topic.
        Returns list of RecentPaper namedtuples with structure: (entity_id, entity_name, publication_id)
        """
        RecentPaper = namedtuple('RecentPaper',
                                 'entity_id entity_name publication_id')

        out = []
        for item in extract_metric_lists(self._json, "MostRecentlyPublishedPapers", "topic"):
            entity_id = item.get('entity_id')
            entity_name = item.get('entity_name')

            for paper in item.get('values', []):
                out.append(RecentPaper(
                    entity_id=entity_id,
                    entity_name=entity_name,
                    publication_id=paper.get('id')
                ))
        return out or None

    @property
    def RelatedTopics(self) -> Optional[list]:
        """Related topics for the topic.
        Returns list of RelatedTopic namedtuples with structure:
        (entity_id, entity_name, related_topic_id, related_topic_name, related_topic_uri, prominencePercentile, relationScore, relatedTopicRank)
        """
        RelatedTopic = namedtuple('RelatedTopic',
                                  'entity_id entity_name related_topic_id related_topic_name related_topic_uri prominencePercentile relationScore relatedTopicRank')

        out = []
        for item in extract_metric_lists(self._json, "RelatedTopics", "topic"):
            entity_id = item.get('entity_id')
            entity_name = item.get('entity_name')

            for topic in item.get('values', []):
                topic_data = topic.get('topic', {})
                out.append(RelatedTopic(
                    entity_id=entity_id,
                    entity_name=entity_name,
                    related_topic_id=topic_data.get('id'),
                    related_topic_name=topic_data.get('name'),
                    related_topic_uri=topic_data.get('uri'),
                    prominencePercentile=topic.get('prominencePercentile'),
                    relationScore=topic.get('relationScore'),
                    relatedTopicRank=topic.get('relatedtopicrank')
                ))
        return out or None

    @property
    def ScholarlyOutput(self) -> Optional[list[MetricData]]:
        """Scholarly output metrics for each topic.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'ScholarlyOutput', self._by_year, "topic")

    @property
    def TopAuthors(self) -> Optional[list]:
        """Top authors for the topic.
        Returns list of TopAuthor namedtuples with structure:
        (entity_id, entity_name, author_id, author_name, publicationCount)
        """
        TopAuthor = namedtuple('TopAuthor',
                               'entity_id entity_name author_id author_name publicationCount')

        out = []
        for item in extract_metric_lists(self._json, "TopAuthors", "topic"):
            entity_id = item.get('entity_id')
            entity_name = item.get('entity_name')

            for author in item.get('values', []):
                out.append(TopAuthor(
                    entity_id=entity_id,
                    entity_name=entity_name,
                    author_id=author.get('id'),
                    author_name=author.get('name'),
                    publicationCount=author.get('publicationCount')
                ))
        return out or None

    @property
    def TopCitedPublications(self) -> Optional[list]:
        """Top cited publications for the topic.
        Returns list of TopPublication namedtuples with structure:
        (entity_id, entity_name, publication_id, citationCount)
        """
        TopPublication = namedtuple('TopPublication',
                                    'entity_id entity_name publication_id citationCount')

        out = []
        for item in extract_metric_lists(self._json, "TopCitedPublications", "topic"):
            entity_id = item.get('entity_id')
            entity_name = item.get('entity_name')

            for pub in item.get('values', []):
                out.append(TopPublication(
                    entity_id=entity_id,
                    entity_name=entity_name,
                    publication_id=pub.get('id'),
                    citationCount=pub.get('citationCount')
                ))
        return out or None

    @property
    def TopInstitutions(self) -> Optional[list]:
        """Top institutions for the topic.
        Returns list of TopInstitution namedtuples with structure:
        (entity_id, entity_name, institution_id, institution_name, publicationCount)
        """
        TopInstitution = namedtuple('TopInstitution',
                                    'entity_id entity_name institution_id institution_name publicationCount')

        out = []
        for item in extract_metric_lists(self._json, "TopInstitutions", "topic"):
            entity_id = item.get('entity_id')
            entity_name = item.get('entity_name')

            for institution in item.get('values', []):
                out.append(TopInstitution(
                    entity_id=entity_id,
                    entity_name=entity_name,
                    institution_id=institution.get('id'),
                    institution_name=institution.get('name'),
                    publicationCount=institution.get('publicationCount')
                ))
        return out or None

    @property
    def TopJournals(self) -> Optional[list]:
        """Top journals for the topic.
        Returns list of TopJournal namedtuples with structure:
        (entity_id, entity_name, journal_id, journal_name, publicationCount, 
        citationCount, authorCount, publicationGrowth, authorGrowth, sjr, snip, citeScore)
        """
        TopJournal = namedtuple('TopJournal',
                                'entity_id entity_name journal_id journal_name publicationCount citationCount authorCount publicationGrowth authorGrowth sjr snip citeScore')

        out = []
        for item in extract_metric_lists(self._json, "TopJournals", "topic"):
            entity_id = item.get('entity_id')
            entity_name = item.get('entity_name')

            for journal in item.get('values', []):
                out.append(TopJournal(
                    entity_id=entity_id,
                    entity_name=entity_name,
                    journal_id=journal.get('id'),
                    journal_name=journal.get('name'),
                    publicationCount=journal.get('publicationCount'),
                    citationCount=journal.get('citationCount'),
                    authorCount=journal.get('authorCount'),
                    publicationGrowth=journal.get('publicationGrowth'),
                    authorGrowth=journal.get('authorGrowth'),
                    sjr=journal.get('sjr'),
                    snip=journal.get('snip'),
                    citeScore=journal.get('citeScore')
                ))
        return out or None

    @property
    def TopKeywords(self) -> Optional[list]:
        """Top keywords for the topic.
        Returns list of TopKeyword namedtuples with structure:
        (entity_id, entity_name, keyword_name, keyword_uri, weight, 
        relevance, publicationCount, publicationGrowth)
        """
        TopKeyword = namedtuple('TopKeyword',
                                'entity_id entity_name keyword_name keyword_uri weight relevance publicationCount publicationGrowth')
        out = []
        for item in extract_metric_lists(self._json, "TopKeywords", "topic"):
            entity_id = item.get('entity_id')
            entity_name = item.get('entity_name')

            for keyword in item.get('values', []):
                out.append(TopKeyword(
                    entity_id=entity_id,
                    entity_name=entity_name,
                    keyword_name=keyword.get('name'),
                    keyword_uri=keyword.get('uri'),
                    weight=keyword.get('weight'),
                    relevance=keyword.get('relevance'),
                    publicationCount=keyword.get('publicationCount'),
                    publicationGrowth=keyword.get('publicationGrowth')
                ))
        return out or None

    def __init__(self,
                 topic_ids: Union[str, list],
                 metric_types: Optional[Union[str, list]] = None,
                 by_year: bool = False,
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ) -> None:
        """Interaction with the SciVal's `metrics` endpoint of the `TopicLookup API`.

        :param topic_ids: SciVal Topic ID(s). Can be a single ID or comma-separated 
                          string of IDs, or a list of IDs (e.g. `[1516, 1517]`).
        :param metric_types: Metric type(s) to retrieve. Can be a single metric 
                             or comma-separated string, or a list. Available metrics are:
                             AuthorCount, CitationCount, CorePapers, FieldWeightedCitationImpact,
                             InstitutionCount, MostRecentlyPublishedPapers, RelatedTopics,
                             ScholarlyOutput, TopAuthors, TopCitedPublications, TopInstitutions,
                             TopJournals, TopKeywords.
                             If not provided, all metrics are retrieved.
        :param by_year: Whether to retrieve metrics broken down by year.
                        Note: Some metrics are not available by year: CorePapers, 
                        MostRecentlyPublishedPapers, RelatedTopics, TopAuthors, 
                        TopInstitutions, TopJournals, TopKeywords.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the 
                     https://dev.elsevier.com/documentation/SciValTopicAPI.wadl.
        """
        self._view = ''
        self._refresh = refresh
        self._by_year = by_year

        # Handle topic_ids parameter
        if isinstance(topic_ids, list):
            topic_ids = ",".join(str(t) for t in topic_ids)
        else:
            topic_ids = topic_ids.replace(" ", "")

        # Depend on by_year, set default metric_types if not provided
        if metric_types is None:
            if not by_year:
                metric_types = SCIVAL_METRICS["TopicLookupMetrics"]["byYear"] + SCIVAL_METRICS["TopicLookupMetrics"]["notByYear"]
            else:
                metric_types = SCIVAL_METRICS["TopicLookupMetrics"]["byYear"]

        if isinstance(metric_types, list):
            metric_types = ",".join(metric_types)

        # Set up parameters for the API call
        params = {
            'topicIds': topic_ids,
            'metricTypes': metric_types,
            'byYear': str(by_year).lower(),
            **kwds
        }

        Retrieval.__init__(self, **params)

    def __str__(self):
        """Return pretty text version of the topic metrics."""
        topics = self.topics or []
        topic_count = len(topics)

        if topic_count == 0:
            return "No topics found"
        else:
            s = f"TopicLookupMetrics for {topic_count} topic(s):"
            for topic in topics:
                s += f"\n- {topic.name} (ID: {topic.id})"
            return s
