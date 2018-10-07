Configuration
-------------

Since version 1.0 `scopus` uses a config file in folder `~/.scopus/` to save credentials as well as directory names for folder that store cached files.  You can always change those values, e.g. when you want to cache files on a shared drive.

If the file does not exist, `scopus` will raise a warning.  To generate the configuration file, issue the command

.. code-block:: python

    >>> scopus.utils.create_config()


after import.  `scopus` the prompts you for your credentials.  Most users only need to provide the API Key and hit enter on the second prompt.  If you have to use InstToken authentication, enter it in the second step.

Folder `~/` refers to your private home directory or home path.  On many Windows machines this is usually `C:\Document and Settings\<Your User Name>`.  In there you find a hidden folder `.scopus`, which is also the directory where `scopus` caches downloaded files.
