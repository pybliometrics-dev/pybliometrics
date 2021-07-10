Database updates
~~~~~~~~~~~~~~~~
Scopus is a living database with changes happning constantly.  These are not just additions of new items (Articles, Books, ...) as they are published or updated citation counts, but also backfills of existing sources and corrections.  Corrections include changes of titles, names or abstracts, mergers of duplicate authors, affiliations or even research items.  Mergers affect multiple entities: For example mergers of authors affect both the authors and the articles of the duplicate.

* When author profiles are merged, the old profile(s) forward to the new one for about 6 months.  When you instantiate the :doc:`AuthorRetrieval() <../classes/AuthorRetrieval>` class with a merged profile using and then access the `.identifier` property, pybliometrics will raise a warning pointing to the ID of the new main profile.
* Keep your cached files updated.  The `refresh` parameter, which is implemented in all classes, helps you doing so.  Specifying a maximum age in days of the cached files, your local cache will always be at most that old.
* Implement cross-checks, for example to verify that an abstract is also listed as publication in the author profile.

Corrections in the Scopus database can be reported `here <https://service.elsevier.com/app/contact/supporthub/scopuscontent/>`_.
