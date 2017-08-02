These testfiles are designed to test features of the various classes.  To run these tests, you need the [nosetesting package](http://nose.readthedocs.io/en/latest/).

The simplest way to invoke the tests is run

    nosetests scopus/tests/ --verbose

in the commandline from within the scopus repo.

During the tests, files from the Scopus database are downloaded and cached the usual way. Hence, tests make use of your API Key and require a valid connection.
