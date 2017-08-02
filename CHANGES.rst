Change Log
----------

0.3.0
~~~~~

2017-08-02

* Few bugfixes.
* New property for ScopusAbstract: `abstract`.
* Change latex key in ScopusAbstract.bibtex to <FirstauthorYearTitlefirstwordTitlelastword>
* Raise ValueError in ScopusAbstract if .bibtex or .ris is called on an item whose aggregationType is not Journal.
* Improved docstrings for ScopusAbstract.
* New properties for ScopusAffiliation: `api_url`, `date_created`, `org_type`, `org_domain`, `org_url`.
* In ScopusAffiliation, the `affiliation_id` returns the Scopus Affiliation ID from the result rather than the used aff_id.

0.2.1
~~~~~

2017-07-21

* Some bugfixes.
* Examples for all classes.
* Fix typos in docstrings.
* In ScopusAuthor, the `author_id` returns the Scopus Author ID from the result rather than the used author_id.

0.2.0
~~~~~

2017-04-05

* Several bugfixes.
* Docstrings for all classes according to numpy standard.
* Outsourced help functions in module `utils`.
* Import classes in `__init__` to allow top level import.
* New methods for ScopusAuthor: `n_yearly_publications()`.
* New properties for ScopusAbstract: `citationType`, `citationLanguage`, `refcount`, `references`, `subjectAreas`, `website`.
* Raising exception when download status is not ok.
* Python2.7 compatibility.

0.1.0
~~~~~

2016-02-22

* Initial release.
