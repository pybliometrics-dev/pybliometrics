============
Installation
============

Install scopus from PyPI:

.. code-block:: console

    $ pip install scopus

or the development version from the GitHub repository (requires git on your system):

.. code-block:: console

    $ pip install git+https://github.com/scopus-api/scopus

To access the Scopus database using `scopus`, get an API key from http://dev.elsevier.com/myapikey.html.  On first usage, `scopus` prompts you for authentication details and stores them in `~/.scopus/config.ini`, where you can change it manually (see :doc:`Configuration </configuration>`).  Additionally, you may need to be in your institution's network or you need to have an InstToken, which can also be saved in the configuration.

See extended description and examples in the :doc:`Examples </examples>` section.
