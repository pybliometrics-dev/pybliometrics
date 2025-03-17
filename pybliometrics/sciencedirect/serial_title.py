"""Module with the class ScDirSerialTitle."""
from typing import Optional, Union

from pybliometrics.scopus import SerialTitle


class ScDirSerialTitle(SerialTitle):
    def __init__(self,
                 issn: Union[int, str],
                 refresh: Union[bool, int] = False,
                 view: str = "ENHANCED",
                 years: Optional[str] = None,
                 **kwds: str
                 ) -> None:
        """Interaction with the ScienceDirect Serial Title API.

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
        SerialTitle.__init__(self, issn, refresh, view, years, **kwds)
