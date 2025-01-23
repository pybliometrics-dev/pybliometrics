"""Tests for ObjectMetadata"""
from collections import namedtuple

from pybliometrics.sciencedirect import init, ObjectMetadata

init()

om_1 = ObjectMetadata('10.1016/j.neunet.2024.106632', refresh=30)
om_2 = ObjectMetadata('S2213305418300365', id_type='pii', refresh=30)


def test_len():
    """Tests whether the number of results is correct."""
    assert len(om_1.results) == 355
    assert len(om_2.results) == 18


def test_results():
    """Tests whether the results are correct."""
    fields = 'eid filename height mimetype ref size type url width'
    metadata = namedtuple('Metadata', fields)
    expected_metadata_0 = metadata(
        eid="1-s2.0-S0893608024005562-gr3.jpg",
        filename="gr3.jpg",
        height="729",
        mimetype="image/jpeg",
        ref="gr3",
        size="100202",
        type="IMAGE-DOWNSAMPLED",
        url="https://api.elsevier.com/content/object/eid/1-s2.0-S0893608024005562-gr3.jpg?httpAccept=%2A%2F%2A",
        width="656",
    )
    assert om_1.results[0] == expected_metadata_0


def test_str():
    """Tests whether the __str__ method works correctly."""
    assert str(om_1) == 'Document with doi 10.1016/j.neunet.2024.106632 contains 355 objects.'
    assert str(om_2) == 'Document with pii S2213305418300365 contains 18 objects.'
