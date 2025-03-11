pybliometrics.sciencedirect.ObjectMetadata
==========================================

All components of a document that are not text (figures, formulas, etc.) are called `objects`.
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

    >>> import pandas as pd
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

The `results` can be casted to a pandas DataFrame:

.. code-block:: python

    >>> df = pd.DataFrame(om.results)
    >>> # Print retrieved fields
    >>> df.columns
    Index(['eid', 'filename', 'height', 'mimetype', 'ref', 'size', 'type', 'url',
       'width'], dtype='object')
    >>> # Get shape of the dataframe (rows x columns)
    >>> df.shape
    (355, 9)
    >>> # Print the first 5 rows
    >>> df.head()


.. raw:: html

    <div style="overflow-x:auto; border:1px solid #ddd; padding:10px;">
    <style scoped>
        .dataframe tbody tr th:only-of-type {
            vertical-align: middle;
        }

        .dataframe tbody tr th {
            vertical-align: top;
        }

        .dataframe thead th {
            text-align: right;
        }
        .dataframe{
            font-size: 12px;
        }
    </style>
    <table border="1" class="dataframe">
    <thead>
        <tr style="text-align: right;">
        <th></th>
        <th>eid</th>
        <th>filename</th>
        <th>height</th>
        <th>mimetype</th>
        <th>ref</th>
        <th>size</th>
        <th>type</th>
        <th>url</th>
        <th>width</th>
        </tr>
    </thead>
    <tbody>
        <tr>
        <th>0</th>
        <td>1-s2.0-S0893608024005562-gr3.jpg</td>
        <td>gr3.jpg</td>
        <td>729.0</td>
        <td>image/jpeg</td>
        <td>gr3</td>
        <td>100202</td>
        <td>IMAGE-DOWNSAMPLED</td>
        <td>https://api.elsevier.com/content/object/eid/1-...</td>
        <td>656.0</td>
        </tr>
        <tr>
        <th>1</th>
        <td>1-s2.0-S0893608024005562-gr5.jpg</td>
        <td>gr5.jpg</td>
        <td>256.0</td>
        <td>image/jpeg</td>
        <td>gr5</td>
        <td>44240</td>
        <td>IMAGE-DOWNSAMPLED</td>
        <td>https://api.elsevier.com/content/object/eid/1-...</td>
        <td>623.0</td>
        </tr>
        <tr>
        <th>2</th>
        <td>1-s2.0-S0893608024005562-gr4.jpg</td>
        <td>gr4.jpg</td>
        <td>246.0</td>
        <td>image/jpeg</td>
        <td>gr4</td>
        <td>51563</td>
        <td>IMAGE-DOWNSAMPLED</td>
        <td>https://api.elsevier.com/content/object/eid/1-...</td>
        <td>376.0</td>
        </tr>
        <tr>
        <th>3</th>
        <td>1-s2.0-S0893608024005562-gr6.jpg</td>
        <td>gr6.jpg</td>
        <td>246.0</td>
        <td>image/jpeg</td>
        <td>gr6</td>
        <td>53955</td>
        <td>IMAGE-DOWNSAMPLED</td>
        <td>https://api.elsevier.com/content/object/eid/1-...</td>
        <td>376.0</td>
        </tr>
        <tr>
        <th>4</th>
        <td>1-s2.0-S0893608024005562-gr2.jpg</td>
        <td>gr2.jpg</td>
        <td>729.0</td>
        <td>image/jpeg</td>
        <td>gr2</td>
        <td>98000</td>
        <td>IMAGE-DOWNSAMPLED</td>
        <td>https://api.elsevier.com/content/object/eid/1-...</td>
        <td>656.0</td>
        </tr>
    </tbody>
    </table>
    </div>