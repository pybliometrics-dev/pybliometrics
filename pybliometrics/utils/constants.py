from pathlib import Path

# Location of configuration file with legacy support
config_path_options = [
    Path.home() / ".scopus" / "config.ini",
    Path.home() / ".pybliometrics" / "Scopus" / "config.ini",
    Path.home() / ".config" / "pybliometrics.cfg"  # default
]
CONFIG_FILE = next((path for path in config_path_options if path.exists()),
                   config_path_options[-1])

# Location of cache with legacy support
cache_path_options = [
    Path.home() / ".scopus",
    Path.home() / ".pybliometrics",
    Path.home() / ".cache" / "pybliometrics"  # default
]
CACHE_PATH = next((path for path in cache_path_options if path.exists()),
                 cache_path_options[-1])

DEFAULT_PATHS = {
    'AbstractRetrieval': CACHE_PATH / "Scopus" / 'abstract_retrieval',
    'AffiliationRetrieval': CACHE_PATH / "Scopus" / 'affiliation_retrieval',
    'AffiliationSearch': CACHE_PATH / "Scopus" / 'affiliation_search',
    'AuthorRetrieval': CACHE_PATH / "Scopus" / 'author_retrieval',
    'AuthorSearch': CACHE_PATH / "Scopus" / 'author_search',
    'ArticleEntitlement': CACHE_PATH / "ScienceDirect" / 'article_entitlement',
    'ArticleMetadata': CACHE_PATH / "ScienceDirect" / 'article_metadata',
    'ArticleRetrieval': CACHE_PATH / "ScienceDirect" / 'article_retrieval',
    'NonserialTitle': CACHE_PATH / "ScienceDirect" / 'nonserial_title',
    'CitationOverview': CACHE_PATH / "Scopus" / 'citation_overview',
    'ObjectMetadata': CACHE_PATH / "ScienceDirect" / 'object_metadata',
    'ObjectRetrieval': CACHE_PATH / "ScienceDirect" / 'object_retrieval',
    'PlumXMetrics': CACHE_PATH / "Scopus" / 'plumx',
    'ScDirSubjectClassifications': CACHE_PATH / "ScienceDirect" / 'subject_classification',
    'ScienceDirectSearch': CACHE_PATH / "ScienceDirect" / 'science_direct_search',
    'ScopusSearch': CACHE_PATH / "Scopus" / 'scopus_search',
    'SerialSearch': CACHE_PATH / "Scopus" / 'serial_search',
    'SerialTitle': CACHE_PATH / "Scopus" / 'serial_title',
    'SubjectClassifications': CACHE_PATH / "Scopus" / 'subject_classification',
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
    'NonserialTitle': RETRIEVAL_BASE + 'nonserial/title/isbn/',
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
    "NonserialTitle": ["STANDARD"],
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
    'NonserialTitle': 6,
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
