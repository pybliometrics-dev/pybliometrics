Error message hierarchy
~~~~~~~~~~~~~~~~~~~~~~~

`pybliometrics` raises exceptions if the download status is not ok.  To allow for error-specific handling, `pybliometrics` employs the following exception hierarchy:

* `pybliometrics.scopus.exception.ScopusException`: Base class for the following exceptions.

   * `pybliometrics.scopus.exception.ScopusQueryError`: When a search query returns more results than specified or allowed (Scopus allows 5000 results maximum).  Change the query such that less than or equal to 5000 results are returned.

   * `pybliometrics.scopus.exception.ScopusHtmlError`: Base class for the following exceptions raised through the `requests` package.

      * `pybliometrics.scopus.exception.Scopus400Error: BAD REQUEST`: Usually an invalid search query, such as a missing parenthesis.  Verify that your query works in `Advanced Search <https://www.scopus.com/search/form.uri?display=advanced>`_.

      * `pybliometrics.scopus.exception.Scopus401Error: UNAUTHORIZED`: Either the provided key is not correct, in which case you should change it in your :doc:`configuration file <../configuration>`, or you are outside the network that provides you access to the Scopus database (e.g. your university network).  Remember that you need both to access Scopus.

      * `pybliometrics.scopus.exception.Scopus404Error: NOT FOUND`: The entity you are looking for does not exist.  Check that your identifier is still pointing to the item you are looking for.

      * `pybliometrics.scopus.exception.Scopus413Error`: The request entity is too large to be processed by the web server.  Try a less complex query.

      * `pybliometrics.scopus.exception.Scopus414Error: TOO LARGE`: The query string you are using is too long.  Break it up in smaller pieces.

      .. _Scopus429Error:

      * `pybliometrics.scopus.exception.Scopus429Error: QUOTA EXCEEDED`: Your provided API key's weekly quota has been depleted.  If you provided multiple keys in your :doc:`configuration file <../configuration>`, this means all your keys are depleted.  In this case, wait up to week until your API key's quota has been reset.

      * `pybliometrics.scopus.exception.ScopusServerError`: General exception related to all Server-related exceptions defined below.  This may happen for various reasons (the internet is a noisy medium); usually it helps to wait few seconds before the next query.  Server errors are also raised if in searches you use a fieldname that does not exist.  Verify that your query works in Scopus' `Advanced Search <https://www.scopus.com/search/form.uri?display=advanced>`_.  Previously `pybliometrics` used more finegrained exceptions in the 5xx space, namely "Scopus500Error", "Scopus502Error" and "Scopus504Error".  These are deprecated, use "ScopusServerError" instead.

If queries break for other reasons, exceptions of type `requests.exceptions <https://requests.readthedocs.io/en/latest/api/?highlight=exceptions#exceptions>`_ are raised, such as:

`requests.exceptions.TooManyRedirects: Exceeded 30 redirects.`
    The entity you are looking for was not properly merged with another one entity in the sense that it is not forwarding.  Happens rarely when Scopus Author profiles are merged.  May also occur less often with Abstract EIDs and Affiliation IDs.

`pybliometrics` will retry to establish the connection a few times on typical server-side errors.  How often is specified in your :doc:`configuration file <../configuration>`, section "Requests" value "Retries" (if none is given, `pybliometrics` makes 5 attempts).
