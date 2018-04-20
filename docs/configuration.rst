Configuration
-------------

Version 0.6 introduced a config file in in `~/.scopus/`.  This config file will gradually be extended to steer `scopus` to a greater extend but is currently only used for one purpose:  To store credentials for the `token-based authentication <https://dev.elsevier.com/tecdoc_api_authentication.html>`_.  If you want to stick to the more common IP address based authentication, do not create the config file.

If you have an InstToken and an API Key, please create a file `~/.scopus/config`.  Edit it to look like follows:

.. code-block:: none

    [Authentication]
    InstToken = <Your InstToken goes here>
    APIKey = <Your API Key goes here>

Folder `~/` refers to your private home directory or home path.  On many Windows machines this is usually `C:\Document and Settings\<Your User Name>`.  In there you find a hidden folder `.scopus`, which is also the directory where `scopus` caches downloaded files.
