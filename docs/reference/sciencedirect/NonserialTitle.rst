pybliometrics.sciencedirect.NonserialTitle
==========================================

`NonserialTitle()` implements the `ScienceDirect Nonserial Title API <https://dev.elsevier.com/documentation/NonSerialTitleAPI.wadl>`_.  
It provides metadata for non-serial publications (books) registered in ScienceDirect, including publisher details, identifiers, and links.

.. currentmodule:: pybliometrics.sciencedirect
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: NonserialTitle
    :members:
    :inherited-members:

Examples
--------

You initialize the class with an ISBN (with or without hyphens):

.. code-block:: python

    >>> from pybliometrics.sciencedirect import NonserialTitle, init
    >>> init()
    >>> book = NonserialTitle("978-0-12-823751-9")

You can obtain basic information just by accessing the properties:

.. code-block:: python

    >>> book.title
    'The Migration Ecology of Birds'
    >>> book.publisher_name
    'Academic Press'
    >>> book.isbn
    '9780128237519'
    >>> book.aggregation_type
    'ebook'
    >>> book.authors
    'Ian Newton'
    >>> book.edition
    'Second Edition'
    >>> book.self_link
    'https://api.elsevier.com/content/nonserial/title/isbn/9780128237519'
    >>> book.link_homepage
    'https://www.sciencedirect.com/science/book/9780128237519'
    >>> book.link_coverimage
    'https://api.elsevier.com/content/nonserial/title/isbn/9780128237519?view=coverimage'


Downloaded results are cached to expedite subsequent analyses.  This information may become outdated.  To refresh the cached results if they exist, set `refresh=True`, or provide an integer that will be interpreted as maximum allowed number of days since the last modification date.  For example, if you want to refresh all cached results older than 100 days, set `refresh=100`.  Use `ab.get_cache_file_mdate()` to obtain the date of last modification, and `ab.get_cache_file_age()` to determine the number of days since the last modification.
