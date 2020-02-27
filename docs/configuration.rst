Configuration
-------------

Since version 1.0, `pybliometrics` uses a config file stored `~/.scopus/config.ini`.  It saves credentials as well as directory names for folders that store cached files.  Folder `~/` refers to your private home directory or home path.  On many Windows machines this is usually `C:/Document and Settings/<Your User Name>`.

By default, after initial set-up (see below), the file will look like this:

.. code-block:: none

    [Directories]
    AbstractRetrieval = YYY/.scopus/abstract_retrieval
    AffiliationSearch = YYY/.scopus/affiliation_search
    AuthorRetrieval = YYY/.scopus/author_retrieval
    AuthorSearch = YYY/.scopus/author_search
    CitationOverview = YYY/.scopus/citation_overview
    ContentAffiliationRetrieval = YYY/.scopus/affiliation_retrieval
    ScopusSearch = YYY/.scopus/scopus_search
    SerialTitle = YYY/.scopus/serial_title

    [Authentication]
    APIKey = XXX


where YYY refers to `~/` and XXX refers to your API Key.

Simply edit this file to change

* ...your API key
* ...the paths where `pybliometrics` should cache downloaded files (`pybliometrics` will create them if necessary)

Set-up
~~~~~~
If the configuration file does not exist, `pybliometrics` will raise a warning.  To generate the configuration file, issue the command

.. code-block:: python

    >>> import pybliometrics
    >>> pybliometrics.scopus.utils.create_config()


`pybliometrics` then prompts you for your credentials.  Most users only need to provide the API Key and hit enter on the second prompt.  If you have to use InstToken authentication, enter it in the second step.  If you need to use a Proxy, please edit the file manually to include a section that looks like so:

.. code-block:: batch

    [Proxy]
    ftp = socks5://127.0.0.1:1234
    http = socks5://127.0.0.1:1234
    https = socks5://127.0.0.1:1234


The presence of this information will make use of the proxy, so be sure to remove the block when you don't want to use a proxy.
