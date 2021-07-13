API Key quotas and 429 error
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Each API key has a certain usage limit for different Scopus APIs. See https://dev.elsevier.com/api_key_settings.html for the list; for example, a key allows for 5,000 retrieval requests, or 20,000 search requests via the Scopus Search API.

One week after the first usage, Scopus resets the key.

`pybliometrics` will use all the keys provided in the :doc:`configuration file <../configuration>` when one key exceeded its quota for the given API. Be sure to put all keys in the config.ini.

When the last key has been depleted as well, `pybliometrics` throws an a :ref:`pybliometrics.scopus.exception.Scopus429Error <Scopus429Error>`. In this case you need to restart the application one week after it has been started.
