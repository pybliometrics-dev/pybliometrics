Configuration
-------------

pybliometrics.cfg
~~~~~~~~~~~~~~~~~
`pybliometrics` stores values it needs for operation in a configuration file called `pybliometrics.cfg`.  The config file saves credentials as well as directory names for folders that store downloaded results. `pybliometrics` reads this file on startup.

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


Start-up
~~~~~~~~

You initalize `pybliometrics` like so:

.. code-block:: python

    import pybliometrics
	
	pybliometrics.scopus.init()


This reads the configuration from the default locations.  If you store the configuration file elsewhere, you can provide the path using keyword "config_dir" (str).  You may also pass your own keys using the keyword "keys" (list).


Set-up
~~~~~~
If the configuration file does not exist, `pybliometrics` will prompt you to provide the configuration values the first time you execute `init()`.

There are two consecutive prompts: For your API Key(s) and your InstToken.  The InstToken enables or facilitates access from outside your institution network, and you request it from Elsevier's Integration Support.  If you don't use InstToken, hit enter on the second prompt.  The InstToken, if provided, is added to the Authentication block:

.. code-block:: none

    [Authentication]
    APIKey = XXX
    InstToken = WWW


If you need to use a proxy, please edit the file manually to include a section that looks like so:

.. code-block:: none

    [Proxy]
    http = http://127.0.0.1:1234
    https = https://127.0.0.1:1234


The presence of this information will make use of the proxy.  Be sure to remove or comment out the block when you don't want to use a proxy.

In case you build `pybliometrics` using CI or on a server where prompts aren't possible, you can provide a optional parameters to `create_config()`: "config_dir" (str) for the location of the file, "keys" (list) for the API keys, and "insttoken" (list) for the InstTokens.  Note that this only works to overwrite the existing configuration file.


Default location
~~~~~~~~~~~~~~~~
By default, the configuration file is located at `~/.config/`.  Folder `~/` refers to your private home directory or home path.  On many Windows machines this defaults to `C:/Document and Settings/<Your User Name>`.

If you started with versions older than 3.5, the file was called `config.ini` and located either in `~/.pybliometrics/` or (for very old installations) in `~/.scopus/`. You can safely move and rename the file.  The location `~/.config/pybliometrics.cfg` always takes precedence.

To see the location of the configuration file your current `pybliometrics` instance is using, execute this:

.. code-block:: python

    import pybliometrics

    pybliometrics.scopus.utils.constants.CONFIG_FILE
