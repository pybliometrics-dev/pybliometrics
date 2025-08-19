from collections import namedtuple
from typing import Union, Optional

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import make_int_if_possible
from pybliometrics.utils.constants import SCIVAL_METRICS
from pybliometrics.utils.parse_metrics import extract_metric_data


class AuthorMetrics(Retrieval):
    @property  
    def AcademicCorporateCollaboration(self) -> Optional[list]:
        """Academic corporate collaboration metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'AcademicCorporateCollaboration', self._by_year, "author")

    @property
    def AcademicCorporateCollaborationImpact(self) -> Optional[list]:
        """Academic corporate collaboration impact metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'AcademicCorporateCollaborationImpact', self._by_year, "author")

    @property
    def all_metrics(self) -> Optional[list]:
        """Get all available metrics concatenated into a single list.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        all_metrics = []

        # List of all metric properties
        if self._metric_types:
            metric_properties = self._metric_types.split(",")
            
            for prop_name in metric_properties:
                metrics = getattr(self, prop_name)
                if metrics:
                    all_metrics.extend(metrics)

        return all_metrics or None

    @property
    def authors(self) -> Optional[list]:
        """A list of namedtuples representing authors and their basic info
        in the form `(id, name, uri)`.
        """
        out = []
        Author = namedtuple('Author', 'id name uri')

        # Handle both dict and direct access to results
        if isinstance(self._json, dict):
            results = self._json.get('results', [])
        else:
            results = []

        for result in results:
            author_data = result.get('author', {})
            new = Author(
                id=make_int_if_possible(author_data.get('id')),
                name=author_data.get('name'),
                uri=author_data.get('uri')
            )
            out.append(new)
        return out or None

    @property
    def CitationCount(self) -> Optional[list]:
        """Citation count metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CitationCount', self._by_year, "author")

    @property
    def CitationsPerPublication(self) -> Optional[list]:
        """Citations per publication metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CitationsPerPublication', self._by_year, "author")

    @property
    def CitedPublications(self) -> Optional[list]:
        """Cited publications metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CitedPublications', self._by_year, "author")

    @property
    def Collaboration(self) -> Optional[list]:
        """Collaboration metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'Collaboration', self._by_year, "author")

    @property
    def CollaborationImpact(self) -> Optional[list]:
        """Collaboration impact metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CollaborationImpact', self._by_year, "author")

    @property
    def FieldWeightedCitationImpact(self) -> Optional[list]:
        """Field weighted citation impact metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'FieldWeightedCitationImpact', self._by_year, "author")

    @property
    def HIndices(self) -> Optional[list]:
        """H-indices metrics for each author (only available when by_year=False).
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'HIndices', self._by_year, "author")

    @property
    def OutputsInTopCitationPercentiles(self) -> Optional[list]:
        """Outputs in top citation percentiles metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'OutputsInTopCitationPercentiles', self._by_year, "author")

    @property
    def PublicationsInTopJournalPercentiles(self) -> Optional[list]:
        """Publications in top journal percentiles metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'PublicationsInTopJournalPercentiles', self._by_year, "author")

    @property
    def ScholarlyOutput(self) -> Optional[list]:
        """Scholarly output metrics for each author.
        Returns list of MetricData namedtuples with unified structure:
        (entity_id, entity_name, metric, metric_type, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'ScholarlyOutput', self._by_year, "author")

    def __init__(self,
                 author_ids: Union[str, list],
                 metric_types: Optional[Union[str, list]] = None,
                 by_year: bool = False,
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ) -> None:
        """Interaction with the SciVal Author Metrics API.

        :param author_ids: Scopus Author ID(s). Can be a single ID or comma-separated 
                           string of IDs, or a list of IDs (e.g. `[55586732900, 57215631099]`).
        :param metric_types: Metric type(s) to retrieve. Can be a single metric 
                             or comma-separated string, or a list. Available metrics are:
                             AcademicCorporateCollaboration, AcademicCorporateCollaborationImpact,
                             CitationCount, CitedPublications, Collaboration, CollaborationImpact,
                             FieldWeightedCitationImpact, ScholarlyOutput,
                             PublicationsInTopJournalPercentiles, OutputsInTopCitationPercentiles,
                             HIndices.
                             If not provided, all metrics are retrieved.
        :param by_year: Whether to retrieve metrics broken down by year.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/SciValAuthorAPI.wadl.
            
        Note:
            All metric properties return lists of MetricData namedtuples with 
            unified structure: `(entity_id, entity_name, metric, metric_type, 
            year, value, percentage, threshold)`. Use the `all_metrics` property
            to get all metrics concatenated into a single list for easy data
            manipulation and analysis.
        """
        self._view = ''
        self._refresh = refresh
        self._by_year = by_year

        # Handle authors parameter
        if isinstance(author_ids, list):
            author_ids = ",".join(str(a) for a in author_ids)

        # Handle metric_types parameter - use all metrics by default
        if metric_types is None:
            if not by_year:
                metric_types = SCIVAL_METRICS["AuthorMetrics"]["byYear"] + SCIVAL_METRICS["AuthorMetrics"]["notByYear"]
            if by_year:
                metric_types = SCIVAL_METRICS["AuthorMetrics"]["byYear"]

        if isinstance(metric_types, list):
            metric_types = ",".join(metric_types)

        self._metric_types = metric_types

        # Set up parameters for the API call
        params = {
            'authors': author_ids,
            'metricTypes': metric_types,
            'byYear': str(by_year).lower(),
            **kwds
        }

        Retrieval.__init__(self, **params, **kwds)

    def __str__(self):
        """Return pretty text version of the author metrics."""
        authors = self.authors or []
        author_count = len(authors)

        if author_count == 0:
            return "No authors found"
        else:
            s = f"AuthorMetrics for {author_count} author(s):"
            for author in authors:
                s += f"\n- {author.name} (ID: {author.id})"
            return s
