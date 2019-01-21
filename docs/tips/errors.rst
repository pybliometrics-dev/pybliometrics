Error messages
~~~~~~~~~~~~~~

Since scopus 0.2.0, an exception is raised when the download status is not ok.  This is to prevent faulty information (i.e. the error status and message) being saved as cached file.  With scopus 1.3.0 these exceptions are of base class ScopusException.

The following exceptions are defined:

`scopus.exception.ScopusQueryError`
    When a search query returns more results than specified or allowed (Scoups allows 5000 results maximum).  Change the query such that less than or equal to 5000 results are returned.

`scopus.exception.Scopus400Error: BAD REQUEST`
    Usually an invalid search query, such as a missing parenthesis.  Verify that your query works in `Advanced Search <https://www.scopus.com/search/form.uri?display=advanced>`_.

`scopus.exception.Scopus401Error: UNAUTHORIZED`
    Either the provided key is not correct, in which case you should change it in `~/.scopus/my_scopus.py`, or you are outside the network that provides you access to the Scopus database (e.g. your university network).  Remember that you need both to access Scopus.

`scopus.exception.Scopus404Error: NOT FOUND`
    The entity you are looking for does not exist.  Check that your identifier is still pointing to the item you are looking for.

`scopus.exception.Scopus429Error: QUOTA EXCEEDED`
    Your provided API key's weekly allowance of 5000 requests (for standard views) is depleted.  Wait a week or change the key in `~/.scopus/my_scopus.py`

`scopus.exception.Scopus500Error: INTERNAL SERVER ERROR`
    Formally, the server does not respond, for various reasons.  A common reason in searches is that you use a fieldname that does not exist.  Verify that your query works in `Advanced Search <https://www.scopus.com/search/form.uri?display=advanced>`_.

If queries break for other reasons, exceptions of type `requests.exceptions <http://docs.python-requests.org/en/master/api/#requests.RequestException>`_ are raised, such as:

`requests.exceptions.TooManyRedirects: Exceeded 30 redirects.`
    The entity you are looking for was not properly merged with another one entity in the sense that it is not forwarding.  Happens rarely when Scopus Author profiles are merged.  May also occur less often with Abstract EIDs and Affiliation IDs.
