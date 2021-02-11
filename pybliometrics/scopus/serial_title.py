from collections import namedtuple

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import check_parameter_value, get_link


class SerialTitle(Retrieval):
    @property
    def aggregation_type(self):
        """The type of the source."""
        return self._entry['prism:aggregationType']

    @property
    def citescoreyearinfolist(self):
        """A list of two tuples of the form (year, cite-score).  The first
        tuple represents the current cite-score, the second tuple
        represents the tracker cite-score."""
        try:
            d = self._entry['citeScoreYearInfoList']
        except KeyError:
            return None
        current = (d['citeScoreCurrentMetricYear'], d['citeScoreCurrentMetric'])
        tracker = (d['citeScoreTrackerYear'], d['citeScoreTracker'])
        return [current, tracker]

    @property
    def eissn(self):
        """The electronic ISSN of the source."""
        return self._entry.get('prism:eIssn')

    @property
    def issn(self):
        """The ISSN of the source."""
        return self._entry.get('prism:issn')

    @property
    def oaallowsauthorpaid(self):
        """Whether under the Open-Access policy authors are allowed to pay."""
        return self._entry.get('oaAllowsAuthorPaid')

    @property
    def openaccess(self):
        """Open Access status (0 or 1)."""
        return self._entry.get('openaccess')

    @property
    def openaccessstartdate(self):
        """Starting availability date."""
        return self._entry.get('openaccessStartDate')

    @property
    def openaccesstype(self):
        """Open Archive status (full or partial)."""
        return self._entry.get('openaccessType')

    @property
    def openaccessarticle(self):
        """Open Access status (boolean)."""
        return self._entry.get('openaccessArticle')

    @property
    def openarchivearticle(self):
        """Open Archive status (boolean)."""
        return self._entry.get('openArchiveArticle')

    @property
    def openaccesssponsorname(self):
        """The name of the Open Access sponsor."""
        return self._entry.get('openaccessSponsorName')

    @property
    def openaccesssponsortype(self):
        """The type of the Open Access sponsor."""
        return self._entry.get('openaccessSponsorType')

    @property
    def openaccessuserlicense(self):
        """The User license."""
        return self._entry.get('openaccessUserLicense')

    @property
    def publisher(self):
        """The publisher of the source."""
        return self._entry['dc:publisher']

    @property
    def scopus_source_link(self):
        """URL to info site on scopus.com."""
        return get_link(self._entry, 0, ["link"])

    @property
    def self_link(self):
        """URL to the source's API page."""
        return get_link(self._json, 0, ["link"])

    @property
    def sjrlist(self):
        """The SCImago Journal Rank (SJR) indicator as list of
        (year, indicator)-tuples.  See
        https://www.scimagojr.com/journalrank.php.
        """
        return _parse_list(self._entry, "SJR")

    @property
    def sniplist(self):
        """The Source-Normalized Impact per Paper (SNIP) as list of
        (year, indicator)-tuples.  See
        https://blog.scopus.com/posts/journal-metrics-in-scopus-source-normalized-impact-per-paper-snip.
        """
        return _parse_list(self._entry, "SNIP")

    @property
    def source_id(self):
        """The Scopus ID of the source."""
        return self._entry['source-id']

    @property
    def subject_area(self):
        """List of named tuples of subject areas in the form
        (area, abbreviation, code) of the source.
        """
        area = namedtuple('Subjectarea', 'area abbreviation code')
        areas = [area(area=item['$'], code=item['@code'],
                      abbreviation=item['@abbrev'])
                 for item in self._entry["subject-area"]]
        return areas or None

    @property
    def title(self):
        """The title of the source."""
        return self._entry['dc:title']

    def __init__(self, issn, refresh=False, view="ENHANCED", years=None):
        """Interaction with the Serial Title API.

        Parameters
        ----------
        issn : str or int
            The ISSN or the E-ISSN of the source.

        refresh : bool or int (optional, default=False)
            Whether to refresh the cached file if it exists or not.  If int
            is passed, cached file will be refreshed if the number of days
            since last modification exceeds that value.

        view : str (optional, default="ENHANCED")
            The view of the file that should be downloaded.  Allowed values:
            BASIC, STANDARD, ENHANCED.  For details see
            https://dev.elsevier.com/sc_serial_title_views.html.

        years : str (optional, default=None)
            A string specifying a year or range of years (combining two
            years with a hyphen) for which yearly metric data (SJR, SNIP,
            yearly-data) should be looked up for.  If None, only the
            most recent metric data values are provided.
            Note: If not None, refresh will always be True.

        Examples
        --------
        See https://pybliometrics.readthedocs.io/en/stable/examples/SerialTitle.html.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{source_id}`,
        where `path` is specified in `~/.scopus/config.ini`.
        """
        # Checks
        check_parameter_value(view, ('BASIC', 'STANDARD', 'ENHANCED'), "view")
        # Load json
        self._id = str(issn)
        self._years = years
        # Force refresh when years is specified
        if years:
            refresh = True
        Retrieval.__init__(self, identifier=self._id, view=view, date=years,
                           api='SerialTitle', refresh=refresh)
        self._json = self._json['serial-metadata-response']
        self._entry = self._json['entry'][0]

    def __str__(self):
        """Print a summary string."""
        date = self.get_cache_file_mdate().split()[0]
        areas = [e.area for e in self.subject_area]
        if len(areas) == 1:
            areas = areas[0]
        else:
            areas = " and ".join([", ".join(areas[:-1]), areas[-1]])
        s = f"'{self.title}', {self.aggregation_type} published by "\
            f"'{self.publisher}', is active in {areas}\n"
        metrics = []
        if self.sjrlist:
            metrics.append(f"SJR:  year value")
            for rec in self.sjrlist:
                metrics.append(f"      {rec[0]} {rec[1]}")
        if self.sniplist:
            metrics.append(f"SNIP: year value")
            for rec in self.sniplist:
                metrics.append(f"      {rec[0]} {rec[1]}")
        if metrics:
            s += f"Metrics as of {date}:\n    " + "\n    ".join(metrics) + "\n"
        s += f"    ISSN: {self.issn or '-'}, E-ISSN: {self.eissn or '-'}, "\
             f"Scopus ID: {self.source_id}"
        return s


def _parse_list(d, metric):
    """Auxiliary function to parse SNIP and SJR lists."""
    try:
        values = [(r['@year'], r['$']) for r in d[metric + "List"][metric]]
        return sorted(set(values))
    except (KeyError, TypeError):
        return None
