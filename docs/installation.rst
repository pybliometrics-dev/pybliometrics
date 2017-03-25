============
Installation
============

Install scopus with:

.. code-block:: console

    $ pip install git+git://github.com/scopus-api/scopus

Using Scopus is not free. You need to have a license or institutional access to use it.  Go to http://dev.elsevier.com/myapikey.html to register and get a key.  `scopus` expects this key to be in a variable called `MY_API_KEY` defined in `~/.scopus/my_scopus.py`:

.. code-block:: python
   :caption: ~/.scopus/my_scopus.py
   
    MY_API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
