These testfiles are designed to test features of the various classes. The simplest way to invoke the tests is to execute

    pytest --verbose

in the command line from within the pybliometrics repo.  By passing a specific filename, you can test only one suite:

    pytest pybliometrics/sciencedirect/tests/test_ArticleRetrieval.py --verbose

Windows users should try `python -m` in front of above commands.

During the tests, files from the Scopus database are downloaded and cached in the usual way.  Hence, tests make use of your API Key and require a valid connection.
