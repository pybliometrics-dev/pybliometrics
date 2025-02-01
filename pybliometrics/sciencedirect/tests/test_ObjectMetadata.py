"""Tests for ObjectMetadata() class."""

from pybliometrics.sciencedirect import init, ObjectMetadata

init()

om_1 = ObjectMetadata('10.1016/j.neunet.2024.106632', refresh=30)
om_2 = ObjectMetadata('S2213305418300365', id_type='pii', refresh=30)


def test_results():
    """Tests the length and fields of `results`."""
    expected_fields = ('eid', 'filename', 'height', 'mimetype', 'ref', 'size', 'type', 'url', 'width')
    assert om_1.results[0]._fields == expected_fields
    assert len(om_1.results) == 355

    assert om_2.results[2]._fields == expected_fields
    assert len(om_2.results) == 18


def test_eid():
    """Tests whether the EID is correct."""
    assert om_1.results[0].eid == '1-s2.0-S0893608024005562-gr3.jpg'
    assert om_2.results[2].eid == '1-s2.0-S2213305418300365-gr2.sml'


def test_filename():
    """Tests whether the filename is correct."""
    assert om_1.results[0].filename == 'gr3.jpg'
    assert om_2.results[2].filename == 'gr2.sml'


def test_height():
    """Tests whether the height is correct."""
    assert om_1.results[0].height == 729
    assert om_2.results[2].height == 146


def test_mimetype():
    """Tests whether the mimetype is correct."""
    assert om_1.results[0].mimetype == 'image/jpeg'
    assert om_2.results[2].mimetype == 'image/gif'


def test_ref():
    """Tests whether the ref is correct."""
    assert om_1.results[0].ref == 'gr3'
    assert om_2.results[2].ref == 'gr2'


def test_size():
    """Tests whether the size is correct."""
    assert om_1.results[0].size == 100202
    assert om_2.results[2].size == 14910


def test_type():
    """Tests whether the type is correct."""
    assert om_1.results[0].type == 'IMAGE-DOWNSAMPLED'
    assert om_2.results[2].type == 'IMAGE-THUMBNAIL'


def test_url():
    """Tests whether the URL is correct."""
    expected_url_0 = 'https://api.elsevier.com/content/object/eid/1-s2.0-S0893608024005562-gr3.jpg?httpAccept=%2A%2F%2A'
    assert om_1.results[0].url == expected_url_0

    expected_url_1 = 'https://api.elsevier.com/content/object/eid/1-s2.0-S2213305418300365-gr2.sml?httpAccept=%2A%2F%2A'
    assert om_2.results[2].url == expected_url_1


def test_width():
    """Tests whether the width is correct."""
    assert om_1.results[0].width == 656
    assert om_2.results[2].width == 219


def test_str():
    """Tests whether the __str__ method works correctly."""
    assert str(om_1) == 'Document with doi 10.1016/j.neunet.2024.106632 contains 355 objects.'
    assert str(om_2) == 'Document with pii S2213305418300365 contains 18 objects.'
