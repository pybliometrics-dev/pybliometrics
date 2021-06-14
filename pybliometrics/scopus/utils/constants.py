from pathlib import Path

# Paths for cached files
if (Path.home()/".scopus").exists():
    BASE_PATH = Path.home()/".scopus"
else:
    BASE_PATH = Path.home()/".pybliometrics"/"Scopus"
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

# URL prefix and suffixes for retrieval classes
RETRIEVAL_BASE = 'https://api.elsevier.com/content/'
RETRIEVAL_URL = {
    'AbstractRetrieval': RETRIEVAL_BASE + 'abstract/',
    'AffiliationRetrieval': RETRIEVAL_BASE + 'affiliation/affiliation_id/',
    'AuthorRetrieval': RETRIEVAL_BASE + 'author/author_id/',
    'CitationOverview': RETRIEVAL_BASE + 'abstract/citations/',
    'SerialTitle': RETRIEVAL_BASE + 'serial/title/issn/',
    'PlumXMetrics': 'https://api.elsevier.com/analytics/plumx/',
}

# URL prefix and suffixes for search classes
SEARCH_BASE = 'https://api.elsevier.com/content/search/'
SEARCH_URL = {
    'AffiliationSearch': SEARCH_BASE + 'affiliation',
    'AuthorSearch': SEARCH_BASE + 'author',
    'ScopusSearch': SEARCH_BASE + 'scopus',
    'SerialSearch': RETRIEVAL_BASE + 'serial/title',
    'SubjectClassifications': RETRIEVAL_BASE + 'subject/scopus'
}
