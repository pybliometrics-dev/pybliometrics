"""Tests for sciencedirect.ArticleRetrieval"""
from collections import namedtuple

from pybliometrics.sciencedirect import ArticleRetrieval
from pybliometrics.scopus import init

init()

ar_full = ArticleRetrieval('S2949948823000112', view='FULL', refresh=30)


def test_abstract():
    abstract_full = 'Artificial Neural Networks (ANNs) are a type of machine learning algorithm inspired by the structure and function of the human brain. In the context of supply chain management, ANNs can be used for demand forecasting, inventory optimization, logistics planning, and anomaly detection. ANNs help companies to optimize their inventory levels, production schedules and procurement activities in terms of productivity enhancement of part production. By considering multiple variables and constraints, ANNs can identify the most efficient routes, allocate resources effectively, and reduce costs. Furthermore, ANNs can identify anomalies as well as abnormalities in supply chain data, such as unexpected demand patterns, quality issues and disruptions in logistics operations in order to minimize their impact on the supply chain. ANNs can also analyze supplier performance data, including quality, delivery times and pricing in order to assess the reliability and effectiveness of suppliers. This information can support decision-making processes in supplier evaluation and selection processes. Moreover, ANNs can continuously monitor supplier performance, raising alerts for deviations from predefined criteria to provide safe and secure supply chain in part production processes. By analyzing various data sources, including weather conditions, and political instability, ANNs can identify and mitigate risks in terms of safety enhancement of supply chain processes. Artificial neural networks in supply chain management is studied in the research work to analyze and enhance performances of supply chain management in process of part manufacturing. New ideas and concepts of future research works are presented by reviewing and analyzing of recent achievements in applications of artificial neural networks in supply chain management. Thus, productivity of part manufacturing can be enhanced by promoting the supply chain management using the artificial neural networks.'
    assert ar_full.abstract == abstract_full


def test_aggregationType():
    assert ar_full.aggregationType == 'Journal'


def test_authors():
    auth = namedtuple('Author', 'surname given_name')
    authors_full = [auth(surname='Soori', given_name=' Mohsen'),
                          auth(surname='Arezoo', given_name=' Behrooz'),
                          auth(surname='Dastres', given_name=' Roza')]
    assert ar_full.authors == authors_full


def test_copyright():
    assert ar_full.copyright == '© 2024 The Author(s). Published by Elsevier B.V. on behalf of KeAi Communications Co., Ltd.'


def test_coverDate():
    assert ar_full.coverDate == '2023-11-30'


def test_coverDisplayDate():
    assert ar_full.coverDisplayDate == 'November 2023'


def test_doi():
    assert ar_full.doi == '10.1016/j.ject.2023.11.002'


def test_eid():
    assert ar_full.eid == '1-s2.0-S2949948823000112'


def test_endingPage():
    assert ar_full.endingPage == '196'


def test_issn():
    assert ar_full.issn == 29499488


def test_openArchiveArticle():
    assert ar_full.openArchiveArticle is False


def test_openaccess():
    assert ar_full.openaccess is True


def test_openaccessSponsorName():
    assert ar_full.openaccessSponsorName == 'KeAi Communications Co., Ltd'


def test_openaccessSponsorType():
    assert ar_full.openaccessSponsorType == 'FundingBody'


def test_openaccessType():
    assert ar_full.openaccessType == 'Full'


def test_openaccessUserLicense():
    assert ar_full.openaccessUserLicense == 'http://creativecommons.org/licenses/by/4.0/'


def test_pageRange():
    assert ar_full.pageRange == '179-196'


def test_pii():
    assert ar_full.pii == 'S2949-9488(23)00011-2'


def test_pubType():
    assert ar_full.pubType == 'rev'


def test_publicationName():
    assert ar_full.publicationName == 'Journal of Economy and Technology'


def test_publisher():
    publisher_full = 'The Author(s). Published by Elsevier B.V. on behalf of KeAi Communications Co., Ltd.'
    assert ar_full.publisher == publisher_full


def test_sciencedirect_link():
    sciencedirect_link_full = 'https://www.sciencedirect.com/science/article/pii/S2949948823000112'
    assert ar_full.sciencedirect_link == sciencedirect_link_full


def test_self_link():
    assert ar_full.self_link == 'https://api.elsevier.com/content/article/pii/S2949948823000112'


def test_startingPage():
    assert ar_full.startingPage == '179'


def test_subjects():
    assert ar_full.subjects == ['Artificial neural networks', 'Supply chain management']


def test_title():
    assert ar_full.title == 'Artificial neural networks in supply chain management, a review'


def test_url():
    assert ar_full.url == 'https://api.elsevier.com/content/article/pii/S2949948823000112'


def test_volume():
    assert ar_full.volume == 1
