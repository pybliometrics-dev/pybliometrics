from os.path import expanduser

# Paths for cached files
DEFAULT_PATHS = {
    'AbstractRetrieval': expanduser('~/.scopus/abstract_retrieval'),
    'AffiliationSearch': expanduser('~/.scopus/affiliation_search'),
    'AuthorRetrieval': expanduser('~/.scopus/author_retrieval'),
    'AuthorSearch': expanduser('~/.scopus/author_search'),
    'CitationOverview': expanduser('~/.scopus/citation_overview'),
    'ContentAffiliationRetrieval': expanduser('~/.scopus/affiliation_retrieval'),
    'ScopusSearch': expanduser('~/.scopus/scopus_search'),
    'SerialTitle': expanduser('~/.scopus/serial_title')
}

# URL prefix and suffixes for retrieval classes
RETRIEVAL_BASE = 'https://api.elsevier.com/content/'
RETRIEVAL_URL = {
    'AbstractRetrieval': RETRIEVAL_BASE + 'abstract/',
    'AuthorRetrieval': RETRIEVAL_BASE + 'author/author_id/',
    'CitationOverview': RETRIEVAL_BASE + 'abstract/citations/',
    'ContentAffiliationRetrieval': RETRIEVAL_BASE + 'affiliation/affiliation_id/',
    'SerialTitle': RETRIEVAL_BASE + 'serial/title/issn/'
}

# URL prefix and suffixes for search classes
SEARCH_BASE = 'https://api.elsevier.com/content/search/'
SEARCH_URL = {
    'AffiliationSearch': SEARCH_BASE + 'affiliation',
    'AuthorSearch': SEARCH_BASE + 'author',
    'ScopusSearch': SEARCH_BASE + 'scopus'
}