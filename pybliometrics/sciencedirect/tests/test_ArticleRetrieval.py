"""Tests for sciencedirect.ArticleRetrieval"""
from collections import namedtuple

from pybliometrics.sciencedirect import ArticleRetrieval, init

init()

ar_full = ArticleRetrieval('S2949948823000112', view='FULL', refresh=30)
ar_meta = ArticleRetrieval("10.1016/j.procs.2018.05.069", id_type='doi', view='META', refresh=30)
ar_meta_abs = ArticleRetrieval("S0304387823001736", view='META_ABS', refresh=30)
ar_meta_abs_ref = ArticleRetrieval("S2352226722000630", view='META_ABS_REF', refresh=30)
ar_entitled = ArticleRetrieval("S2213305418300365", view='ENTITLED', refresh=30)


def test_abstract():
    abstract_full = 'Artificial Neural Networks (ANNs) are a type of machine learning algorithm inspired by the structure and function of the human brain. In the context of supply chain management, ANNs can be used for demand forecasting, inventory optimization, logistics planning, and anomaly detection. ANNs help companies to optimize their inventory levels, production schedules and procurement activities in terms of productivity enhancement of part production. By considering multiple variables and constraints, ANNs can identify the most efficient routes, allocate resources effectively, and reduce costs. Furthermore, ANNs can identify anomalies as well as abnormalities in supply chain data, such as unexpected demand patterns, quality issues and disruptions in logistics operations in order to minimize their impact on the supply chain. ANNs can also analyze supplier performance data, including quality, delivery times and pricing in order to assess the reliability and effectiveness of suppliers. This information can support decision-making processes in supplier evaluation and selection processes. Moreover, ANNs can continuously monitor supplier performance, raising alerts for deviations from predefined criteria to provide safe and secure supply chain in part production processes. By analyzing various data sources, including weather conditions, and political instability, ANNs can identify and mitigate risks in terms of safety enhancement of supply chain processes. Artificial neural networks in supply chain management is studied in the research work to analyze and enhance performances of supply chain management in process of part manufacturing. New ideas and concepts of future research works are presented by reviewing and analyzing of recent achievements in applications of artificial neural networks in supply chain management. Thus, productivity of part manufacturing can be enhanced by promoting the supply chain management using the artificial neural networks.'
    abstract_meta_abs = 'This paper quantifies the relative footprint of trade and agricultural productivity on deforestation across Brazilian municipalities between 2000 and 2017. Using remote-sensing data, we identify distinct effects of these two phenomena on land use. Greater exposure to new genetically engineered soy seeds is associated with faster deforestation through cropland expansion. We find no significant association between local exposure to Chinese demand and deforestation, but exposure to trade with China mitigates the deforestation impacts from the new soy technology. Our findings suggest that, when considered together, productivity gains altering municipalities’ comparative advantage played a more significant role in driving deforestation across Brazil than Chinese demand alone.'
    abstract_meta_abs_ref = 'Subsidence along the central coast of the Ganges-Brahmaputra Delta and a subsequent rapid burial by mangrove mud have preserved a hundred earthen kilns at 11 localities, exposed due to recent coastal erosion. The associated pottery indicates that the kilns were used for salt crystallization in brine pots mounted on perforated hotplates. Four kiln varieties were found at successive elevations. The kiln chamber walls and the basal charcoal layers were dated using thermoluminescence and radiocarbon dating respectively. The oldest kilns with a round outline, found at the lowest elevations, were operating in the early 8th to middle 9th century. Oval-shaped kilns, found at a 1-m higher elevation, were used from the mid-9th to early 10th century. After a 600-year long period without documented kilns, rectangular kilns with a lateral slot were built again at a 1-m higher land surface in the 16th and 17th century. The youngest kiln type consists of rectangular twin chambers dating from the late 16th to mid-18th century and occurs at 1.5\xa0m below the present sediment surface. Architecture and functioning of these rectangular kilns are reconstructed, showing a multi-step procedure. This technique had been improved in the 19th century when pyramidal kilns were described in historic records.'
    assert ar_full.abstract == abstract_full
    assert ar_meta.abstract is None
    assert ar_meta_abs.abstract == abstract_meta_abs
    assert ar_meta_abs_ref.abstract == abstract_meta_abs_ref


