"""Tests for `scopus.SerialTitle` module."""

import datetime

from collections import namedtuple

from pybliometrics.scopus import SerialTitle, init

init()


# SoftwareX
softwarex = SerialTitle("2352-7110", refresh=30)
# OECD Economic Studies
oecd = SerialTitle("0255-0822", refresh=30)
# Neural Networks
neural_networks = SerialTitle('1879-2782', view='CITESCORE', refresh=30)


def test_aggregation_type():
    assert softwarex.aggregation_type == "journal"
    assert oecd.aggregation_type == "journal"


def test_citescoreyearinfolist():
    info_fields = 'year citescore'
    info = namedtuple('Citescoreinfolist', info_fields)

    # Test softwarex
    expected_named_tuple = [info(year=2023, citescore=5.5),
                            info(year=2024, citescore=3.4)]
    assert softwarex.citescoreyearinfolist == expected_named_tuple

    # Test oecd
    assert oecd.citescoreyearinfolist[0] is None
    assert oecd.citescoreyearinfolist[1] is None

    # Test CITESCORE view
    this_year = datetime.date.today().year
    assert neural_networks.citescoreyearinfolist[0].year == this_year
    assert isinstance(neural_networks.citescoreyearinfolist[3].citationcount, int)


def test_eissn():
    assert softwarex.eissn == "2352-7110"
    assert oecd.eissn == "1609-7491"


def test_issn():
    assert softwarex.issn is None
    assert oecd.issn == "0255-0822"


def test_oaallowsauthorpaid():
    assert softwarex.oaallowsauthorpaid is None
    assert oecd.oaallowsauthorpaid is None


def test_openaccess():
    assert softwarex.openaccess == 1
    assert oecd.openaccess is None


def test_openaccessstartdate():
    assert softwarex.openaccessstartdate is None
    assert oecd.openaccessstartdate is None


def test_openaccesstype():
    assert softwarex.openaccesstype is None
    assert oecd.openaccesstype is None


def test_openaccessarticle():
    assert softwarex.openaccessarticle == True
    assert oecd.openaccessarticle is None


def test_openarchivearticle():
    assert softwarex.openarchivearticle is None
    assert oecd.openarchivearticle is None


def test_openaccesssponsorname():
    assert softwarex.openaccesssponsorname is None
    assert oecd.openaccesssponsorname is None


def test_openaccessuserlicense():
    assert softwarex.openaccessuserlicense is None
    assert oecd.openaccessuserlicense is None


def test_publisher():
    assert softwarex.publisher == "Elsevier B.V."
    assert oecd.publisher == "OECD"


def test_scopus_source_link():
    expected1 = "https://www.scopus.com/source/sourceInfo.url?sourceId=21100422153"
    assert softwarex.scopus_source_link == expected1
    expected2 = "https://www.scopus.com/source/sourceInfo.url?sourceId=24107"
    assert oecd.scopus_source_link == expected2


def test_self_link():
    expected1 = "https://api.elsevier.com/content/serial/title/issn/23527110"
    assert softwarex.self_link == expected1
    expected2 = "https://api.elsevier.com/content/serial/title/issn/02550822"
    assert oecd.self_link == expected2


def test_sjrlist():
    assert softwarex.sjrlist == [(2023, 0.544)]
    assert oecd.sjrlist == [(1999, 2.723)]


def test_sniplist():
    assert softwarex.sniplist == [(2023, 1.5)]
    assert oecd.sniplist is None


def test_source_id():
    assert softwarex.source_id == 21100422153
    assert oecd.source_id == 24107


def test_subject_area():
    area = namedtuple('Subjectarea', 'area abbreviation code')
    expected1 = [
        area(area='Computer Science Applications', abbreviation='COMP', code=1706),
        area(area='Software', abbreviation='COMP', code=1712)
    ]
    assert softwarex.subject_area == expected1
    expected2 = [
        area(area='Geography, Planning and Development', abbreviation='SOCI', code=3305)
    ]
    assert oecd.subject_area == expected2


def test_title():
    assert softwarex.title == "SoftwareX"
    assert oecd.title == "OECD Economic Studies"


def test_yearly_data():
    assert isinstance(softwarex.yearly_data, list)
    assert len(softwarex.yearly_data) == 29
    fields = 'year publicationcount revpercent zerocitessce '\
             'zerocitespercentsce citecountsce'
    dat = namedtuple('Yearlydata', fields)
    expected1_2020 = dat(year=2020, publicationcount=164, revpercent=0.0,
        zerocitessce=8, zerocitespercentsce=4.878048780487805,
        citecountsce=2578)
    assert softwarex.yearly_data[24] == expected1_2020
    expected2_1996 = dat(year=1996, publicationcount=4, revpercent=0.0,
        zerocitessce=0, zerocitespercentsce=0, citecountsce=33)
    assert oecd.yearly_data[0] == expected2_1996
