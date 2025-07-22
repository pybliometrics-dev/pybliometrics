from pybliometrics.scival.publication_lookup import PublicationLookup
from pybliometrics.utils.startup import init

init()

pub1 = PublicationLookup('85036568406')


def test_publication_authors_count():
    assert len(pub1.authors) >= 7


def test_publication_citation_count():
    assert pub1.citation_count > 0


def test_publication_doi():
    assert pub1.doi == "10.1002/anie.201709271"


def test_publication_first_author():
    assert pub1.authors[0].id == 7404861905
    assert pub1.authors[0].name == "Lin, T.-E."
    assert pub1.authors[0].uri == "Author/7404861905"


def test_publication_first_institution():
    assert pub1.institutions[0].id == 217002
    assert pub1.institutions[0].name == "Chang Gung University"
    assert pub1.institutions[0].country == "Taiwan"
    assert pub1.institutions[0].country_code == "TWN"


def test_publication_id():
    assert pub1.id == 85036568406


def test_publication_institutions_count():
    assert len(pub1.institutions) >= 3


def test_publication_sdgs():
    assert len(pub1.sdgs) >= 1
    assert pub1.sdgs[0] == 'SDG 3: Good Health and Well-being'


def test_publication_source_title():
    assert pub1.source_title == 'Angewandte Chemie - International Edition'


def test_publication_type():
    assert pub1.type == "Article"


def test_publication_year():
    assert pub1.publication_year == 2017
