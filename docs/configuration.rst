Configuration
-------------

config.ini
~~~~~~~~~~
`pybliometrics` stores values it needs for operation in a config file `~/.scopus/config.ini`.  It saves credentials as well as directory names for folders that store cached files.  Folder `~/` refers to your private home directory or home path.  On many Windows machines this defaults to `C:/Document and Settings/<Your User Name>`.

By default, after initial set-up (see below), the file will look like this:

.. code-block:: none

    [Directories]
    AbstractRetrieval = PPP/.scopus/abstract_retrieval
    AffiliationSearch = PPP/.scopus/affiliation_search
    AuthorRetrieval = PPP/.scopus/author_retrieval
    AuthorSearch = PPP/.scopus/author_search
    CitationOverview = PPP/.scopus/citation_overview
    ContentAffiliationRetrieval = PPP/.scopus/affiliation_retrieval
    ScopusSearch = PPP/.scopus/scopus_search
    SerialTitle = PPP/.scopus/serial_title

    [Authentication]
    APIKey = XXX, YYYY,
        ZZZ


where PPP refers to `~/` and XXX, YYYY and ZZZ refer to your API Keys, of which you can register 10 for your Scopus account.  If you provide all of them (separated by a comma), pybliometrics automatically replaces a depleted key with a random one of the others.  If you edit the file manually, remember to indent multi-line statements.

Simply edit this file to change the paths where `pybliometrics` should cache downloaded files (`pybliometrics` will create them if necessary)

Set-up
~~~~~~
If the configuration file does not exist, `pybliometrics` will prompt you to provide the configuration values.  To enforce the process yourself, issue the command

.. code-block:: python

    >>> import pybliometrics
    >>> pybliometrics.scopus.utils.create_config()


There are two prompts: For your API Key(s) and your InstToken.  The InstToken enables or facilitates access from outside your institution network, and you request it from Elsevier's Integration Support.  If you don't use InstToken, hit enter on the second prompt.  The InstToken, if provided, is added to the Authentication block:

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


The presence of this information will make use of the proxy.  Be sure to remove the block when you don't want to use a proxy.


Runtime
~~~~~~~

You can easily inspect or change configuration values at runtime.  Simply import the config beforehand and assign new values to the keys as if the config was a dictionary:

.. code-block:: python

    from pybliometrics.scopus.utils import config
    
    print(config['Authentication']['APIKey'])
    config['Proxy']['ftp'] = 'socks5://localhost:8080'


Custom location
~~~~~~~~~~~~~~~

If you prefer to have the configuration file somewhere else, you can `pybliometrics` tell where to look for it.  You will need the `environment facility <https://docs.python.org/3/library/os.html#file-names-command-line-arguments-and-environment-variables>`_ of the base package `os`.  For this to take effect you need to set the environ *before* importing pybliometrics.  `pybliometrics` uses the "PYB_CONFIG_FILE" keyword:

.. code-block:: python

    import os

    os.environ['PYB_CONFIG_FILE'] = "C:/Custom/Location/config.ini"

    import pybliometrics