def test_aggregationType():
    assert ar_full.aggregationType == 'Journal'
    assert ar_meta.aggregationType == 'Journal'
    assert ar_meta_abs.aggregationType == 'Journal'
    assert ar_meta_abs_ref.aggregationType == 'Journal'


def test_authors():
    auth = namedtuple('Author', 'surname given_name')
    authors_full = [auth(surname='Soori', given_name='Mohsen'),
                          auth(surname='Arezoo', given_name='Behrooz'),
                          auth(surname='Dastres', given_name='Roza')]
    authors_meta = [auth(surname='Indolia', given_name='Sakshi'),
                    auth(surname='Goswami', given_name='Anil Kumar'),
                    auth(surname='Mishra', given_name='S.P.'),
                    auth(surname='Asopa', given_name='Pooja')]
    authors_meta_abs = [auth(surname='Carreira', given_name='Igor'),
                        auth(surname='Costa', given_name='Francisco'),
                        auth(surname='Pessoa', given_name='João Paulo')]
    authors_meta_abs_ref = [auth(surname='Kudrass', given_name='H.R.'),
                            auth(surname='Hanebuth', given_name='T.J.J.'),
                            auth(surname='Zander', given_name='A.M.'),
                            auth(surname='Linstädter', given_name='J.'),
                            auth(surname='Akther', given_name='S.H.'),
                            auth(surname='Shohrab', given_name='U.M.')]
    assert ar_full.authors == authors_full
    assert ar_meta.authors == authors_meta
    assert ar_meta_abs.authors == authors_meta_abs
    assert ar_meta_abs_ref.authors == authors_meta_abs_ref


def test_copyright():
    copyright_full = '© 2024 The Author(s). Published by Elsevier B.V. on behalf of KeAi Communications Co., Ltd.'
    copyright_meta = '© 2018 The Author(s). Published by Elsevier B.V.'
    copyright_meta_abs = '© 2023 Elsevier B.V. All rights reserved.'
    copyright_meta_abs_ref = '© 2022 The Authors. Published by Elsevier Ltd.'
    assert ar_full.copyright == copyright_full
    assert ar_meta.copyright == copyright_meta
    assert ar_meta_abs.copyright == copyright_meta_abs
    assert ar_meta_abs_ref.copyright == copyright_meta_abs_ref


def test_coverDate():
    assert ar_full.coverDate == '2023-11-30'
    assert ar_meta.coverDate == '2018-12-31'
    assert ar_meta_abs.coverDate == '2024-03-31'
    assert ar_meta_abs_ref.coverDate == '2022-12-31'


def test_coverDisplayDate():
    assert ar_full.coverDisplayDate == 'November 2023'
    assert ar_meta.coverDisplayDate == '2018'
    assert ar_meta_abs.coverDisplayDate == 'March 2024'
    assert ar_meta_abs_ref.coverDisplayDate == 'December 2022'


def test_document_entitlement_status():
    assert ar_entitled.document_entitlement_status == 'ENTITLED'


def test_doi():
    assert ar_full.doi == '10.1016/j.ject.2023.11.002'
    assert ar_meta.doi == '10.1016/j.procs.2018.05.069'
    assert ar_meta_abs.doi == '10.1016/j.jdeveco.2023.103217'
    assert ar_meta_abs_ref.doi == '10.1016/j.ara.2022.100412'


def test_eid():
    assert ar_full.eid == '1-s2.0-S2949948823000112'
    assert ar_meta.eid == '1-s2.0-S1877050918308019'
    assert ar_meta_abs.eid == '1-s2.0-S0304387823001736'
    assert ar_meta_abs_ref.eid == '1-s2.0-S2352226722000630'


def test_endingPage():
    assert ar_full.endingPage == '196'
    assert ar_meta.endingPage == '688'
    assert ar_meta_abs.endingPage is None
    assert ar_meta_abs_ref.endingPage is None


def test_issn():
    assert ar_full.issn == 29499488
    assert ar_meta.issn == 18770509
    assert ar_meta_abs.issn == 3043878
    assert ar_meta_abs_ref.issn == 23522267


