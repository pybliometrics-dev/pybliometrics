from pathlib import Path

# Location of configuration file with legacy support
config_options = [
    Path.home() / ".scopus" / "config.ini",
    Path.home() / ".pybliometrics" / "Scopus" / "config.ini",
    Path.home() / ".config" / "pybliometrics.cfg"  # default
]
CONFIG_FILE = next((path for path in config_options if path.exists()),
                   config_options[-1])

# Location of cache with legacy support
base_path_options = [
    Path.home() / ".scopus",
    Path.home() / ".pybliometrics" / "Scopus",
    Path.home() / ".cache" / "pybliometrics" / "Scopus"  # default
]
BASE_PATH_SCOPUS = next((path for path in base_path_options if path.exists()),
                        base_path_options[-1])
BASE_PATH_SCIENCEDIRECT = BASE_PATH_SCOPUS.parent / "ScienceDirect"

DEFAULT_PATHS = {
    'AbstractRetrieval': BASE_PATH_SCOPUS / 'abstract_retrieval',
    'AffiliationRetrieval': BASE_PATH_SCOPUS / 'affiliation_retrieval',
    'AffiliationSearch': BASE_PATH_SCOPUS / 'affiliation_search',
    'AuthorRetrieval': BASE_PATH_SCOPUS / 'author_retrieval',
    'AuthorSearch': BASE_PATH_SCOPUS / 'author_search',
    'ArticleEntitlement': BASE_PATH_SCIENCEDIRECT / 'article_entitlement',
    'ArticleMetadata': BASE_PATH_SCIENCEDIRECT / 'article_metadata',
    'ArticleRetrieval': BASE_PATH_SCIENCEDIRECT / 'article_retrieval',
    'CitationOverview': BASE_PATH_SCOPUS / 'citation_overview',
    'ObjectMetadata': BASE_PATH_SCIENCEDIRECT / 'object_metadata',
    'ObjectRetrieval': BASE_PATH_SCIENCEDIRECT / 'object_retrieval',
    'PlumXMetrics': BASE_PATH_SCOPUS / 'plumx',
    'ScDirSubjectClassifications': BASE_PATH_SCIENCEDIRECT / 'subject_classification',
    'ScienceDirectSearch': BASE_PATH_SCIENCEDIRECT / 'science_direct_search',
    'ScopusSearch': BASE_PATH_SCOPUS / 'scopus_search',
    'SerialSearch': BASE_PATH_SCOPUS / 'serial_search',
    'SerialTitle': BASE_PATH_SCOPUS / 'serial_title',
    'SubjectClassifications': BASE_PATH_SCOPUS / 'subject_classification',
}

# URLs for all classes
RETRIEVAL_BASE = 'https://api.elsevier.com/content/'
SEARCH_BASE = 'https://api.elsevier.com/content/search/'
URLS = {
    'AbstractRetrieval': RETRIEVAL_BASE + 'abstract/',
    'ArticleEntitlement': RETRIEVAL_BASE + 'article/entitlement/',
    'ArticleMetadata': RETRIEVAL_BASE + 'metadata/article/',
    'ArticleRetrieval': RETRIEVAL_BASE + 'article/',
    'AffiliationRetrieval': RETRIEVAL_BASE + 'affiliation/affiliation_id/',
    'AffiliationSearch': SEARCH_BASE + 'affiliation',
    'AuthorRetrieval': RETRIEVAL_BASE + 'author/author_id/',
    'AuthorSearch': SEARCH_BASE + 'author',
    'CitationOverview': RETRIEVAL_BASE + 'abstract/citations/',
    'ObjectMetadata': RETRIEVAL_BASE + 'object/',
    'ObjectRetrieval': RETRIEVAL_BASE + 'object/',
    'PlumXMetrics': 'https://api.elsevier.com/analytics/plumx/',
    'ScDirSubjectClassifications': RETRIEVAL_BASE + 'subject/scidir/',
    'ScienceDirectSearch': SEARCH_BASE + 'sciencedirect/',
    'ScopusSearch': SEARCH_BASE + 'scopus',
    'SerialSearch': RETRIEVAL_BASE + 'serial/title',
    'SerialTitle': RETRIEVAL_BASE + 'serial/title/issn/',
    'SubjectClassifications': RETRIEVAL_BASE + 'subject/scopus',
}

# Valid views for all classes
VIEWS = {
    "AbstractRetrieval": ["META", "META_ABS", "FULL", "REF", "ENTITLED"],
    "AffiliationRetrieval": ["LIGHT", "STANDARD", "ENTITLED"],
    "AffiliationSearch": ["STANDARD"],
    "ArticleEntitlement": ["FULL"],
    "ArticleMetadata": ["STANDARD", "COMPLETE"],
    "ArticleRetrieval": ["META", "META_ABS", "META_ABS_REF", "FULL", "ENTITLED"],
    "AuthorRetrieval": ["LIGHT", "STANDARD", "ENHANCED", "METRICS", "ENTITLED"],
    "AuthorSearch": ["STANDARD"],
    "CitationOverview": ["STANDARD"],
    "PlumXMetrics": ["ENHANCED"],
    "ScDirSubjectClassifications": [''],
    "ScienceDirectSearch": ["STANDARD"],
    "ScopusSearch": ["STANDARD", "COMPLETE"],
    "SerialSearch": ["STANDARD", "ENHANCED", "CITESCORE"],
    "SerialTitle": ["STANDARD", "ENHANCED", "CITESCORE"],
    "SubjectClassifications": [''],
    "ObjectMetadata": ["META"],
    "ObjectRetrieval": [""]
}

# APIs whose URL needs an id_type
APIS_WITH_ID_TYPE = {"AbstractRetrieval",
                     "PlumXMetrics",
                     "ArticleRetrieval",
                     "ArticleEntitlement",
                     "ObjectMetadata",
                     "ObjectRetrieval"}

# Item per page limits for all classes
COUNTS = {
    "AffiliationSearch": {"STANDARD": 200},
    "AuthorSearch": {"STANDARD": 200},
    "ArticleMetadata": {"STANDARD": 200, "COMPLETE": 25},
    "ScDirSubjectClassifications": {"": 200},
    "ScienceDirectSearch": {"STANDARD": 100},
    "ScopusSearch": {"STANDARD": 200, "COMPLETE": 25},
    "SerialSearch": {"STANDARD": 200, "ENHANCED": 200, "CITESCORE": 200},
    "SubjectClassifications": {"": 200}
}

# Throttling limits (in queries per second) // 0 = no limit
RATELIMITS = {
    'AbstractRetrieval': 9,
    'AffiliationRetrieval': 9,
    'AffiliationSearch': 6,
    'ArticleEntitlement': 0,
    'ArticleMetadata': 6,
    'ArticleRetrieval': 10,
    'AuthorRetrieval': 3,
    'AuthorSearch': 2,
    'CitationOverview': 4,
    'ObjectMetadata': 0,
    'ObjectRetrieval': 0,
    'PlumXMetrics': 6,
    'ScDirSubjectClassifications': 0,
    'ScienceDirectSearch': 2,
    'ScopusSearch': 9,
    'SerialSearch': 6,
    'SerialTitle': 6,
    'SubjectClassifications': 0
}

# Other API restrictions
SEARCH_MAX_ENTRIES = 5_000
