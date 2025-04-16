"""Test pybliometrics.sciencedirect.SerialTitle()"""

from collections import namedtuple

from pybliometrics.sciencedirect import SerialTitle, init

init()

gene = SerialTitle('03781119', view='ENHANCED', refresh=30)

def test_module():
    assert gene.__module__  == 'pybliometrics.scopus.serial_title'


def test_aggregation_type():
    assert gene.aggregation_type == "journal"


def test_citescoreyearinfolist():
    info_fields = 'year citescore'
    info = namedtuple('Citescoreinfolist', info_fields)

    # Test softwarex
    expected_named_tuple = [info(year=2023, citescore=6.1),
                            info(year=2024, citescore=5.1)]
    assert gene.citescoreyearinfolist == expected_named_tuple


def test_eissn():
    assert gene.eissn == "1879-0038"


def test_issn():
    assert gene.issn == "0378-1119"


def test_oaallowsauthorpaid():
    assert gene.oaallowsauthorpaid is True


def test_openaccess():
    assert gene.openaccess == 0


def test_openaccessstartdate():
    assert gene.openaccessstartdate is None


def test_openaccesstype():
    assert gene.openaccesstype == 'None'


def test_openaccessarticle():
    assert gene.openaccessarticle is False


def test_openarchivearticle():
    assert gene.openarchivearticle is False


def test_openaccesssponsorname():
    assert gene.openaccesssponsorname is None


def test_openaccessuserlicense():
    assert gene.openaccessuserlicense is None


def test_publisher():
    assert gene.publisher == 'Elsevier B.V.'


def test_scopus_source_link():
    expected1 = 'https://www.scopus.com/source/sourceInfo.url?sourceId=15636'
    assert gene.scopus_source_link == expected1


def test_self_link():
    expected1 = 'https://api.elsevier.com/content/serial/title/issn/03781119'
    assert gene.self_link == expected1


def test_sjrlist():
    assert gene.sjrlist == [(2023, 0.725)]


def test_sniplist():
    assert gene.sniplist == [(2023, 0.765)]


def test_source_id():
    assert gene.source_id == 15636


def test_subject_area():
    area = namedtuple('Subjectarea', 'area abbreviation code')
    expected1 = [
        area(area='Genetics', abbreviation='BIOC', code=1311)
    ]
    assert gene.subject_area == expected1


def test_title():
    assert gene.title == 'Gene'


def test_yearly_data():
    assert isinstance(gene.yearly_data, list)
    assert len(gene.yearly_data) == 30
    fields = 'year publicationcount revpercent zerocitessce '\
             'zerocitespercentsce citecountsce'
    dat = namedtuple('Yearlydata', fields)
    expected1_2023 = dat(year=2023, publicationcount=654, revpercent=8.56,
        zerocitessce=89, zerocitespercentsce=13.608562691131498,
        citecountsce=32424)
    assert gene.yearly_data[27] == expected1_2023
