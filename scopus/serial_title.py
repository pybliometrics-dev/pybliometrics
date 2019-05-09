from collections import namedtuple
from json import loads

from scopus.classes import Retrieval

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
        return self._entry.get('link', [{}])[0].get('@href')

    @property
    def self_link(self):
        """URL to the source's API page."""
        return self._json.get('link', [{}])[0].get('@href')

    @property
    def sjrlist(self):
        """The most recent SCImago Journal Rank (SJR) indicator as
        (year, indicator)-tuple.  See
        https://www.scimagojr.com/journalrank.php.
        """
        return (self._entry['SJRList']['SJR'][0]['@year'],
                self._entry['SJRList']['SJR'][0]['$'])

    @property
    def sniplist(self):
        """Source-Normalized Impact per Paper (SNIP) of the source.  See
        https://blog.scopus.com/posts/journal-metrics-in-scopus-source-normalized-impact-per-paper-snip."""
        return (self._entry['SNIPList']['SNIP'][0]['@year'],
                self._entry['SNIPList']['SNIP'][0]['$'])
    
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

    def __init__(self, issn, refresh=False, view="ENHANCED"):
        """Class to represent a Serial Title retrieval.

        Parameters
        ----------
        issn : str or int
            The ISSN or the E-ISSN of the source.

        refresh : bool (optional, default=False)
            Whether to refresh the cached file (if it exists) or not.

        view : str (optional, default="ENHANCED")
            The view of the file that should be downloaded.  Will not take
            effect for already cached files.  Allowed values: BASIC, STANDARD,
            ENHANCED.  See
            https://dev.elsevier.com/guides/SerialTitleViews.htm
            for details.

        Notes
        -----
        The files are cached in ~/.scopus/serial_title/{source_id}.
        """
        # Checks
        allowed_views = ('BASIC', 'STANDARD', 'ENHANCED')
        if view not in allowed_views:
            raise ValueError('view parameter must be one of ' +
                             ', '.join(allowed_views))
        # Load json
        self._id = str(issn)
        Retrieval.__init__(self, identifier=self._id, api='SerialTitle',
                           refresh=refresh)
        self._json = self._json['serial-metadata-response']
        self._entry = self._json['entry'][0]

    def __str__(self):
        """Print a summary string."""
        areas = [e.area for e in self.subject_area]
        if len(areas) == 1:
            areas = areas[0]
        else:
            areas = " and ".join([", ".join(areas[:-1]), areas[-1]])
        s = '''{self.title}, {self.aggregation_type} published by {self.publisher}
active in {areas}.
SJR ({self.sjrlist[0]}): ({self.sjrlist[1]}),
SNIP ({self.sniplist[0]}): ({self.sniplist[1]})
ISSN: {self.issn}, E-ISSN: {self.eissn}, Scopus ID: {self.source_id}'''.format(
            self=self, areas=areas)
        return s
