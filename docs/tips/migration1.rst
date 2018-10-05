Migration Guide from 0.x to 1.x
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The upgrade from scopus 0.x to 1.x saw many changes in `scopus`' internal architecture, but also in four classes (see `change log <https://scopus.readthedocs.io/en/latest/changelog.html>`_): `ScopusAbstract()`, `ScopusAffiliation()`, `ScopusAuthor()` and `ScopusSearch()`.

To avoid too many issues resulting from missing backward-compatibility, new classes were introduced to gradually replace other ones: `AbstractRetrieval()` (replacing `ScopusAbstract()`), `AuthorRetrieval()` (replacing `ScopusAuthor()`) and `ContentAffiliationRetrieval()` (replacing `ScopusAffiliation()`).  The corresponding old classes will stay until scopus 2.x but their maintenance has been suspended.  Cached files that were downloaded with the old classes are not usable by the new classes.

`ScopusSearch()` had to be revamped completely; code that uses `ScopusSearch()` has to be updated, but not significantly.

Guiding principles
""""""""""""""""""

The change to scopus 1.x was guided by five principles:
1. Use json rather than xml for the cached files to reduce overhead and lower maintenance efforts
2. Align class names, script names, attribution names and names of folders with the names the Scopus API uses
3. Use properties to return a high share of information provided by Scopus, and get functions to increase user experience
4. Allow users to set and change configuration via a configuration file
5. Return `namedtuples <https://docs.python.org/2/library/collections.html#collections.namedtuple>`_ when Scopus provides combined information to increase interoperability with other python modules

How to update code
""""""""""""""""""

Class `AbstractRetrieval()` replaces `ScopusAbstract()`.  This class has seen the most changes.  The following attributes have been renamed but their return value stays the same (so that simply renaming it will suffice): `citationLanguage` becomes `language`, `citationType` becomes `srctype`, `citingby_url` becomes `citingby_link`, `scopus_url` becomes `scopus_link`.  There are some attributes which are now properties: `bibtex` becomes `get_bibtex()`, `html` becomes `get_html()`, `ris` becomes `get_ris()` and `latex` becomes `get_latex()`. Properties `affiliations` (new: `affiliation`), `subjectAreas` (new: `subject_areas`), `authkeywords` and `authors` are entirely different now: They return namedtuples.  Please see the `examples <https://scopus.readthedocs.io/en/latest/reference/scopus.AbstractRetrieval.html#scopus.AbstractRetrieval>`_ for how to use them.  Property `nauthors` has been removed; use `len(AbstractRetrieval(<eid>).authors` instead.  Finally, method `get_corresponding_author_info()` has been removed, as Scopus does not prodive this information any more.

Class `AuthorRetrieval()` replaces `ScopusAuthor()`.  The following properties have been renamed but their value stays the same: `author_id` becomes `identifier`, `coauthor_url` becomes `coauthor_link`, `firstname` becomes `given_name`, `hindex` becomes `h_index`, `lastname` becomes `surname`, `name` becomes `indexed_name`, `ncited_by` becomes `cited_by_count`, `ncoauthors` becomes `coauthor_count`, `ndocuments` becomes `document_count`.  Property `current_affiliation` has been renamed to `affiliation_current` but the return value is now the Scopus ID of the affiliation. Property `publication_history` has been renamed to `journal_history` and returns a list of namedtuples rather than a a list of tuples.  Property `affiliation_history` now returns a list of Scopus IDs instead of a list of `ScopusAffiliation()` objects.  Property `subject_areas` now returns a list of namedtuples instead of a list of tuples.

Class `ContentAffiliationRetrieval()` replaces `ScopusAffiliation`.  It will suffice to replace the class name in your scripts and rename the following attributes:  `nauthors` becomes `author_count`, `ndocuments` becomes `document_count`, `name` becomes `affiliation_name`, `org_url` becomes `org_URL`, `api_url` becomes `self_link`, `scopus_id` becomes `identifier`.

Class `ScopusSearch()` remains but was revamped.  The search results are now cached under a hex-ed filename to allow for complex queries.  Files are now saved in a different folder (by default).  `results` is now the main property, returning a list of namedtuples containing all useful information regarding the search results.  For convenience, `get_eids()` returns just the list of EIDs of the articles, and property `EIDS`, which will be removed in a future release, returns just this list.
