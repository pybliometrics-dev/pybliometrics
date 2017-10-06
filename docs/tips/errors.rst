Error messages
~~~~~~~~~~~~~~

Since scopus 0.2.0, an exception is raised when the download status is not ok.  This is to prevent faulty information (i.e. the error status and message) being saved as cached file.

The Scopus API returns a number of errors, upon which the current scopus run interrupts and prints the error to the screen.

Here are common exception classes, status lines and possible causes:

`requests.exceptions.TooManyRedirects: Exceeded 30 redirects.`
    The entity you are looking for was not properly merged with another one entity in the sense that it is not forwarding.  Happens rarely when Scopus Author profiles are merged.  May also occur less often with Abstract EIDs and Affiliation IDs.

`requests.exceptions.HTTPError: 400 Client Error: Bad Request for url`
    Usually an invalid search query, such as a missing parenthesis.  Verify that your query works in `Advanced Search <https://www.scopus.com/search/form.uri?display=advanced>`_.

`requests.exceptions.HTTPError: 401 Client Error: Unauthorized for url`
    Either the provided key is not correct, in which case you should change it in `~/.scopus/my_scopus.py`, or you are outside the network that provides you access to the Scopus database (e.g. your university network).  Remember that you need both to access Scopus.

`requests.exceptions.HTTPError: 404 Client Error: Not Found for url`
    The entity you are looking for does not exist.  Check that your identifier is still pointing to the item you are looking for.

`requests.exceptions.HTTPError: 421 Quota Exceeded`
    Your provided API key's weekly allowance of 5000 requests (for standard views) is depleted.  Wait a week or change the key in `~/.scopus/my_scopus.py`

`requests.exceptions.HTTPError: 500 Server Error: Internal Server Error for url`
    Formally, the server does not respond, for various reasons.  A common reason in searches is that you use a fieldname that does not exist.  Verify that your query works in `Advanced Search <https://www.scopus.com/search/form.uri?display=advanced>`_.
