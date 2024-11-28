Migration Guide from 3.x to 4.x
-------------------------------

Upgrading from `pybliometrics` 3.x to 4.x requires a minor adjustment in your code due to changes in how the library handles configuration files. Many users requested more flexibility in configuration storage. To address this, version 4.0 introduces a new initialization function.

Users now simply initialize `pybliometrics`:

.. code-block:: python

    >>> import pybliometrics
    >>> pybliometrics.scopus.init()

The `init()` function offers two functionalities:

1. Specify the location of the :doc:`Configuration <../configuration>` file using the "config_dir" parameter. The default location remains the `.config` folder in your home directory. Previously, users had to rely on `os.environ` to set the path if the configuration file resided elsewhere (e.g., project folder). This is no longer necessary.
2. Provide a list of API keys using the "keys" keyword.
