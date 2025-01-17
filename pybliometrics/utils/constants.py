from pathlib import Path

# Location of configuration file with legacy support
config_options = [
    Path.home() / ".scopus" / "config.ini",
    Path.home() / ".pybliometrics" / "Scopus" / "config.ini",
    Path.home() / ".config" / "pybliometrics.cfg"  # default
]
CONFIG_FILE = next((path for path in config_options if path.exists()),
                   config_options[-1])
# Location of Scopus cache with legacy support
base_path_options = [
    Path.home() / ".scopus",
    Path.home() / ".pybliometrics" / "Scopus",
    Path.home() / ".cache" / "pybliometrics" / "Scopus"  # default
]
BASE_PATH_SCOPUS = next((path for path in base_path_options if path.exists()),
                        base_path_options[-1])
# Location of ScienceDirect cache
BASE_PATH_SCIENCEDIRECT = Path.home() / ".cache" / "pybliometrics" / "ScienceDirect"

# Location of Scival cache
BASE_PATH_SCIVAL = Path.home() / ".cache" / "pybliometrics" / "Scival"

DEFAULT_PATHS = {
    'AbstractRetrieval': BASE_PATH_SCOPUS / 'abstract_retrieval',
    'AffiliationRetrieval': BASE_PATH_SCOPUS / 'affiliation_retrieval',
    'AffiliationSearch': BASE_PATH_SCOPUS / 'affiliation_search',
    'ArticleEntitlement': BASE_PATH_SCIENCEDIRECT / 'article_entitlement',
    'ArticleMetadata': BASE_PATH_SCIENCEDIRECT / 'article_metadata / ',
    'ArticleRetrieval': BASE_PATH_SCIENCEDIRECT / 'article_retrieval',
    'AuthorRetrieval': BASE_PATH_SCOPUS / 'author_retrieval',
    'AuthorSearch': BASE_PATH_SCOPUS / 'author_search',
    'CitationOverview': BASE_PATH_SCOPUS / 'citation_overview',
    'PlumXMetrics': BASE_PATH_SCOPUS / 'plumx',
    'PublicationLookup': BASE_PATH_SCIVAL / 'publication_lookup',
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
SCIVAL_BASE = 'https://api.elsevier.com/analytics/scival/'


URLS = {
    'AbstractRetrieval': RETRIEVAL_BASE + 'abstract/',
    'AffiliationRetrieval': RETRIEVAL_BASE + 'affiliation/affiliation_id/',
    'AffiliationSearch': SEARCH_BASE + 'affiliation',
    'ArticleEntitlement': RETRIEVAL_BASE + 'article/entitlement/',
    'ArticleMetadata': RETRIEVAL_BASE + 'metadata/article/',
    'ArticleRetrieval': RETRIEVAL_BASE + 'article/',
    'AuthorRetrieval': RETRIEVAL_BASE + 'author/author_id/',
    'AuthorSearch': SEARCH_BASE + 'author',
    'CitationOverview': RETRIEVAL_BASE + 'abstract/citations/',
    'PlumXMetrics': 'https://api.elsevier.com/analytics/plumx/',
    'PublicationLookup': SCIVAL_BASE + 'publication/',
    'ScopusSearch': SEARCH_BASE + 'scopus',
    'ScienceDirectSearch': SEARCH_BASE + 'sciencedirect/',
    'ScDirSubjectClassifications': RETRIEVAL_BASE + 'subject/scidir/',
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
    'PlumXMetrics': 6,
    'PublicationLookup': 6,
    'ScDirSubjectClassifications': 0,
    'ScienceDirectSearch': 2,
    'ScopusSearch': 9,
    'SerialSearch': 6,
    'SerialTitle': 6,
    'SubjectClassifications': 0,
}

# Other API restrictions
SEARCH_MAX_ENTRIES = 5_000
