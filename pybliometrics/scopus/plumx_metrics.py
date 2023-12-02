from collections import namedtuple
from typing import List, NamedTuple, Optional, Union

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import check_parameter_value


class PlumXMetrics(Retrieval):
    @property
    def category_totals(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing total metrics as categorized
        by PlumX Metrics in the form `(capture, citation, mention, socialMedia,
        usage)`.

        Note: For Citation category a maximum citation count across sources
        is shown.  For details on PlumX Metrics categories see
        https://plumanalytics.com/learn/about-metrics/.
        """
        categories = self._json.get('count_categories', [])
        return _format_as_namedtuple_list(categories, "Category") or None

    @property
    def capture(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing metrics in the Captures category.

        Note: For details on Capture metrics see
        https://plumanalytics.com/learn/about-metrics/capture-metrics/.
        """
        metrics = self._count_categories.get('capture', [])
        return _format_as_namedtuple_list(metrics) or None

    @property
    def citation(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing citation counts from
        different sources.

        Note: For details on Citation metrics see
        https://plumanalytics.com/learn/about-metrics/citation-metrics/.
        """
        metrics = []
        for item in self._count_categories.get('citation', []):
            if item.get('sources'):
                metrics += item['sources']
        return _format_as_namedtuple_list(metrics) or None

    @property
    def mention(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing metrics in Mentions category.

        Note: For details on Mention metrics see
        https://plumanalytics.com/learn/about-metrics/mention-metrics/.
        """
        metrics = self._count_categories.get('mention', [])
        return _format_as_namedtuple_list(metrics) or None

    @property
    def social_media(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing social media metrics.

        Note: For details on Social Media metrics see
        https://plumanalytics.com/learn/about-metrics/social-media-metrics/.
        """
        metrics = self._count_categories.get('socialMedia', [])
        return _format_as_namedtuple_list(metrics) or None

    @property
    def usage(self) -> Optional[List[NamedTuple]]:
        """A list of namedtuples representing Usage category metrics.

        Note: For details on Usage metrics see
        https://plumanalytics.com/learn/about-metrics/usage-metrics/.
        """
        metrics = self._count_categories.get('usage', [])
        return _format_as_namedtuple_list(metrics) or None

    def __init__(self,
                 identifier: str,
                 id_type: str,
                 refresh: Union[bool, int] = False,
                 **kwds: str
                 ) -> None:
        """Interaction with the PlumX Metrics API.

        :param identifier: The identifier of a document.
        :param id_type: The type of used ID. Allowed values are:
                        'airitiDocId'; 'cabiAbstractId'; 'citeulikeId';
                        'digitalMeasuresArtifactId'; 'doi'; 'elsevierId';
                        'elsevierPii'; 'facebookCountUrlId';
                        'figshareArticleId'; 'isbn'; 'lccn'; 'medwaveId';
                        'nctId'; 'oclc'; 'pittEprintDscholarId'; 'pmcid';
                        'pmid'; 'redditId'; 'repecHandle'; 'repoUrl';
                        'scieloId'; 'sdEid'; 'slideshareUrlId';
                        'smithsonianPddrId'; 'ssrnId'; 'urlId'
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If `int` is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/PlumXMetricsAPI.wadl.

        Raises
        ------
        ValueError
            If the parameter `refresh` is not one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/ENHANCED/{identifier}`,
        where `path` is specified in your configuration file.
        """
        # Checks
        allowed = ('airitiDocId', 'cabiAbstractId', 'citeulikeId',
                   'digitalMeasuresArtifactId', 'doi', 'elsevierId',
                   'elsevierPii', 'facebookCountUrlId', 'figshareArticleId',
                   'isbn', 'lccn', 'medwaveId', 'nctId', 'oclc',
                   'pittEprintDscholarId', 'pmcid', 'pmid', 'redditId',
                   'repecHandle', 'repoUrl', 'scieloId', 'sdEid',
                   'slideshareUrlId', 'smithsonianPddrId', 'ssrnId', 'urlId')
        check_parameter_value(id_type, allowed, "id_type")
        self._id_type = id_type
        self._identifier = identifier

        # Load json
        self._refresh = refresh
        self._view = 'ENHANCED'
        Retrieval.__init__(self, identifier=identifier, id_type=id_type,
                           api='PlumXMetrics', **kwds)
        cats = self._json.get('count_categories', [])
        self._count_categories = {d["name"]: d['count_types'] for d in cats}

    def __str__(self):
        """Print a summary string."""
        s = f"Document with {self._id_type} {self._identifier} received:\n- "
        cats = [f"{c.total:,} citation(s) in category '{c.name}'"
                for c in self.category_totals]
        s += "\n- ".join(cats)
        s += f"\nas of {self.get_cache_file_mdate().split()[0]}"
        return s


def _format_as_namedtuple_list(metric_counts, tuple_name='Metric'):
    """Formats list of dicts of metrics into list of namedtuples in the
    form `(name, total)`.
    """
    metric = namedtuple(tuple_name, 'name total')
    return [metric(name=t['name'], total=t['total']) for t in metric_counts]
