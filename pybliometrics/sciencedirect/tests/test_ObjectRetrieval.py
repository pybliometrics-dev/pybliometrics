"""Tests for ObjectRetrieval() class."""

import xml.etree.ElementTree as ET

from io import BytesIO
from PIL import Image

from pybliometrics.sciencedirect import init, ObjectRetrieval

init()

or_1 = ObjectRetrieval('S156984322300331X',
                       'gr10.jpg',
                       refresh=30)
or_2 = ObjectRetrieval('10.1016/j.rcim.2020.102086',
                       'si92.svg',
                       id_type='doi',
                       refresh=30)


def test_object():
    """Tests whether the object is a BytesIO object and its content."""
    obj_1_last_50 = b'\xbf\xbd\xb6\xeb;+\\\x87Y7\x94[y\x17\xe3\xeb/(\xcf#\xda\xc9\x90\x80 \x08\x02\x00\x80 \x08\x02\x00\x80 \x08\x02\x00\x80 \x08\x02\x00\x80 \x08\x02\x03\xff\xd9'
    assert isinstance(or_1.object, BytesIO)
    assert or_1.object.getvalue()[-50:] == obj_1_last_50
    with Image.open(or_1.object) as img:
        assert img.format.lower() == 'jpeg'

    obj_2_150_200 = b"085 235.866 8.8237' width='283.039pt' xmlns='http:"
    assert isinstance(or_2.object, BytesIO)
    assert or_2.object.getvalue()[150:200] == obj_2_150_200
    assert ET.parse(or_2.object).getroot().tag == '{http://www.w3.org/2000/svg}svg'
