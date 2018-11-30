============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every
little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/scopus-api/scopus/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Respect the `Python Code of Conduct <https://www.python.org/psf/codeofconduct/>`_

Report Bugs
~~~~~~~~~~~

Before are reporting a bug, please

* Upgrade to the newest version if necessary: `pip install scopus --upgrade`
* Make sure your error message is not one of `these <https://scopus.readthedocs.io/en/latest/tips.html#error-messages>`_.

Report bugs at https://github.com/scopus-api/scopus/issues.  Please include:

* Your operating system name and version (after `import scopus` in Python, type `print(scopus.__version__)`.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug"
is open to whoever wants to fix it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement"
is open to whoever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

This repo could always use more documentation, whether as part of the
official scopus docs, in docstrings, or even on the web in blog posts,
articles, and such.

Get Started!
------------

Ready to contribute? Here's how to set up `scopus` for local development.

1. Fork the `scopus` repo on GitHub.
2. Clone your fork locally::

    $ git clone https@github.com:your_name_here/scopus.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv scopus
    $ cd scopus/
    $ python setup.py develop

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1. Adhere to `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_
2. Run nosetests locally `python -m nose --verbose` (on Windows) or `nosetests3 scopus/tests/ --verbose`.
3. The pull request should work for Python 2.7, and 3.5.
