"""Base exceptions and classes for scopus."""


# Base classes
class ScopusException(Exception):
    """Base class for exceptions in scopus."""


class ScopusError(ScopusException):
    """Exception for a serious error in scopus."""


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


class Scopus404Error(ScopusHtmlError):
    """Raised if a query yields a 404 error (Not Found for url)."""


class Scopus429Error(ScopusHtmlError):
    """Raised if a query yields a 429 error (Quota exceeded)."""


class Scopus500Error(ScopusHtmlError):
    """Raised if a query yields a 500 error (Internal Server Error
    for url).
    """
