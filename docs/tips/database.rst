Database updates
----------------

Scopus is a living database with changes happening constantly.  These are not just additions of new items (Articles, Books, ...) as they are published or updated citation counts, but also backfills of existing sources and corrections.  Corrections include changes of titles, names or abstracts, mergers of duplicate authors, affiliations or even research items.  Mergers affect multiple entities at once: for instance, author mergers impact both the authors' profiles and the associated articles.

* When author profiles are merged, the old profile(s) forward to the new one for about 6 months.  When you instantiate the :doc:`AuthorRetrieval() <../reference/scopus/AuthorRetrieval>` class with a merged profile using and then access the `.identifier` property, pybliometrics will raise a warning pointing to the ID of the new main profile.
* Keep your cached files updated.  The `refresh` parameter, which is implemented in all classes, helps you do so.  Specifying a maximum age in number of days when making calls (e.g., `AuthorRetrieval(..., refresh=20)`), your local cache will always be at most that old.
* Implement cross-checks, for example to verify that an abstract is also listed as publication in the author profile.

Corrections in the Scopus database can be reported `here <https://service.elsevier.com/app/contact/supporthub/scopuscontent/>`_.
