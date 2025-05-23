============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

Submit Feedback
---------------

The best way to send feedback is to file an issue at https://github.com/pybliometrics-dev/pybliometrics/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Respect the `Python Code of Conduct <https://www.python.org/psf/codeofconduct/>`_

Report Bugs
-----------

Before are reporting a bug, please

* Upgrade to the newest version if necessary: `pip install pybliometrics --upgrade`
* Make sure your error message is not one of `these <https://pybliometrics.readthedocs.io/en/latest/tips.html#error-messages>`_.

Report bugs at https://github.com/pybliometrics-dev/pybliometrics/issues.  Please include:

* Your operating system name and version (after `import pybliometrics` in Python, type `print(pybliometrics.__version__)`.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.
* If you have a mere question on how to do things, please rather pose your question on `StackOverflow.com <https://stackoverflow.com/>`_ using the `#pybliometrics <https://stackoverflow.com/questions/tagged/pybliometrics>`_ tag.

Fix bugs and implement features
-------------------------------

If you found a bug and know how to fix it: Why not suggest a pull request right away? We commit to review it soon.

Here's how to set up `pybliometrics` for local development:

1. Fork the `pybliometrics` repo on GitHub.
2. Clone your fork locally::

    $ git clone https://github.com/your_username_here/pybliometrics.git

3. Install your local copy into a virtualenv. Assuming you have virtualenvwrapper installed, this is how you set up your fork for local development::

    $ mkvirtualenv pybliometrics
    $ cd pybliometrics/
    $ pip install -e .

4. Create a branch for local development::

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. Commit your changes and push your branch to GitHub::

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

6. Submit a pull request through the GitHub website.

Before you submit a pull request, check that it meets these guidelines:

1. Adhere to `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_.
2. Run tests locally `python -m pytest --verbose` (on Windows) or `pytest pybliometrics/scopus/tests/ --verbose`.
3. The pull request should work for all currently active python versions.
