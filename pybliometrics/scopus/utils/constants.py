from os import environ
from pathlib import Path

# Paths for cached files
if (Path.home()/".scopus").exists():
    BASE_PATH = Path.home()/".scopus"
elif (Path.home()/".pybliometrics"/"Scopus").exists():
    BASE_PATH = Path.home()/".pybliometrics"/"Scopus"
else:
    BASE_PATH = Path.home()/".cache"/"pybliometrics"/"Scopus"
DEFAULT_PATHS = {
    'AbstractRetrieval': BASE_PATH/'abstract_retrieval',
    'AffiliationRetrieval': BASE_PATH/'affiliation_retrieval',
    'AffiliationSearch': BASE_PATH/'affiliation_search',
    'AuthorRetrieval': BASE_PATH/'author_retrieval',
    'AuthorSearch': BASE_PATH/'author_search',
    'CitationOverview': BASE_PATH/'citation_overview',
    'ScopusSearch': BASE_PATH/'scopus_search',
    'SerialSearch': BASE_PATH/'serial_search',
    'SerialTitle': BASE_PATH/'serial_title',
    'PlumXMetrics': BASE_PATH/'plumx',
    'SubjectClassifications': BASE_PATH/'subject_classification'
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
    'PlumXMetrics': 'https://api.elsevier.com/analytics/plumx/'
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
    'SubjectClassifications': 0
}

# Other API restrictions
SEARCH_MAX_ENTRIES = 5_000