def test_openArchiveArticle():
    assert ar_full.openArchiveArticle is False
    assert ar_meta.openArchiveArticle is False
    assert ar_meta_abs.openArchiveArticle is False
    assert ar_meta_abs_ref.openArchiveArticle is False


def test_openaccess():
    assert ar_full.openaccess is True
    assert ar_meta.openaccess is True
    assert ar_meta_abs.openaccess is False
    assert ar_meta_abs_ref.openaccess is True


def test_openaccessSponsorName():
    assert ar_full.openaccessSponsorName == 'KeAi Communications Co., Ltd'
    assert ar_meta.openaccessSponsorName is None
    assert ar_meta_abs.openaccessSponsorName is None
    assert ar_meta_abs_ref.openaccessSponsorName is None


def test_openaccessSponsorType():
    assert ar_full.openaccessSponsorType == 'FundingBody'
    assert ar_meta.openaccessSponsorType == 'ElsevierWaived'
    assert ar_meta_abs.openaccessSponsorType is None
    assert ar_meta_abs_ref.openaccessSponsorType == 'Author'


def test_openaccessType():
    assert ar_full.openaccessType == 'Full'
    assert ar_meta.openaccessType == 'Full'
    assert ar_meta_abs.openaccessType is None
    assert ar_meta_abs_ref.openaccessType == 'Full'


def test_openaccessUserLicense():
    assert ar_full.openaccessUserLicense == 'http://creativecommons.org/licenses/by/4.0/'
    assert ar_meta.openaccessUserLicense == 'http://creativecommons.org/licenses/by-nc-nd/4.0/'
    assert ar_meta_abs.openaccessUserLicense is None
    assert ar_meta_abs_ref.openaccessUserLicense == 'http://creativecommons.org/licenses/by/4.0/'


def test_originalText():
    ar_full_test_originalText = 'c and Kuźnar, 2021). By analyzing data from multiple sources, including social media, news feeds, and sensor data, ANNs can provide early warnings and recommend proactive measures to mitigate potential risks. ANNs can be used to identify and mitigate supply chain risks by analyzing historical data and external factors (Liu, 2022). By training an ANN model with historical risk data and relevant variables, it can identify patterns and correlations which can be used in assessing the likelihood and impacts of potential risks, such as supplier disruptions, natural disasters and market volatility (Kosasih et al., 2022). This information allows organizations to take proactive measures to mitigate risks and improve supply chain resilience. ANNs can be used to analyze and mitigate risks at various stages of the supply chain, including procurement, production, transportation, and distribution during advanced supply chain management (Jianying et al., 2021). Here are some ways ANNs are used in supply chain risk analysis and mitigation: 1. Demand Forecasting: ANNs can be used to predict future demand patterns based on historical sales data, market trends, and other relevant factors. Accurate demand forecasting helps in inventory management and reduces the risk of stockouts or excess inventory (Aamer et al., 2020). 2. Supplier Evaluation: ANNs can assess supplier performance by analyzing various factors such as quality, delivery reliability, and pricing. By considering historical data and other relevant variables, ANNs can identify high-risk suppliers and help in making informed decisions about supplier selection and management (Hui and Choi, 2016). 3. Quality Control: ANNs can analyze quality-related data to identify patterns and anomalies that may indicate potential quality issues. By monitoring and analyzing data from production processes and quality inspections, ANNs can help in early detection and mitigation of quality-related risks (Cai et al., 2020; Minis, 2007). 4. Transp'
    assert ar_full.originalText[-80000:-78000] == ar_full_test_originalText


def test_pageRange():
    assert ar_full.pageRange == '179-196'
    assert ar_meta.pageRange == '679-688'
    assert ar_meta_abs.pageRange == '103217'
    assert ar_meta_abs_ref.pageRange == '100412'


def test_pii():
    assert ar_full.pii == 'S2949-9488(23)00011-2'
    assert ar_meta.pii == 'S1877-0509(18)30801-9'
    assert ar_meta_abs.pii == 'S0304-3878(23)00173-6'
    assert ar_meta_abs_ref.pii == 'S2352-2267(22)00063-0'


