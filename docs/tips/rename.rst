Migration Guide from scopus to pybliometrics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In June 2019 we renamed the package from scopus to pybliometrics.  This way we comply with naming rules for Elesevier's trademark "Scopus".  At the same time we open the package for further development.

Migration is easy:

1. Install pybliometrics
2. Uninstall scopus
3. In your scripts, simply change the import statement: "from pybliometrics.scopus import ..." instead of "from scopus import ..."

