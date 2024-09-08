from os import environ
from pathlib import Path

# Paths for cached files
if (Path.home()/".scopus").exists():
    BASE_PATH_SCOPUS = Path.home()/".scopus"
    BASE_PATH_SCIENCEDIRECT = Path.home()/".sciencedirect"
elif (Path.home()/".pybliometrics"/"Scopus").exists():
    BASE_PATH_SCOPUS = Path.home()/".pybliometrics"/"Scopus"
    BASE_PATH_SCIENCEDIRECT = Path.home()/".pybliometrics"/"ScienceDirect"
else:
    BASE_PATH_SCOPUS = Path.home()/".cache"/"pybliometrics"/"Scopus"
    BASE_PATH_SCIENCEDIRECT = Path.home()/".cache"/"pybliometrics"/"ScienceDirect"

DEFAULT_PATHS = {
    'AbstractRetrieval': BASE_PATH_SCOPUS/'abstract_retrieval',
    'AffiliationRetrieval': BASE_PATH_SCOPUS/'affiliation_retrieval',
    'AffiliationSearch': BASE_PATH_SCOPUS/'affiliation_search',
    'AuthorRetrieval': BASE_PATH_SCOPUS/'author_retrieval',
    'AuthorSearch': BASE_PATH_SCOPUS/'author_search',
    'CitationOverview': BASE_PATH_SCOPUS/'citation_overview',
    'ScopusSearch': BASE_PATH_SCOPUS/'scopus_search',
    'SerialSearch': BASE_PATH_SCOPUS/'serial_search',
    'SerialTitle': BASE_PATH_SCOPUS/'serial_title',
    'PlumXMetrics': BASE_PATH_SCOPUS/'plumx',
    'SubjectClassifications': BASE_PATH_SCOPUS/'subject_classification',
    'ArticleMetadata': BASE_PATH_SCIENCEDIRECT/'article_metadata/',
    'ArticleRetrieval': BASE_PATH_SCIENCEDIRECT/'article_retrieval',
    'ScienceDirectSearch': BASE_PATH_SCIENCEDIRECT/'science_direct_search'
}

# Configuration file location
if 'PYB_CONFIG_FILE' in environ:
    CONFIG_FILE = Path(environ['PYB_CONFIG_FILE'])
else:
    if (Path.home()/".scopus").exists():
        CONFIG_FILE = Path.home()/".scopus"/"config.ini"
    elif (Path.home()/".pybliometrics"/"config.ini").exists():
        CONFIG_FILE = Path.home()/".pybliometrics"/"config.ini"
    else:
        CONFIG_FILE = Path.home()/".config"/"pybliometrics.cfg"

# URLs for all classes
RETRIEVAL_BASE = 'https://api.elsevier.com/content/'
SEARCH_BASE = 'https://api.elsevier.com/content/search/'
URLS = {
    'AbstractRetrieval': RETRIEVAL_BASE + 'abstract/',
    'AffiliationRetrieval': RETRIEVAL_BASE + 'affiliation/affiliation_id/',
    'AffiliationSearch': SEARCH_BASE + 'affiliation',
    'AuthorRetrieval': RETRIEVAL_BASE + 'author/author_id/',
    'AuthorSearch': SEARCH_BASE + 'author',
    'CitationOverview': RETRIEVAL_BASE + 'abstract/citations/',
    'ScopusSearch': SEARCH_BASE + 'scopus',
    'SerialSearch': RETRIEVAL_BASE + 'serial/title',
    'SerialTitle': RETRIEVAL_BASE + 'serial/title/issn/',
    'SubjectClassifications': RETRIEVAL_BASE + 'subject/scopus',
    'PlumXMetrics': 'https://api.elsevier.com/analytics/plumx/',
    'ArticleMetadata': RETRIEVAL_BASE + 'metadata/article/',
    'ArticleRetrieval': RETRIEVAL_BASE + 'article/',
    'ScienceDirectSearch': SEARCH_BASE + 'sciencedirect/'
}

# Valid views for all classes
VIEWS = {
    "CitationOverview": ["STANDARD"],
    "AbstractRetrieval": ["META", "META_ABS", "FULL", "REF", "ENTITLED"],
    "AffiliationRetrieval": ["LIGHT", "STANDARD", "ENTITLED"],
    "AffiliationSearch": ["STANDARD"],
    "AuthorRetrieval": ["LIGHT", "STANDARD", "ENHANCED", "METRICS", "ENTITLED"],
    "AuthorSearch": ["STANDARD"],
    "PlumXMetrics": ["ENHANCED"],
    "ScopusSearch": ["STANDARD", "COMPLETE"],
    "SerialSearch": ["STANDARD", "ENHANCED", "CITESCORE"],
    "SerialTitle": ["STANDARD", "ENHANCED", "CITESCORE"],
    "SubjectClassifications": [''],
    "ArticleRetrieval": ["META", "META_ABS", "META_ABS_REF", "FULL", "ENTITLED"],
    "ArticleMetadata": ["STANDARD", "COMPLETE"],
    "ScienceDirectSearch": ["STANDARD"]
}

# Throttling limits (in queries per second) // 0 = no limit
RATELIMITS = {
    'AbstractRetrieval': 9,
    'AffiliationRetrieval': 9,
    'AffiliationSearch': 6,
    'AuthorRetrieval': 3,
    'AuthorSearch': 2,
    'CitationOverview': 4,
    'ScopusSearch': 9,
    'SerialSearch': 6,
    'SerialTitle': 6,
    'PlumXMetrics': 6,
    'SubjectClassifications': 0,
    'ArticleMetadata': 6,
    'ArticleRetrieval': 10,
    'ScienceDirectSearch': 2
}

# Other API restrictions
SEARCH_MAX_ENTRIES = 5_000

