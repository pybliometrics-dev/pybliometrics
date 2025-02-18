pybliometrics.sciencedirect.ObjectRetrieval
==========================================

All components of a Document that are not text (figures, formulas, etc.) are called `objects`.
`ObjectRetrieval()` retrieves objects in a document using the `ScienceDirect Object Retrieval API <https://dev.elsevier.com/documentation/ObjectRetrievalAPI.wadl>`_.

.. currentmodule:: pybliometrics.sciencedirect 
.. contents:: Table of Contents
    :local:

Documentation
-------------

.. autoclass:: ObjectRetrieval
   :members:
   :inherited-members:

Examples
--------

Objects are uniquely identified by the `document id` and the `object filename`. To get the filename of an object you use the `ObjectMetadata` class.
Let's start by retrieving all object's filenames:
        
.. code-block:: python

    >>> from PIL import Image
    >>> from pybliometrics.sciencedirect import init, ObjectMetadata, ObjectRetrieval
    >>> init()
    >>> # Get all objects and its filenames
    >>> om = ObjectMetadata('10.1016/j.rcim.2020.102086')
    >>> all_filenames = [f.filename for f in om.results]
    >>> all_filenames
    ['gr13.jpg', 'gr9.jpg', 'gr12.jpg', ..., 'si98.svg', 'si99.svg', 'am.pdf']


Now let's retrieve the third filname in the list and retrieve the object:

.. code-block:: python

    >>> # Get third object: gr12.jpg
    >>> obj_ret = ObjectRetrieval('10.1016/j.rcim.2020.102086', all_filenames[2])
    >>> # Access object using the 'object' property and display using PIL
    >>> img = Image.open(obj_ret.object)
    >>>> img.show()

.. image:: ./figures/gr12.jpg
    :alt: Example image of gr12.jpg
    :width: 300px
    :align: left
