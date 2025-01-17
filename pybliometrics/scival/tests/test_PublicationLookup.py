from pybliometrics.scival import PublicationLookup
from pybliometrics.utils import init

init()

# Base information
pub1 = PublicationLookup(85036568406)


def test_publication():
    assert pub1.id == 85036568406
    assert pub1.doi == "10.1002/anie.201709271"
    assert pub1.type == "Article"
    assert pub1.publication_year == 2017
    assert pub1.source_title == 'Angewandte Chemie - International Edition'
    assert pub1.citation_count > 0
    assert len(pub1.authors) >= 7
    assert pub1.authors[0].id == 7404861905
    assert pub1.authors[0].name == "Lin, T.-E."
    assert len(pub1.institutions) >= 3
    assert pub1.institutions[0].id == 217002
    assert pub1.institutions[0].name == "Chang Gung University"
    assert pub1.institutions[0].country == "Taiwan"
    assert pub1.institutions[0].country_code == "TWN"
    assert len(pub1.sdgs) >= 1
    assert pub1.sdgs[0] == 'SDG 3: Good Health and Well-being'