These testfiles are designed to test features of the various classes.  To run these tests, you need the [nosetesting package](http://nose.readthedocs.io/en/latest/).

The simplest way to invoke the tests is to execute

    nosetests3 --verbose

in the command line from within the scopus repo.  By passing a specific filename, you can test only one suite:

    nosetests3 scopus/tests/test_ContentAffiliationRetrieval.py --verbose

Windows users should try `python -m` is nosetests3 fail.

During the tests, files from the Scopus database are downloaded and cached in the usual way.  Hence, tests make use of your API Key and require a valid connection.
