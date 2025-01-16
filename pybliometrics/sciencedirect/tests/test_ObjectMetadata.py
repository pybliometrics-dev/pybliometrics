"""Tests for ObjectMetadata"""

from pybliometrics.sciencedirect import init, ObjectMetadata

init()

om_1 = ObjectMetadata('10.1016/j.neunet.2024.106632', refresh=30)
om_2 = ObjectMetadata('S2213305418300365', refresh=30)


def test_len():
    """Tests whether the number of results is correct."""
    assert len(om_1.results) == 355
    assert len(om_2.results) == 18


def test_results():
    """Tests whether the results are correct."""
    obj = om_1.results[0]
    expected_url = 'https://api.elsevier.com/content/object/eid/1-s2.0-S0893608024005562-gr3.jpg?httpAccept=%2A%2F%2A'
    assert obj.get('url') == expected_url
    assert obj.get('eid') == '1-s2.0-S0893608024005562-gr3.jpg'
    assert obj.get('ref') == 'gr3'
    assert obj.get('filename') == 'gr3.jpg'
    assert obj.get('mimetype') == 'image/jpeg'
    assert obj.get('size') == '100202'
    assert obj.get('height') == '729'
    assert obj.get('width') == '656'
    assert obj.get('type') == 'IMAGE-DOWNSAMPLED'


def test_str():
    """Tests whether the __str__ method works correctly."""
    assert str(om_1) == 'Document with doi 10.1016/j.neunet.2024.106632 contains 355 objects.'
    assert str(om_2) == 'Document with pii S2213305418300365 contains 18 objects.'
