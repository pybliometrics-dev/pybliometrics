from collections import namedtuple

from pybliometrics.scopus.superclasses import Retrieval


class PlumXMetrics(Retrieval):
    @property
    def category_totals(self):
        """A list of namedtuples representing total metrics as categorized
        by PlumX Metrics in the form (capture, citation, mention, socialMedia,
        usage).
        Note: Can be empty. Specific categories can be absent depending on
        existence of data and applicability of metrics to document type. For
        Citation category a maximum citation count across sources is shown.
        For details on PlumX Metrics categories see
        https://plumanalytics.com/learn/about-metrics/
        """
        out = []
        fields = 'name total'
        cat = namedtuple('Category', fields)
        for item in self._json.get('count_categories', []):
            if item.get('name') and item.get('total'):
                new = cat(name=item.get('name'),
                          total=item.get('total'))
                out.append(new)
        return out or None
    
    @property
    def capture(self):
        """A list of namedtuples representing metrics in Captures category:
        metrics that track when end users bookmark, favorite, become a reader,
        become a watcher, etc, i.e. metrics that indicate that someone wants
        to come back to the work.
        Note: Can be empty. Specific metrics can be absent depending on
        existence of data and applicability of metrics to document type.
        For details on Capture metrics see
        https://plumanalytics.com/learn/about-metrics/capture-metrics/
        """
        categories = self._json.get('count_categories', [])
        mention_metrics = _category_metrics('capture', categories)
        return _list_metrics_totals(mention_metrics) or None
    
    @property
    def citation(self):
        """A list of namedtuples representing citation counts from 
        different sources.
        Note: Can be empty.
        For details and list of possible sources see
        https://plumanalytics.com/learn/about-metrics/citation-metrics/
        """
        categories = self._json.get('count_categories', [])
        citation_metrics = _category_metrics('citation', categories)
        source_metrics = []
        if citation_metrics:
            for item in citation_metrics:
                if item.get('sources'):
                    source_metrics += item.get('sources')
        return _list_metrics_totals(source_metrics) or None
    
    @property
    def mention(self):
        """A list of namedtuples representing metrics in Mentions category:
        metrics that measure engagement with research.
        Note: Can be empty. Specific metrics can be absent depending on
        existence of data and applicability of metrics to document type.
        For details on Mention metrics see
        https://plumanalytics.com/learn/about-metrics/mention-metrics/
        """
        categories = self._json.get('count_categories', [])
        mention_metrics = _category_metrics('mention', categories)
        return _list_metrics_totals(mention_metrics) or None
    
    @property
    def social_media(self):
        """A list of namedtuples representing social media metrics:
        metrics on promotion of research.
        Note: Can be empty. Specific metrics can be absent depending on
        existence of data and applicability of metrics to document type.
        For details on social media metrics see
        https://plumanalytics.com/learn/about-metrics/social-media-metrics/
        """
        categories = self._json.get('count_categories', [])
        social_metrics = _category_metrics('socialMedia', categories)
        return _list_metrics_totals(social_metrics) or None
    
    @property
    def usage(self):
        """A list of namedtuples representing Usage category metrics:
        metrics that capture interaction with and usage of research.
        Note: Can be empty. Specific metrics can be absent depending on
        existence of data and applicability of metrics to document type.
        For details on Usage metrics see
        https://plumanalytics.com/learn/about-metrics/usage-metrics/
        """
        categories = self._json.get('count_categories', [])
        usage_metrics = _category_metrics('usage', categories)
        return _list_metrics_totals(usage_metrics) or None
    
    def __init__(self, identifier, id_type, refresh=False):
        """Interaction with the PlumX Metrics API.

        Parameters
        ----------
        identifier : str
            The identifier of a document.

        id_type: str
            The type of used ID. Allowed values are:
                - 'airitiDocId'
                - 'arxivId'
                - 'cabiAbstractId'
                - 'citeulikeId'
                - 'digitalMeasuresArtifactId'
                - 'doi'
                - 'elsevierId'
                - 'elsevierPii'
                - 'facebookCountUrlId'
                - 'figshareArticleId'
                - 'githubRepoId'
                - 'isbn'
                - 'lccn'
                - 'medwaveId'
                - 'nctId'
                - 'oclc'
                - 'pittEprintDscholarId'
                - 'pmcid'
                - 'pmid'
                - 'redditId'
                - 'repecHandle'
                - 'repoUrl'
                - 'scieloId'
                - 'sdEid'
                - 'slideshareUrlId'
                - 'smithsonianPddrId'
                - 'soundcloudTrackId'
                - 'ssrnId'
                - 'urlId'
                - 'usPatentApplicationId'
                - 'usPatentPublicationId'
                - 'vimeoVideoId'
                - 'youtubeVideoId'

        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/PlumXMetrics.html.

        Notes
        -----
        The directory for cached results is `{path}/ENHANCED/{identifier}`,
        where `path` is specified in `~/.scopus/config.ini`.
        """
        allowed_ids = ('airitiDocId', 'arxivId', 'cabiAbstractId',
                       'citeulikeId', 'digitalMeasuresArtifactId', 'doi',
                       'elsevierId', 'elsevierPii', 'facebookCountUrlId',
                       'figshareArticleId', 'githubRepoId', 'isbn',
                       'lccn', 'medwaveId', 'nctId',
                       'oclc', 'pittEprintDscholarId', 'pmcid',
                       'pmid', 'redditId', 'repecHandle',
                       'repoUrl', 'scieloId', 'sdEid',
                       'slideshareUrlId', 'smithsonianPddrId', 'soundcloudTrackId',
                       'ssrnId', 'urlId', 'usPatentApplicationId',
                       'usPatentPublicationId', 'vimeoVideoId', 'youtubeVideoId')
        if id_type not in allowed_ids:
            raise ValueError('Id type must be one of: ' +
                             ', '.join(allowed_ids))
        self.id_type = id_type
        self.identifier = identifier
        Retrieval.__init__(self, identifier=identifier, id_type=id_type,
                           api='PlumXMetrics', refresh=refresh, view='ENHANCED')

    def __str__(self):
        """Print a summary string."""
        cats = [f"{c.total:,} citations in category '{c.name}'"
                for c in self.category_totals]
        date = self.get_cache_file_mdate().split()[0]
        cats[0] += f" as of {date}"
        s = f"Document with {self.id_type} {self.identifier} has "
        s += ", ".join(cats)
        return s


def _category_metrics(category_name, categories_list):
    """Auxiliary function returning all available metrics in a single
    category as a list of dicts
    """
    cat_counts = []
    for item in categories_list:
        if item.get('name') == category_name:
            cat_counts += item.get('count_types', [])
    return cat_counts


def _list_metrics_totals(metric_counts):
    """Formats list of dicts of metrics into list of namedtuples in form
    (name, total)
    """
    out = []
    # Metric names and associated counts if either is not None
    values = [[m.get('name'), m.get('total')] for m in metric_counts
              if m.get('name') and m.get('total')]
    fields = 'name total'
    capture = namedtuple('Metric', fields)
    for v in values:
        new = capture(name=v[0], total=v[1])
        out.append(new)
    return out

