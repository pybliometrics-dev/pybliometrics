This class provides a function to generate a report on a `ScopusSearch <../reference/scopus.ScopusSearch>`_ object.  It outputs text in org-format.

.. code-block:: python
   
    >>> from scopus import report, ScopusSearch
    >>> s = ScopusSearch('FIRSTAUTH ( kitchin  j.r. )')


It summarizes the results in a variety of ways, such as the number of hits, which journals they are published in, who the coauthors are, how many times the articles have been published, and more.
