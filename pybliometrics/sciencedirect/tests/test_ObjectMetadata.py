"""Tests for ObjectMetadata() class."""

from collections import namedtuple

from pybliometrics.sciencedirect import init, ObjectMetadata

init()

om_1 = ObjectMetadata('10.1016/j.neunet.2024.106632', refresh=30)
om_2 = ObjectMetadata('S2213305418300365', id_type='pii', refresh=30)


def test_results():
    """Tests the length and fields of `results`."""
    fields = ('eid', 'filename', 'height', 'mimetype', 'ref', 'size', 'type', 'url', 'width')
    metadata = namedtuple('Metadata', fields)

    assert om_1.results[0]._fields == fields
    assert len(om_1.results) == 355

    expected_om_1 = metadata(eid='1-s2.0-S0893608024005562-gr3.jpg',
                         filename='gr3.jpg',
                         height=729,
                         mimetype='image/jpeg',
                         ref='gr3',
                         size=100202,
                         type='IMAGE-DOWNSAMPLED',
                         url='https://api.elsevier.com/content/object/eid/1-s2.0-S0893608024005562-gr3.jpg?httpAccept=%2A%2F%2A',
                         width=656)

    assert om_1.results[0] == expected_om_1

    assert om_2.results[2]._fields == fields
    assert len(om_2.results) == 18

    expected_om_2 = metadata(eid='1-s2.0-S2213305418300365-gr2.sml',
                             filename='gr2.sml',
                             height=146,
                             mimetype='image/gif',
                             ref='gr2',
                             size=14910,
                             type='IMAGE-THUMBNAIL',
                             url='https://api.elsevier.com/content/object/eid/1-s2.0-S2213305418300365-gr2.sml?httpAccept=%2A%2F%2A',
                             width=219)

    assert om_2.results[2] == expected_om_2
