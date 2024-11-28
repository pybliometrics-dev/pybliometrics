API Key quotas and 429 error
----------------------------

Each API key has a certain usage limit for different Scopus APIs which are reset weekly.  See https://dev.elsevier.com/api_key_settings.html for the list; for example, a key allows for 5,000 retrieval requests, or 20,000 search requests via the Scopus Search API.

The usage limits for each key are reset weekly, one week after their first usage.  To this end, each class has two methods that can help you: `.get_key_remaining_quota()` tells you how many calls you have left with the current key for the last used API.  `.get_key_reset_time()` tells you the time until reset.

`pybliometrics` will use all the keys provided in the :doc:`configuration file <../configuration>` when one key exceeded its quota for the given API. Be sure to put all keys in the config.ini.

When the last key has been depleted as well, `pybliometrics` throws a :ref:`pybliometrics.scopus.exception.Scopus429Error <Scopus429Error>`. In this case you need to restart the application one week after it has been started.
