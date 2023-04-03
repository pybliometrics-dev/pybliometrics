Configuration
-------------

pybliometrics.cfg
~~~~~~~~~~~~~~~~~
`pybliometrics` stores values it needs for operation in a configuration file called `pybliometrics.cfg`.  The config file saves credentials as well as directory names for folders that store downloaded results.

By default, after initial set-up (see below), the file will look like this:

.. code-block:: none

    [Directories]
    AbstractRetrieval = PPP/.pybliometrics/Scopus/abstract_retrieval
    AffiliationSearch = PPP/.pybliometrics/Scopus/affiliation_search
    AuthorRetrieval = PPP/.pybliometrics/Scopus/author_retrieval
    AuthorSearch = PPP/.pybliometrics/Scopus/author_search
    CitationOverview = PPP/.pybliometrics/Scopus/citation_overview
    AffiliationRetrieval = PPP/.pybliometrics/Scopus/affiliation_retrieval
    ScopusSearch = PPP/.pybliometrics/Scopus/scopus_search
    SerialTitle = PPP/.pybliometrics/Scopus/serial_title

    [Authentication]
    APIKey = XXX,
        YYYY,
        ZZZ

    [Requests]
    Timeout = 20
    Retries = 5


Section `[Directories]` contains the paths where `pybliometrics` should store (cache) downloaded files.  `pybliometrics` will create them if necessary.

Section `[Authentication]` contains the API Keys which you obtain from http://dev.elsevier.com/myapikey.html.  If you provide multiple (separated by a comma), `pybliometrics` automatically replaces a depleted key with another one at random at runtime until all of them are depleted.

Simply edit this file using a simple text editor; changes will take effect the next time you start pybliometrics.  Remember to indent multi-line statements.

Under `pybliometrics` 2.x and before, the default paths used to be `PPP/.scopus/abstract_retrieval`.  You can safely rename the cache folder `.scopus` to `.pybliometrics` (on Windows machines, rename to `.pybliometrics.`), but remember to change the paths in the configuration file, too.


Set-up
~~~~~~
If the configuration file does not exist, `pybliometrics` will prompt you to provide the configuration values on first import.

There are two consecutive prompts: For your API Key(s) and your InstToken.  The InstToken enables or facilitates access from outside your institution network, and you request it from Elsevier's Integration Support.  If you don't use InstToken, hit enter on the second prompt.  The InstToken, if provided, is added to the Authentication block:

.. code-block:: none

    [Authentication]
    APIKey = XXX, YYY, ZZZ
    InstToken = WWW


If you need to use a proxy, please edit the file manually to include a section that looks like so:

.. code-block:: none

    [Proxy]
    ftp = socks5://127.0.0.1:1234
    http = socks5://127.0.0.1:1234
    https = socks5://127.0.0.1:1234


The presence of this information will make use of the proxy.  Be sure to remove or comment out the block when you don't want to use a proxy.

In case you build `pybliometrics` using CI or on a server where prompts aren't possible, you can provide a single optional parameter to `create_config()`.  The parameter must be a list of keys.  When this parameter is used, there will be no prompts.  Note that this only works to overwrite the existing configuration file.


Runtime
~~~~~~~

You can easily inspect configuration values at runtime, and even set some during execution.  Simply import the config beforehand and assign new values to the keys as if the config was a dictionary:

.. code-block:: python

    from pybliometrics.scopus.utils import config

    print(config['Authentication']['APIKey'])  # Show keys
    config['Proxy']['ftp'] = 'socks5://localhost:8080'  # Redefine proxy

Setting the keys at runtime is however not possible.


Default location
~~~~~~~~~~~~~~~~
For recent and new installations, the configuration file is located at `~/.config/`.  Folder `~/` refers to your private home directory or home path.  On many Windows machines this defaults to `C:/Document and Settings/<Your User Name>`.

If you started with versions older than 3.5, the file was called `config.ini` and located either in `~/.pybliometrics/` or (for very old installations) in `~/.scopus/`. You can safely move and rename the file.  The location `~/.config/pybliometics.cfg` always takes precedence.

To see the location of the configuration file your current `pybliometrics` instance is using, execute this:

.. code-block:: python

    import pybliometrics

    pybliometrics.scopus.utils.constants.CONFIG_FILE


Custom location
~~~~~~~~~~~~~~~

If you prefer to have the configuration file somewhere else, you can tell `pybliometrics` where to look for it.  You will need the `environment facility <https://docs.python.org/3/library/os.html#file-names-command-line-arguments-and-environment-variables>`_ of the base package `os`.  For this to take effect you need to set the environ *before* importing pybliometrics.  `pybliometrics` uses the "PYB_CONFIG_FILE" keyword:

.. code-block:: python

    import os

    os.environ['PYB_CONFIG_FILE'] = "C:/Custom/Location/pybliometrics.cfg"

    import pybliometrics