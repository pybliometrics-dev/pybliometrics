Download Machine
~~~~~~~~~~~~~~~~
Often one is interested in downloading (and caching) many more items than one key allows.  Either users would have to wait a week until the key resets or change the key in the :doc:`configuration file <../configuration/>`.

However, it is also possible to programmatically change the API key that pybliometrics should use once a :ref:`Scopus429Error <Scopus429Error>` occurs:

.. code-block:: python
   
    >>> from pybliometrics.scopus import config, AuthorRetrieval
    >>> from pybliometrics.scopus.exception import Scopus429Error
    >>>
    >>> _keys = ["key1", "key2", "key3"]
    >>> error = True
    >>> while error:
    >>>     try:
    >>>         au = AuthorRetrieval("54885755900", refresh=True)
    >>>         error = False
    >>>     except Scopus429Error:
    >>>         # Remove the last item in _keys to assign it as new API key
    >>>         config["Authentication"]["APIKey"] = _keys.pop()
    >>> # continue with normal code

Of course, any other class instead of AuthorRetrieval will work as well.
