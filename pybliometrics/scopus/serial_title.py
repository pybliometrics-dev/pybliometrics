from collections import namedtuple
from typing import List, NamedTuple, Optional, Tuple, Union

from pybliometrics.scopus.superclasses import Retrieval
from pybliometrics.scopus.utils import chained_get, check_parameter_value,\
    get_link, make_float_if_possible, make_int_if_possible, VIEWS


class SerialTitle(Retrieval):
    @property
    def aggregation_type(self) -> str:
        """The type of the source."""
        return self._entry['prism:aggregationType']

    @property
    def citescoreyearinfolist(self) -> Optional[List[NamedTuple]]:
        """A list of named tuples of the form: `(year citescoare)` or (when
        `view="CITESCORE"`) `(year citescore status documentcount citationcount
        percentcited rank)`.  `rank` is `None` or a named tuple of the form
        `(subjectcode rank percentile)`.

        For more information see the
        [CiteScore documentation](https://service.elsevier.com/app/answers/detail/a_id/14880/supporthub/scopus/).
        """
        
        try:
            data = self._entry.get('citeScoreYearInfoList', {})
        except KeyError:
            return None

        # Named Tuples
        info_fields = 'year citescore status documentcount citationcount '\
                      'percentcited rank'
        rank_fields = 'subjectcode rank percentile'
        info_short = namedtuple('Citescoreinfolist', info_fields.split()[:2])
        info_full = namedtuple('Citescoreinfolist', info_fields,
            defaults=(None,) * len(info_fields.split()))
        rank = namedtuple('Citescoresubjectrank', rank_fields)

        # Function to create a named tuple for CurrentMetric and CurrentTracker
        def _create_namedtuple(data, mode, info):
            year = data.get(f'citeScore{mode}Year')
            cite_score = data.get(f'citeScore{mode}')

            # To be consistent with old verion
            if (year is None) and (cite_score is None):
                return None

            return info(year=int(year), citescore=float(cite_score))

        # Extract depending on view
        if self._view in ('STANDARD', 'ENHANCED'):
            current = _create_namedtuple(data, 'CurrentMetric', info_short)
            tracker = _create_namedtuple(data, 'Tracker', info_short)
            new_data = [current, tracker]

        elif self._view == 'CITESCORE':
            new_data = _get_all_cite_score_years(self, info_full, rank, data)

        return new_data or None

    @property
    def eissn(self) -> Optional[str]:
        """The electronic ISSN of the source."""
        return self._entry.get('prism:eIssn')

    @property
    def issn(self) -> Optional[str]:
        """The ISSN of the source."""
        return self._entry.get('prism:issn')

    @property
    def oaallowsauthorpaid(self) -> Optional[str]:
        """Whether under the Open-Access policy authors are allowed to pay."""
        return self._entry.get('oaAllowsAuthorPaid')

    @property
    def openaccess(self) -> Optional[int]:
        """Open Access status (0 or 1)."""
        return make_int_if_possible(chained_get(self._entry, ['openaccess']))

    @property
    def openaccessstartdate(self):
        """Starting availability date."""
        return self._entry.get('openaccessStartDate')

    @property
    def openaccesstype(self) -> Optional[str]:
        """Open Archive status (full or partial)."""
        return self._entry.get('openaccessType')

    @property
    def openaccessarticle(self) -> Optional[bool]:
        """Open Access status."""
        return self._entry.get('openaccessArticle')

    @property
    def openarchivearticle(self) -> Optional[bool]:
        """Open Archive status."""
        return self._entry.get('openArchiveArticle')

    @property
    def openaccesssponsorname(self) -> Optional[str]:
        """The name of the Open Access sponsor."""
        return self._entry.get('openaccessSponsorName')

    @property
    def openaccesssponsortype(self) -> Optional[str]:
        """The type of the Open Access sponsor."""
        return self._entry.get('openaccessSponsorType')

    @property
    def openaccessuserlicense(self) -> Optional[str]:
        """The User license."""
        return self._entry.get('openaccessUserLicense')

    @property
    def publisher(self) -> str:
        """The publisher of the source."""
        return self._entry['dc:publisher']

    @property
    def scopus_source_link(self) -> str:
        """URL to info site on scopus.com."""
        return get_link(self._entry, 0, ["link"])

    @property
    def self_link(self) -> str:
        """URL to the source's API page."""
        return get_link(self._json, 0, ["link"])

    @property
    def sjrlist(self) -> Optional[List[Tuple[int, float]]]:
        """The SCImago Journal Rank (SJR) indicator as list of tuples in the form
        `(year, indicator)`.  See
        https://www.scimagojr.com/journalrank.php.
        """
        return _parse_list(self._entry, "SJR")

    @property
    def sniplist(self) -> Optional[List[Tuple[int, float]]]:
        """The Source-Normalized Impact per Paper (SNIP) as list of tuples in the form
        `(year, indicator)`.  See
        https://blog.scopus.com/posts/journal-metrics-in-scopus-source-normalized-impact-per-paper-snip.
        """
        return _parse_list(self._entry, "SNIP")

    @property
    def source_id(self) -> int:
        """The Scopus ID of the source."""
        return int(self._entry['source-id'])

    @property
    def subject_area(self) -> Optional[List[NamedTuple]]:
        """List of named tuples of subject areas in the form
        `(area, abbreviation, code)` of the source.
        """
        area = namedtuple('Subjectarea', 'area abbreviation code')
        areas = [area(area=item['$'], code=int(item['@code']),
                      abbreviation=item['@abbrev'])
                 for item in self._entry["subject-area"]]
        return areas or None

    @property
    def title(self) -> str:
        """The title of the source."""
        return self._entry['dc:title']

    @property
    def yearly_data(self) -> Optional[List[NamedTuple]]:
        """Yearly citation information as a list of namedtuples in the
        form `(year, publicationcount, revpercent, zerocitessce,
        zerocitespercentsce, citecountsce)`.  That's the number of documents
        published in this year, the share of review articles thereof, the
        number and share of not-cited documents, and the number of distinct
        documents that were cited in this year.
        """
        try:
            data = self._entry['yearly-data']["info"]
        except KeyError:
            return None
        fields = 'year publicationcount revpercent zerocitessce '\
                 'zerocitespercentsce citecountsce'
        dat = namedtuple('Yearlydata', fields)
        data = [dat(year=int(d['@year']), citecountsce=int(d['citeCountSCE']),
                    publicationcount=int(d['publicationCount']),
                    revpercent=make_float_if_possible(d['revPercent']),
                    zerocitessce=int(d['zeroCitesSCE']),
                    zerocitespercentsce=make_float_if_possible(d['zeroCitesPercentSCE']))
                for d in data]
        return data or None

    def __init__(self,
                 issn: Union[int, str],
                 refresh: Union[bool, int] = False,
                 view: str = "ENHANCED",
                 years: str = None,
                 **kwds: str
                 ) -> None:
        """Interaction with the Serial Title API.

        :param issn: The ISSN or the E-ISSN of the source.
        :param refresh: Whether to refresh the cached file if it exists or not.
                        If int is passed, cached file will be refreshed if the
                        number of days since last modification exceeds that value.
        :param view: The view of the file that should be downloaded.  Allowed
                     values: `STANDARD`, `ENHANCED`, `CITESCORE`.  For details
                     see https://dev.elsevier.com/sc_serial_title_views.html.
        :param years: A string specifying a year or range of years (combining
                      two years with a hyphen) for which yearly metric data
                      (SJR, SNIP, yearly-data) should be looked up for.  If
                      `None`, only the most recent metric data values are
                      provided. Note: If not `None`, refresh will always be `True`.
        :param kwds: Keywords passed on as query parameters.  Must contain
                     fields and values mentioned in the API specification at
                     https://dev.elsevier.com/documentation/SerialTitleAPI.wadl.

        Raises
        ------
        ValueError
            If any of the parameters `refresh` or `view` is not
            one of the allowed values.

        Notes
        -----
        The directory for cached results is `{path}/{view}/{source_id}`,
        where `path` is specified in your configuration file.
        """
        # Checks
        check_parameter_value(view, VIEWS['SerialTitle'], "view")
        self._view = view

        # Force refresh when years is specified
        if years:
            refresh = True
        self._refresh = refresh

        # Load json
        self._id = str(issn)
        self._years = years
        Retrieval.__init__(self, identifier=self._id, date=years,
                           api='SerialTitle', **kwds)

        # Parse json
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
        values = [(int(r['@year']), float(r['$'])) for r
                  in d[metric + "List"][metric]]
        return sorted(set(values))
    except (KeyError, TypeError):
        return None


def _get_all_cite_score_years(self, named_info_list, named_rank_list, data) -> Optional[List[NamedTuple]]:
    """Auxiliary function to get all information contained in cite score 
    information list for the `CITESCORE` view."""
    data = data.get('citeScoreYearInfo', [])

    new_data = []
    # Iterate through years
    for d in data:
        citeScoreInfo = d.get('citeScoreInformationList', [])[
            0].get('citeScoreInfo', [])[0]
        # Iterate through subject ranks
        subject_rank = [named_rank_list(subjectcode=int(subject['subjectCode']),
                        rank=int(subject['rank']),
                        percentile=int(subject['percentile']))
                        for subject in citeScoreInfo['citeScoreSubjectRank']]
        # Create named tuple with info
        Citescoreinfolist_year = named_info_list(year=int(d['@year']),
            status=d['@status'],
            documentcount=int(citeScoreInfo['scholarlyOutput']),
            citationcount=int(citeScoreInfo['citationCount']),
            citescore=make_float_if_possible(citeScoreInfo['citeScore']),
            percentcited=int(citeScoreInfo['percentCited']),
            rank=subject_rank)
        # Append new data
        new_data.append(Citescoreinfolist_year)

    return new_data or None
