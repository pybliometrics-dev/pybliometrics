"""Base exceptions and classes for pybliometrics.scopus."""

import warnings

warnings.filterwarnings("default", category=DeprecationWarning)


def deprecated(cls):
    original_init = cls.__init__
    def __init__(self, *args, **kwargs):
        msg = f"{cls.__name__} is deprecated and will be removed in the next "\
              "release. Please use ScopusServerError instead"
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
        original_init(self, *args, **kwargs)
    cls.__init__ = __init__
    return cls


# Base classes
class ScopusException(Exception):
    """Base class for exceptions in pybliometrics."""


class ScopusError(ScopusException):
    """Exception for a serious error in pybliometrics."""


# Query errors
class ScopusQueryError(ScopusException):
    """Exception for problems related to Scopus queries."""


# HTML errors
class ScopusHtmlError(ScopusException):
    """Wrapper for exceptions raised by requests."""


class Scopus400Error(ScopusHtmlError):
    """Raised if a query yields a 400 error (Bad Request for url)."""


class Scopus401Error(ScopusHtmlError):
    """Raised if a query yields a 401 error (Unauthorized for url)."""


class Scopus403Error(ScopusHtmlError):
    """Raised if a query yields a 403 error (Forbidden for url)."""


class Scopus404Error(ScopusHtmlError):
    """Raised if a query yields a 404 error (Not Found for url)."""


class Scopus407Error(ScopusHtmlError):
    """Raised if a query yields a 407 error (Proxy Authentication Required)."""


class Scopus413Error(ScopusHtmlError):
    """Raised if a query yields a 413 error (Request Entity Too
    Large for url).
    """


class Scopus414Error(ScopusHtmlError):
    """Raised if a query yields a 414 error (Request-URI Too Large for url)."""


class Scopus429Error(ScopusHtmlError):
    """Raised if a query yields a 429 error (Quota exceeded)."""


class ScopusServerError(ScopusHtmlError):
    """Wrapper for Server related exceptions (code 5xx)."""


@deprecated
class Scopus500Error(ScopusServerError):
    """Raised if a query yields a 500 error (Internal Server Error
    for url).
    """

@deprecated
class Scopus502Error(ScopusServerError):
    """Raised if a query yields a 502 error (Bad gateway for url)."""

@deprecated
class Scopus504Error(ScopusServerError):
    """Raised if a query yields a 504 error (Gateway Time-out for url)."""
