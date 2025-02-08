=============
Configuration
=============

pybliometrics.cfg
-----------------
`pybliometrics` stores values it needs for operation in a configuration file called `pybliometrics.cfg`.  The config file saves credentials as well as directory names for folders that store downloaded results. `pybliometrics` reads this file on startup.

The structure of the file is the following:

.. code-block:: none

    [Directories]
    AbstractRetrieval = PPP/.cache/pybliometrics/Scopus/abstract_retrieval
    AffiliationRetrieval = PPP/.cache/.pybliometrics/Scopus/affiliation_retrieval
    AffiliationSearch = PPP/.cache/.pybliometrics/Scopus/affiliation_search
    AuthorRetrieval = PPP/.cache/.pybliometrics/Scopus/author_retrieval
    AuthorSearch = PPP/.cache/.pybliometrics/Scopus/author_search
    CitationOverview = PPP/.cache/.pybliometrics/Scopus/citation_overview
    ScopusSearch = PPP/.cache/.pybliometrics/Scopus/scopus_search
    SerialSearch = PPP/.cache/.pybliometrics/Scopus/serial_search
    SerialTitle = PPP/.cache/.pybliometrics/Scopus/serial_title
    PlumXMetrics = PPP/.cache/.pybliometrics/Scopus/plumx
    SubjectClassifications = PPP/.cache/.pybliometrics/Scopus/subject_classification

    [Authentication]
    APIKey = Key1, Key2, Key3
    InstToken = Token for Key1, Token for Key2, Token for Key3
    
    [Proxy]
    http = http://127.0.0.1:1234
    https = https://127.0.0.1:1234

    [Requests]
    Timeout = 20
    Retries = 5


Section `[Directories]` contains the paths where `pybliometrics` should store (cache) downloaded files.  `pybliometrics` will create them if necessary.  "PPP" is the extended version of `~/`, your private home directory or home path.  The default paths are entered automatically.  To set different paths, edit the config file manually.  Under `pybliometrics` 2.x and before, the default paths used to be `~/.pybliometrics/abstract_retrieval` or `~/.scopus/abstract_retrieval`.  You can safely rename and move the cache folder, but remember to change the paths in the configuration file, too.

Section `[Authentication]` contains the API keys which you obtain from http://dev.elsevier.com/myapikey.html.  If you provide multiple (separated by a comma), `pybliometrics` automatically replaces a depleted key with another one at random at runtime until all of them are depleted.  Remember that you can register multiple keys for the same email address, and you may use multiple email addresses which do not need to be associated to the institution through which you access Scopus.  Some users need InstToken, which allow for access outside a specific network.  They are tied to one particular API keys of yours, and must be passed in the same order.  Most users do not use InstTokens though.

Section `[Proxy]` will be used when it exists; therefore remember to remove or comment out when you do not need it.

Section `[Requests]` stores parameters passed on to `requests` (see their `advanced documentation<https://requests.readthedocs.io/en/latest/user/advanced/>_`).

Simply edit this file using a simple text editor; changes will take effect the next time you start pybliometrics.  Remember to indent multi-line statements.


Start-up
--------

You initalize `pybliometrics` like so:

.. code-block:: python

    >>> import pybliometrics
	
    >>> pybliometrics.init()


This attempts to read the configuration from the default locations.

If the configuration file does not exist, `pybliometrics` will prompt you to provide the configuration values the first time you execute `init()`.

There are two consecutive prompts: For your API Key(s) and the corresponding InstToken(s).  The InstToken enables or facilitates access from outside your institution network, and you request it from Elsevier's Integration Support.  If you don't use InstToken, hit enter on the second prompt:

.. code-block:: none

    Creating config file at C:\Users\rosm\.config\pybliometrics.cfg with default paths...
    Please enter your API Key(s), obtained from http://dev.elsevier.com/myapikey.html.  Separate multiple keys by comma:
    xxx
    API Keys are sufficient for most users.  If you have an InstToken, please enter the tokens pair now. Separate multiple tokens by a comma. The correspondig key's position should match the position of the token.If you don't have tokens, just press Enter:
    yyy

The :ref:`function <doc-init>` accepts three parameters: A custom location `config_path` (str or `pathlib.Path() <https://docs.python.org/3/library/pathlib.html>`_, a list of `keys`, and a list of `inst_tokens`.  The order of the provided InstTokens must match that of the provided API Keys.  This is relevant for users who build `pybliometrics` using CI or who work on a server where prompts aren't possible.


Default location
----------------
By default, the configuration file is located at `~/.config/`.  `~/` refers to your private home directory or home path.  On many Windows machines this defaults to `C:/Document and Settings/<Your User Name>`.

To see the location of the configuration file your current `pybliometrics` instance is using, execute this:

.. code-block:: python

    >>> import pybliometrics

    >>> print(pybliometrics.utils.constants.CONFIG_FILE)

If you started with versions older than 3.5, the file was called `config.ini` and located either in `~/.pybliometrics/` or (for very old installations) in `~/.scopus/`. You can safely move and rename the file.  Those locations always take precedence.
