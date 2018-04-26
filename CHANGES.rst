Change Log
----------

.. toctree::

0.7
~~~

2018-04-27

* Use https instead of http wherever possible.
* Add support for InstToken Authentication via config file.
* Redirect DOI links to preferred resolver.

0.6
~~~

2017-12-12

* CitationOverview class to access the Abstract Citation View.


0.5
~~~

2017-09-28

* New properties for ScopusAuthor: publication_history and subject_areas.
* Update namespace in ScopusAbstract to retrieve affiliation information.
* Complete affiliation information in ScopusAbstract.

0.4.4
~~~~~

2017-09-06

* Fix bugs related to unicode on Python2.7 and installation on Windows.

0.4.3
~~~~~

2017-08-30

* Update ScopusAbstract to reflect change in the API.

0.4.2
~~~~~

2017-08-23

* Fix bug with generating `my_scopus.py` on Python 3.
* In ScopusAbstract, do not raise TypeErrors for information not present in current view.

0.4.1
~~~~~

2017-08-20

* Remove unwanted print() statement.

0.4
~~~

2017-08-20

* Use refresh_affiliation parameter in ScopusAuthor.
* Improve background service to load user's API key.
* Ask user for API key if it can't be found.
* New property for ScopusAbstract: `citation_count`.

0.3.1
~~~~~

2017-08-09

* Update ScopusAbstract to reflect change in the API.

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
