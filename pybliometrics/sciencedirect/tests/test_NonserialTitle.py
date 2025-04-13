"""Test NonserialTitle()."""

from pybliometrics.sciencedirect import NonserialTitle, init

init()

nst_1 = NonserialTitle('978-0-12-823751-9', view='STANDARD', refresh=30)
nst_2 = NonserialTitle(9780128203101, view='STANDARD', refresh=30)
nst_3 = NonserialTitle('978-0-12-821777-1', view='STANDARD', refresh=30)

def test_aggregation_type():
    assert nst_1.aggregation_type == "ebook"
    assert nst_2.aggregation_type == "ebook"
    assert nst_3.aggregation_type == "ebook"


def test_authors():
    assert nst_1.authors == "Ian Newton"
    assert nst_2.authors is None
    assert nst_3.authors is None


def test_description():
    assert nst_1.description is None
    assert nst_2.description is None
    assert nst_3.description is None


def test_edition():
    assert nst_1.edition == "Second Edition"
    assert nst_2.edition is None
    assert nst_3.edition is None


def test_editors():
    assert nst_1.editors is None
    assert nst_2.editors == "Elias Barriga and Ivana Pajic-Lijakovic"
    assert nst_3.editors == "Fatos Xhafa, Mohamed A. Tawhid, Pardeep Kumar and Yugal Kumar"


def test_isbn():
    assert nst_1.isbn == "9780128237519"
    assert nst_2.isbn == "9780128203101"
    assert nst_3.isbn == "9780128217771"


def test_link_coverimage():
    assert nst_1.link_coverimage == "https://api.elsevier.com/content/nonserial/title/isbn/9780128237519?view=coverimage"
    assert nst_2.link_coverimage == "https://api.elsevier.com/content/nonserial/title/isbn/9780128203101?view=coverimage"
    assert nst_3.link_coverimage == "https://api.elsevier.com/content/nonserial/title/isbn/9780128217771?view=coverimage"


def test_link_homepage():
    assert nst_1.link_homepage == "https://www.sciencedirect.com/science/book/9780128237519"
    assert nst_2.link_homepage == "https://www.sciencedirect.com/science/book/9780128203101"
    assert nst_3.link_homepage == "https://www.sciencedirect.com/science/book/9780128217771"


def test_link_search():
    assert nst_1.link_search == "https://api.elsevier.com/content/nonserial/title/isbn/9780128237519"
    assert nst_2.link_search == "https://api.elsevier.com/content/nonserial/title/isbn/9780128203101"
    assert nst_3.link_search == "https://api.elsevier.com/content/nonserial/title/isbn/9780128217771"


def test_publisher_id():
    assert nst_1.publisher_id == "350"
    assert nst_2.publisher_id == "350"
    assert nst_3.publisher_id == "350"


def test_publisher_name():
    assert nst_1.publisher_name == "Academic Press"
    assert nst_2.publisher_name == "Academic Press"
    assert nst_3.publisher_name == "Academic Press"


def test_self_link():
    assert nst_1.self_link == "https://api.elsevier.com/content/nonserial/title/isbn/9780128237519"
    assert nst_2.self_link == "https://api.elsevier.com/content/nonserial/title/isbn/9780128203101"
    assert nst_3.self_link == "https://api.elsevier.com/content/nonserial/title/isbn/9780128217771"


def test_title():
    assert nst_1.title == "The Migration Ecology of Birds"
    assert nst_2.title == "Viscoelasticity and  Collective Cell Migration"
    assert nst_3.title == "Machine Learning, Big Data, and IoT for Medical Informatics"
