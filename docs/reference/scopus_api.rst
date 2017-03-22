ScopusAbstract
==============

This module implements the http://dev.elsevier.com/retrieval.html API.  The main entry point is the ScopusAbstract class, which takes a `Scopus EID <http://kitchingroup.cheme.cmu.edu/blog/2015/06/07/Getting-a-Scopus-EID-from-a-DOI/>`_ and an optional refresh boolean value.  Retrieving these results is not fast, so we cache them to speed up subsequent uses of the code.  Sometimes you may want new results, e.g. to get citation counts, and then you set `refresh=True`.

.. code-block:: python
   
    from scopus.scopus_api import ScopusAbstract


Reference
---------

.. automodule:: scopus.scopus_api
    :members:
    :undoc-members:
    :show-inheritance: