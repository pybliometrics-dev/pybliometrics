KeyError
~~~~~~~~
There are idiosynchratic, seemingly KeyErrors when accessing `ScopusSearch().results`.  The error means that for at least one entry, the EID is missing, which in reality should not happen.  This is not a bug of `pybliometrics`.  Instead it is somehow related to a problem in  the download process from the Scopus database.  The probability of observing a KeyError increases in the results size.

The solution is simply to refresh the file.  Optimally you want to write a function that makes the query robust to the KeyError, i.e. attempting to return `ScopusSearch().results` until there is no KeyError.  Trying at least once is recommended:

.. code-block:: python
   
    def robust_query(q, refresh=False):
        """Wrapper function for individual ScopusSearch query."""
        try:
            return ScopusSearch(q, refresh=refresh).results
        except KeyError:
            return ScopusSearch(q, refresh=True).results
