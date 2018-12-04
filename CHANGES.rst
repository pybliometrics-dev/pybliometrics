Change Log
----------

.. toctree::

1.3
~~~

2018-11-04

* Fix bugs related to empty values or missing keys in `AuthorRetrieval` (.affiliation_history, .get_coauthors(), .journal_history, .name_variant, referred_name, .subject_area) and in `ScopusSearch` (.results).
* Introduce Retrieval() superclass for all retrieval and content classes.
* Refactor Search() superclass and all search classes internally.
* Implement scopus-specific exceptions.

1.2
~~~

2018-10-24

* In AbstractRetrieval, users can now initate the class with DOI, Scopus ID, PII or Pubmed ID.  Parameter `EID` has hence been deprecatd in favor of the new parameter `identifier`.
* New properties for AbstractRetrieval: `chemicals`, `contributor_group`, `funding`, `funding_text`, `isbn`, `sequencebank`.
* In ContentAffiliationRetrieval, return None rather than empty dict when no address is provided.
* In AbstractRetrieval.confsponsor, return None when no confsponsor is provided.
* In ScopusSearch.results, return "afid" as part of namedtuple.
* Fix bug in AbstractRetrieval.authorgroup related to affiliation groups without authors.
* Fix bug in AbstractRetrieval.affiliation related to affiliations without Scopus ID.
* Fix bugs in ScopusSearch.results with duplicate authors, missing titles and unusual coverDates.
* AuthorRetrieval warns User via UserWarnings if the supplied author ID is outdated or if it has been forwarded to a new profile.

1.1
~~~

2018-10-07

* Generate configuration file via separate method, not directly on import.

1.0
~~~

2018-10-06

* New class AbstractRetrieval to replace ScopusAbstract, with the following properties renamed: `affiliations`: `affiliation`, `bibtex`: `get_bibtex()`, `citationLanguage`: `language`, `citationType`: `srctype`, `citingby_url`: `citingby_link`, `html`: `get_html()`, `ris`: `get_ris()`, `latex`: `get_latex()`, `scopus_url`: `scopus_link`, `subjectAreas`: `subject_areas`
* New class AuthorRetrieval to replace ScopusAuthor, with the following properties renamed: `author_id`: `identifier`, `coauthor_url`: `coauthor_link`, `current_affiliation`: `affiliation_current`, `firstname`: `given_name`, `hindex`: `h_index`, `lastname`: `surname`, `name`: `indexed_name`, `ncited_by`: `cited_by_count`, `ncoauthors`: `coauthor_count`, `ndocuments`: `document_count`, `publication_history`: `journal_history`
* New class ContentAffiliationRetrieval to replace ScopusAffiliation, with  the following properties renamed: `api_url`: `self_link`, `nauthors`: `author_count`, `ndocuments`: `document_count`, `name`: `affiliation_name`, `org_url`: `org_URL`, `scopus_id`: `identifier`
* Rewrite class ScopusSearch: new property `results`, cache search results in json format with hex-ed filename and new method `get_eids()`, which replaces property `EIDS`
* Use config.ini to store API Key (and if necessary, InstToken) as well as directories
* Migration Guide to update code from scopus 0.x to 1.x

0.10
~~~~

2018-08-14

* In ScopusAuthor, refactor generating abstracts lists into `get_journal_abstract()`.
* New properties for ScopusAbstract: `citedby_url` and `scopus_url`
* New property for ScopusAffiliation: `state`
* Correct property citedby_url from ScopusAuthor.
* In all retrieval classes, remove underscore properties.

0.9
~~~

2018-07-23

* SearchAffiliation to access the Affiliation Search API.
* Fix bug occuring with fields of length one in Author search.
* ScopusAbstract returns abstract keywords if present.
* Refactor search classes to inherit from common auxiliary class.
* ScopusAffiliation now accepts EID as well.

0.8
~~~

2018-06-18

* ScopusAuthor now accepts EID as well.
* Fix bug occuring with non-existent journal abbreviations.
* SearchAuthor class to access the Author Search API.
* Fix links in examples.

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

* New properties for ScopusAuthor: `publication_history` and `subject_areas`.
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
