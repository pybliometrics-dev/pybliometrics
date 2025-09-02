from collections import namedtuple
from typing import Union, Optional

from pybliometrics.superclasses import Retrieval
from pybliometrics.utils import make_int_if_possible
from pybliometrics.utils.constants import SCIVAL_METRICS
from pybliometrics.utils.parse_metrics import extract_metric_data, MetricData


class InstitutionLookupMetrics(Retrieval):
    @property  
    def AcademicCorporateCollaboration(self) -> Optional[list[MetricData]]:
        """Academic corporate collaboration metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'AcademicCorporateCollaboration', self._by_year, "institution")

    @property
    def AcademicCorporateCollaborationImpact(self) -> Optional[list[MetricData]]:
        """Academic corporate collaboration impact metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'AcademicCorporateCollaborationImpact', self._by_year, "institution")

    @property
    def institutions(self) -> Optional[list[MetricData]]:
        """A list of namedtuples representing institutions and their basic info
        in the form `(id, name, uri)`.
        """
        out = []
        Institution = namedtuple('Institution', 'id name uri')

        # Handle both dict and direct access to results
        if isinstance(self._json, dict):
            results = self._json.get('results', [])
        else:
            results = []

        for result in results:
            institution_data = result.get('institution', {})
            new = Institution(
                id=make_int_if_possible(institution_data.get('id')),
                name=institution_data.get('name'),
                uri=institution_data.get('uri')
            )
            out.append(new)
        return out or None

    @property
    def CitationCount(self) -> Optional[list[MetricData]]:
        """Citation count metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CitationCount', self._by_year, "institution")

    @property
    def CitationsPerPublication(self) -> Optional[list[MetricData]]:
        """Citations per publication metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CitationsPerPublication', self._by_year, "institution")

    @property
    def CitedPublications(self) -> Optional[list[MetricData]]:
        """Cited publications metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CitedPublications', self._by_year, "institution")

    @property
    def Collaboration(self) -> Optional[list[MetricData]]:
        """Collaboration metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'Collaboration', self._by_year, "institution")

    @property
    def CollaborationImpact(self) -> Optional[list[MetricData]]:
        """Collaboration impact metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'CollaborationImpact', self._by_year, "institution")

    @property
    def FieldWeightedCitationImpact(self) -> Optional[list[MetricData]]:
        """Field weighted citation impact metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'FieldWeightedCitationImpact', self._by_year, "institution")

    @property
    def OutputsInTopCitationPercentiles(self) -> Optional[list[MetricData]]:
        """Outputs in top citation percentiles metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'OutputsInTopCitationPercentiles', self._by_year, "institution")

    @property
    def PublicationsInTopJournalPercentiles(self) -> Optional[list[MetricData]]:
        """Publications in top journal percentiles metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'PublicationsInTopJournalPercentiles', self._by_year, "institution")

    @property
    def ScholarlyOutput(self) -> Optional[list[MetricData]]:
        """Scholarly output metrics for each institution.
        Returns list of MetricData namedtuples with structure:
        (entity_id, entity_name, metric, year, value, percentage, threshold)
        """
        return extract_metric_data(self._json, 'ScholarlyOutput', self._by_year, "institution")

    def __init__(self,
                 institution_ids: Union[str, list],
                 metric_types: Optional[Union[str, list]] = None,
                 by_year: bool = False,
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ) -> None:
        """Interaction with the SciVal's `metrics` endpoint of the `InstitutionLookup API`.

        :param institution_ids: SciVal Institution ID(s). Can be a single ID or comma-separated 
                               string of IDs, or a list of IDs (e.g. `[309054, 309086]`).
        :param metric_types: Metric type(s) to retrieve. Can be a single metric 
                             or comma-separated string, or a list. Available metrics are:
                             AcademicCorporateCollaboration, AcademicCorporateCollaborationImpact,
                             CitationCount, CitedPublications, Collaboration, CollaborationImpact,
                             FieldWeightedCitationImpact, ScholarlyOutput,
                             PublicationsInTopJournalPercentiles, OutputsInTopCitationPercentiles.
                             If not provided, all metrics are retrieved.
        :param by_year: Whether to retrieve metrics broken down by year.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/SciValInstitutionAPI.wadl.
            
        Note:
            All metric properties return lists of MetricData namedtuples with 
            structure: `(entity_id, entity_name, metric, 
            year, value, percentage, threshold)`.

        """
        self._view = ''
        self._refresh = refresh
        self._by_year = by_year

        # Handle institutions parameter
        if isinstance(institution_ids, list):
            institution_ids = ",".join(str(i) for i in institution_ids)

        # Handle metric_types parameter - use all metrics by default
        if metric_types is None:
            metric_types = SCIVAL_METRICS["InstitutionLookupMetrics"]["byYear"]

        if isinstance(metric_types, list):
            metric_types = ",".join(metric_types)

        self._metric_types = metric_types

        # Set up parameters for the API call
        params = {
            'institutionIds': institution_ids,
            'metricTypes': metric_types,
            'byYear': str(by_year).lower(),
            **kwds
        }

        Retrieval.__init__(self, **params, **kwds)

    def __str__(self):
        """Return pretty text version of the institution metrics."""
        institutions = self.institutions or []
        institution_count = len(institutions)

        if institution_count == 0:
            return "No institutions found"
        else:
            s = f"InstitutionLookupMetrics for {institution_count} institution(s):"
            for institution in institutions:
                s += f"\n- {institution.name} (ID: {institution.id})"
            return s
