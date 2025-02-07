pybliometrics.sciencedirect.ObjectMetadata
==========================================

All components of a Document that are not text (figures, formulas, etc.) are called `objects`.
`ObjectMetadata()` retrieves the metadata associated with all objects in a document.
Specifically, it retrieves the metadata from the `ScienceDirect Object Retrieval API <https://dev.elsevier.com/documentation/ObjectRetrievalAPI.wadl>`_.

.. currentmodule:: pybliometrics.sciencedirect 
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: ObjectMetadata
   :members:
   :inherited-members:

Examples
--------

To use the class provide a valid identifier:

.. code-block:: python

    >>> from pybliometrics.sciencedirect import ObjectMetadata, init
    >>> init()
    >>> om = ObjectMetadata('10.1016/j.neunet.2024.106632')

The `results` property contains a list of the metadata of the objects found. The available fields and a description can be found in the `Object Retrieval Views <https://dev.elsevier.com/sd_object_retrieval_views.html>`_:

.. code-block:: python

    >>> om.results
    [Metadata(eid='1-s2.0-S0893608024005562-gr3.jpg', filename='gr3.jpg', height=729, mimetype='image/jpeg', ref='gr3', size=100202, type='IMAGE-DOWNSAMPLED', url='https://api.elsevier.com/content/object/eid/1-s2.0-S0893608024005562-gr3.jpg?httpAccept=%2A%2F%2A', width=656),
     Metadata(eid='1-s2.0-S0893608024005562-gr5.jpg', filename='gr5.jpg', height=256, mimetype='image/jpeg', ref='gr5', size=44240, type='IMAGE-DOWNSAMPLED', url='https://api.elsevier.com/content/object/eid/1-s2.0-S0893608024005562-gr5.jpg?httpAccept=%2A%2F%2A', width=623),
     Metadata(eid='1-s2.0-S0893608024005562-gr4.jpg', filename='gr4.jpg', height=246, mimetype='image/jpeg', ref='gr4', size=51563, type='IMAGE-DOWNSAMPLED', url='https://api.elsevier.com/content/object/eid/1-s2.0-S0893608024005562-gr4.jpg?httpAccept=%2A%2F%2A', width=376),
     ...]

Note that each object is uniquely identified by its EID, which is a concatenation of the document's EID and the object's filename.