def test_pubType():
    assert ar_full.pubType == 'rev'
    assert ar_meta.pubType == 'fla'
    assert ar_meta_abs.pubType == 'fla'
    assert ar_meta_abs_ref.pubType == 'fla'


def test_publicationName():
    assert ar_full.publicationName == 'Journal of Economy and Technology'
    assert ar_meta.publicationName == 'Procedia Computer Science'
    assert ar_meta_abs.publicationName == 'Journal of Development Economics'
    assert ar_meta_abs_ref.publicationName == 'Archaeological Research in Asia'


def test_publisher():
    publisher_full = 'The Author(s). Published by Elsevier B.V. on behalf of KeAi Communications Co., Ltd.'
    assert ar_full.publisher == publisher_full
    assert ar_meta.publisher == 'The Author(s). Published by Elsevier B.V.'
    assert ar_meta_abs.publisher == 'Elsevier B.V.'
    assert ar_meta_abs_ref.publisher == 'The Authors. Published by Elsevier Ltd.'



def test_sciencedirect_link():
    assert ar_full.sciencedirect_link == 'https://www.sciencedirect.com/science/article/pii/S2949948823000112'
    assert ar_meta.sciencedirect_link == 'https://www.sciencedirect.com/science/article/pii/S1877050918308019'
    assert ar_meta_abs.sciencedirect_link == 'https://www.sciencedirect.com/science/article/pii/S0304387823001736'
    assert ar_meta_abs_ref.sciencedirect_link == 'https://www.sciencedirect.com/science/article/pii/S2352226722000630'


def test_self_link():
    assert ar_full.self_link == 'https://api.elsevier.com/content/article/pii/S2949948823000112'
    assert ar_meta.self_link == 'https://api.elsevier.com/content/article/pii/S1877050918308019'
    assert ar_meta_abs.self_link == 'https://api.elsevier.com/content/article/pii/S0304387823001736'
    assert ar_meta_abs_ref.sciencedirect_link == 'https://www.sciencedirect.com/science/article/pii/S2352226722000630'


def test_startingPage():
    assert ar_full.startingPage == '179'
    assert ar_meta.startingPage == '679'
    assert ar_meta_abs.startingPage == '103217'
    assert ar_meta_abs_ref.startingPage == '100412'


def test_subjects():
    assert ar_full.subjects == ['Artificial neural networks', 'Supply chain management']
    assert ar_meta.subjects == ['Convolution Neural Network', 'Deep Neural Network', 'Gradient Descent', 'ADAM']
    assert ar_meta_abs.subjects == ['Deforestation', 'Trade', 'Agricultural productivity', 'Technology', 'Soy', 'Brazil']
    assert ar_meta_abs_ref.subjects == ['Salt production', 'Earthen kiln', 'Ganges-Brahmaputra Delta', 'Sundarbans']


def test_title():
    assert ar_full.title == 'Artificial neural networks in supply chain management, a review'
    assert ar_meta.title == 'Conceptual Understanding of Convolutional Neural Network- A Deep Learning Approach '
    assert ar_meta_abs.title == 'The deforestation effects of trade and agricultural productivity in Brazil '
    assert ar_meta_abs_ref.title == 'Architecture and function of salt-producing kilns from the 8th to 18th century in the coastal Sundarbans mangrove forest, Central Ganges-Brahmaputra Delta, Bangladesh '


def test_url():
    assert ar_full.url == 'https://api.elsevier.com/content/article/pii/S2949948823000112'
    assert ar_meta.url == 'https://api.elsevier.com/content/article/pii/S1877050918308019'
    assert ar_meta_abs.url == 'https://api.elsevier.com/content/article/pii/S0304387823001736'
    assert ar_meta_abs_ref.url == 'https://api.elsevier.com/content/article/pii/S2352226722000630'


def test_volume():
    assert ar_full.volume == 1
    assert ar_meta.volume == 132
    assert ar_meta_abs.volume == 167
    assert ar_meta_abs_ref.volume == 32


def test__str__():
    expected  = 'Mohsen Soori, Behrooz Arezoo and Roza Dastres: "Artificial neural networks in supply chain management, a review", Journal of Economy and Technology, 1, pp. 179-196(2023). https://doi.org/10.1016/j.ject.2023.11.002.'
    assert str(ar_full) == expected
