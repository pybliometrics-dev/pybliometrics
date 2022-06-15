Change Log
----------

.. toctree::

3.4.0
~~~~~

2022-06-15

* Implement requests timeout via configuration file (default: 20 seconds).
* Introduce new exception Scopus407Error.
* In `AbstractRetrieval().references`, add new field "coverDate" and remove field "text".
* In `AbstractRetrieval().references`, deduplicate list of authors.
* Fix bug in `AuthorRetrieval().classificationgroup` with non-digits.

3.3.0
~~~~~

2022-03-22

* Add support for Python 3.10.
* Allow for arbitrary keywords in all classes.
* Allow for individual API key and InstToken when initiating any class (via paramters `apikey` and `insttoken`), which overrides the values retrieved form the configuration file.
* In `AbstractRetrieval()`, add new properties `copyright`, `copyright_type` and `date_created`.
* In `ScopusSearch().auth_afid`, return `None` instead of empty list when there are no affiliation information.
* Fix bug with `AbstractRetrieval().authorgroup` for collaborations.
* In `ScopusSearch()`, fix bug with properties `.freetoread` and `.freetoreadLabel` resulting from non-standard format.

3.2.0
~~~~~

2022-01-02

* In `ScopusSearch().results`, add fields "freetoread" and "freetoreadlabel".
* In `AbstractRetrieval().authorgroup`, add field "orcid".
* In `AuthorSearch().authors`, add field "orcid".
* In `create_config()`, add parameters "keys" and "instoken" for usage in workflows under CI.
* Adapt timestamp to Scopus changes in `.get_key_reset_time()` method.
* Improve documentation w.r.t. to the configuration file.
* Fix bug with generation of configuration file.
* Fix bug with custom location of configuration file.
* Fix bug in `SerialTitle().citescoreinfolist` for discontinued sources.

3.1.0
~~~~~

2021-10-16

* In `AbstractRetrieval().funding`, rename field "id" to "agency_id", add field "funding_id" and change order.
* Introduce new exceptions Scopus504Error and document Scopus413Error.
* Better document `SerialTitle()` w.r.t. to journal metrics.
* Correct document of where to find the cache folder since pybliometrics 3.x.

3.0.1
~~~~~

2021-08-01

* Fix bug with generation of configuration file.
* Fix bug with all search classes not testing the number of results before downloading.
* Fix bug with deprecation warning of `CitationOverview()`.

3.0
~~~

2021-07-18

* Implement throttling as per Scopus' definition.
* Enable type hints.
* Revamp documentation: Document all classes with examples on the same page in the new section "Classes"; Add new section "Access" using subsections previously listed under "Tips".
* For the following properties, type str changed to numeric type (either as scalar or within a container): `AbstractRetrieval().authorgroup.affiliation_id`, `AbstractRetrieval().authorgroup.dep_id` and `AbstractRetrieval().authorgroup.auid`, `AbstractRetrieval().authors.id`, `AbstractRetrieval().authors.auid`, `AbstractRetrieval().citedby_count`, `AbstractRetrieval().confcode` `AbstractRetrieval().identifier`, `AbstractRetrieval().openaccess`, `AbstractRetrieval().pubmed_id`, `AbstractRetrieval().source_id`, `AbstractRetrieval().subject_areas.code` `AffiliationRetrieval().author_count`, `AffiliationRetrieval().document_count`, `AffiliationRetrieval().identifier`, `AffiliationRetrieval().name_variants.doc_count`, `AffiliationSearch().affiliations.documents`, `AuthorRetrieval().affiliation_current.id` and `AuthorRetrieval().affiliation_current.parent`, `AuthorRetrieval().affiliation_history.id` and `AuthorRetrieval().affiliation_history.parent`, `AuthorRetrieval().citation_count`, `AuthorRetrieval().cited_by_count`, `AuthorRetrieval().classificationgroup`, `AuthorRetrieval().coauthor_count`, `AuthorRetrieval().document_count`, `AuthorRetrieval().historical_identifier`, `AuthorRetrieval().identifier`, `AuthorRetrieval().subject_areas.code`, `AuthorSearch().authors.documents`, `ScopusSearch().results.citedby_count` and `ScopusSearch().results.openaccess`, `SerialTitle().citescoreyearinfolist`, `SerialTitle().sjrlist`, `SerialTitle().sniplist`, `SerialTitle().source_id`, `SerialTitle().subject_area.code`.
* The type of `AbstractRetrieval().authors.affiliation` is now a string joining all affiliation IDs on ";".
* In `AffiliationSearch()` and `AuthorSearch()`, parameter `count` is deprecated and will be removed in a future release.  There is no substitute.
* In `AbstractRetrieval()`, property `.correspondence` is now a list.
* In `CitationOverview()`, parameter `eid` is deprecated and will be removed in a future release.  Instead, the class now accepts a list of up to 25 identifiers (Scopus ID, DOI, PII or Pubmed ID) and returns individual citation trajectories for each of the documents.
* In `CitationOverview()`, all current properties now return lists, except for `.h_index`, which remains int.
* In `CitationOverview()`, add new properties `.columnTotal`, `.grandTotal`, `.laterColumnTotal`, `prevColumnTotal`, `.rangeColumnTotal`.
* In `CitationOverview()`, change the cache file name to md5-hash of the used identifiers plus the citation type information (e.g., when self-citations are excluded).
* In `AffiliationRetrieval()`, add property `.status`.
* In `SubjectClassifications()`, the default cache file path now goes without the folder "STANDARD".
* The default folder for the configuration file become `.pybliometrics` instead of `.scopus`, but if `.scopus` exists, `pybliometrics` will use this folder.  New installations will only use `.pybliometrics`.  The default path for the cache file folders has become `.pybliometrics/Scopus/`.
* Allow for kwds to be passed on in the following classes: `AffiliationRetrieval()`, `AffiliationSearch()`, `AuthorSearch()`, `CitationOverview()`, `SubjectClassifications()`.
* For search classes, change error message when the search result size exceeds 5k.  The possiblity to change this number has been removed.
* In all classes, raise ValueError if parameter `refresh` is neither int nor bool.
* In all classes, harmonize error message documentation and order of parameters.
* Require `tqdm` package to print progress bars.
* Class `ContentAffiliationRetrieval()` has been removed.
* Fix bug that cached an empty file when `download=False` using any Search class.

2.9.1
~~~~~

2021-02-25

* Allow for the LIGHT view in `AffiliationRetrieval()` to retrieve fewer information.
* Allow for the METRICS, LIGHT and STANDARD views in `AuthorRetrieval()` to retrieve fewer information.
* In `AuthorRetrieval().h_index` and `AuthorRetrieval().coauthor_count`, return `None` instead of 0 as default value.

2.9
~~~

2021-02-11

* New class `SubjectClassifications()` to interact with the Subject Classifications API.
* In `CitationOverview()`, add optional parameter `citation` to allow for exlusion of self-citations or those of books.
* Fix links in class docstrings.

2.8
~~~

2021-01-28

* Class `ContentAffiliationRetrieval()` has been renamed to `AffiliationRetrieval()`; `ContentAffiliationRetrieval()` will remain until 3.0 but it will raise a Warning.
* Add parameter `years` to `SerialTitle()`, to retrieve journal metrics for specific years.
* Fix documentation on InstToken.
* Fix bug with reading empty queries.

2.7.2
~~~~~

2020-12-08

* Fix bug with writing empty results of search classes.
* In `AuthorRetrieval()`, allow for kwds to be passed on to the retrieval.
* Update some documentation w.r.t. to differences between the API and the website.

2.7.1
~~~~~

2020-11-30

* Always dump minified json.
* Introduce new exceptions: Scopus413Error and Scopus502Error.
* Change print dunder functions to allow for singleton counts.
* In `ScopusSearch()`, respect 'count' argument when passed as keyword.
* Update some documentation and fix internal links.
* In `AuthorRetrieval()`, fix bug with private variable.

2.7
~~~

2020-09-25

* Introduce new exception: Scopus414Error.
* In `AuthorRetrieval()`, add new property `.alias`.
* In `AbstractRetrieval()`, add new properties `.subtype` and `.subtypedescription`.
* Fix bug with kwds in all search classes accidentally not passed on requests.

2.6.3
~~~~~

2020-08-04

* In `AbstractRetrieval()`, add new properties `.openaccess` and `.openaccessFlag`.
* In `AuthorSearch().__str__`, fix bug with missing names.
* In `AuthorRetrieval().__str__`, fix bug with already removed property `.journal-history`.
* For all search classes, do not create an empty file when `download=False`.

2.6.2
~~~~~

2020-07-21

* In `AuthorRetrieval()`, remove property `.journal-history` as it was removed from the API.
* Fix bug with duplicate entries in multi-page search results with cursors.

2.6.1
~~~~~

2020-07-14

* Show date of retrieval when printing any class object.
* Refactor some of the information when printing class objects.
* Fix bug related to missing requests header with empty results.
* Fix bug with missing source history when printing an `AuthorRetrieval()` object.

2.6
~~~

2020-07-10

* Add support for multiple keys in the configuration file, and replace depleted keys automatically.
* In all classes, add methods `.get_key_remaining_quota()` and `.get_key_reset_time()` to get the remaining calls of the current key and the time when the current key will be reset, relative to the last actual request.
* Provide link examples in reference of each class.
* In `ScopusSearch().results`, use empty strings for missing affiliations (e.g. non-org profile affiliations) when information in concatenated.
* Fix bug in `ScopusSearch().results` when affiliation information has the wrong type (e.g. boolean).

2.5
~~~

2020-05-25

* New class `SerialSearch()` to search via the Serial Title API.
* Add new exception Scopus403Error for forbidden access.
* Fix bug with `AuthorRetrieval().get_coauthors()` only returning the first 25 results.
* Fix bug with progress bar in search classes not showing.

2.4
~~~

2020-04-15

* `PlumXMetrics()` class to access the PlumX Metrics API.
* Fix and update the str dunder functions of all classes.
* Fix bug with raising a ScopusException when the resulting json is malformatted.

2.3.2
~~~~~

2020-03-29

* In `AuthorRetrieval().estimate_uniqueness()`, allow for args and fix documentation.
* Fix bug with missing file modification time stamp.

2.3.1
~~~~~

2020-03-29

* In `AuthorRetrieval().get_coauthors()`, return `None` instead of empty list when there are no coauthors.
* Improve warning and error messages.
* Improve all documentation.

2.3
~~~

2020-03-22

* Support for python 2.7 has ended.
* Introduce `Base()` class from which all classes inherit the following two methods: `.get_cache_file_age()` and `.get_cache_file_mdate()`.
* In all classes, refresh parameter accepts an integer which will refresh the cached file if the last modification date is longer than that number of days ago.
* Provide extensive affiliation information in `AuthorRetrieval().affiliation_current` and `AuthorRetrieval().affiliation_history` as namedtuples.
* Provide more robust example of the "Download Machine" in the documentation.
* Fix typos and formatting errors in the documentation.
* In `AbstractRetrieval().__str__`, fix bug due to missing authors and affiliations.

2.2.2
~~~~~

2019-12-29

* EIDs starting with "1-s2.0-" are automatically detected as EID as well.
* In `ScopusSearch().results` add field "subtypeDescription".
* In `AbstractRetrieval().idxterms` return None instead of empty lists.
* In `AbstractRetrieval().confdate` return None instead of list with tuples with None.
* Add UserWarning for change of type of `AuthorRetrieval().affiliation_current` and `AuthorRetrieval().affiliation_history`.

2.2.1
~~~~~

2019-09-09

* Add user agent string to evaluate usage.
* Fix bug with missing journal metrics in `SerialTitle()`.

2.2
~~~

2019-08-21

* Add parameters `integrity_fields` and `integrity_action` to all search classes to avoid KeyErrors of missing fields.
* Add progress bar to all search classes indicating download progress.
* Fix bug with missing entries in author-group list in `AbstractRetrieval()`.

2.1.3
~~~~~

2019-07-16

* Fix bug detecting DOIs without slash in `AbstractRetrieval()`.
* Fix bug related to creating the config file.

2.1.2
~~~~~

2019-07-09

* Fix bugs arising from passing duplicate parameters through kwds in Search classes.
* Fix bug in `AbstractRetrieval().references` with duplicte volume/issue information from Scopus.
* Fix bug with wrong object type when using `AuthorRetrieval().get_coauthors()`.

2.1.1
~~~~~

2019-06-26

* New properties for `AbstractRetrieval()`: `pii` and `pubmed_id`.
* Improve documentation (`AbstractRetrieval().idxterms` and download machine).
* Fix bug forcing the presence of the package `scopus`.

2.1.0
~~~~~

2019-06-17

* Rename package to pybliometrics.
* In all search classes, properties return None if download=False instead of raising an error.

2.0.1
~~~~~

2019-06-08

* In `AbstractRetrieval().references`, add field "type" for the status of the parsed reference.
* Raise proper Scopus.exception even when no Scopus-supplied error message exists.
* In `AbstractRetrieval()`, update docstrings.
* Fix bug related to creating the config when the config doesn't exist.
* Fix bug when using `AbstractRetrieval()` in Python 2.

2.0
~~~

2019-05-28

* Cache files in subfolders according to the used view.
* Add method `.estimate_uniqueness()` to `AuthorRetrieval()` to estimate how unique an author profile is.
* Use error message provided by Scopus for ScopusErrors.
* Add tip how to deal with "KeyError: 'eid'".
* Remove deprecated classes, modules, parameters and attributes.  Removed deprecated classes are `ScopusAbstract()`, `ScopusAffiliation()`, `ScopusAuthor()` and `report()`.  Removed deprecated parameters are start and max_entries in `AuthorSearch()` and `AffiliationSearch()`.  Removed deprecated attributes include only `ScopusSearch.EIDS`.

1.6.1
~~~~~

2019-05-14

* Add support for proxies.
* In `AbstractRetrieval().correspondence`, turn values into proper strings.
* Fix bug when creating the config file.

1.6
~~~

2019-05-09

* `SerialTitle()` class to access the Serial Title API.
* In all search classes, add method `.get_results_size()` to return the number of matches.
* In all search classes, add boolean parameter `download` to not download the results (but get the number of matches anyways).
* In `AbstractRetrieval().authorgroup`, rename field "city-group" to "city" and add new fields: "dptid", "postalcode", "addresspart".
* In `AbstractRetrieval().authorgroup`, fix bug with missing affiliation information.
* In all search classes, remove deprecated parameter `start`.

1.5
~~~

2019-05-16

* Add parameter `subscriber` to `ScopusSearch()` class to set request parameters to maximum values depending on view.
* Add support for cursor-navigation in searches.
* Add `__citation__` dunder.
* Allow for the REF view in `AbstractRetrieval()` to obtain detailed information on referenced items.
* New properties for `AuthorRetrieval()`: `historical_identifier` and `status`.
* Allow `ScopusSearch()` to pass on kwds as query params.
* Deprecate `start` and `max_entries` parameters in `AffiliationSearch()` and `AuthorSearch()`.
* Deprecate `start` parameter in `ScopusSearch()` class.
* Fix bug with `ContentAffiliationRetrieval().__str__`.
* Fix bugs in `AbstractRetrieval()` related to missing information obtained from Scopus.

1.4.3
~~~~~

2019-02-12

* Fix bug with empty value in `AbstractRetrieval().language`.
* Add matplotlib as requirement.

1.4.2
~~~~~

2019-02-05

* Fix bug with TypeErrors when navigating a path in the json.
* Fix bug with missing author information in `AbstractRetrieval().authors`.
* Fix bug with missing title in `AbstractRetrieval().title`.

1.4.1
~~~~~

2019-01-24

* Add citation.
* Render reports class deprecated.
* Add str-dunder function for `CitationOverview()` class.

1.4
~~~

2019-01-17

* Use number of results from first search query rather than from separate query.
* Write empty file if search is empty.
* In `ScopusSearch().results`, add new fields: "affilname", "affiliation_city", "affiliation_country", "article_number", "author_count", "authkeywords", "eIssn", "description", "fund_acr", "fund_no", "fund_sponsor", "pubmed_id".
* In `ScopusSearch().results`, rename the following fields: "names" to "author_names", "authid" to "author_ids", "afid" to "author_afids".
* In `ScopusSearch()`, add parameter view to specify the view and number of entries per query run.
* In `AbstractRetrieval().affiliation`, `AbstractRetrieval().authorgroup`, `AbstractRetrieval().authors`, `AbstractRetrieval().subject_areas`, `AffiliationSearch().affiliations`, `AuthorRetrieval().classificationgroup`, `AuthorRetrieval().journal_history`, `AuthorRetrieval().name_variants`, `AuthorSearch().authors`, `CitationOverview().authors` and `ScopusSearch().results` return `None` if the result list is empty, instead of an empty list.
* In `AbstractRetrieval().chemicals`, fix bug with missing values for cas-registry-number.
* Allow for the STANDARD view in `ScopusSearch()` to increase number of results per query.
* Refactor all classes internally for maintainability and readability.
* Register project with Code Climate.

1.3.1
~~~~~

2018-12-11

* Extend tests for `ScopusSearch()`.
* Fix bug with zero search results.
* Open cached search files in binary mode.
* Fix bug in `AbstractRetrieval()` with missing affiliation names in `.authorgroup`.

1.3
~~~

2018-12-04

* Fix bugs related to empty values or missing keys in `AuthorRetrieval()` (`.affiliation_history`, `.get_coauthors()`, `.journal_history`, `.name_variant`, `preferred_name`, `.subject_area`) and in `ScopusSearch()` (`.results`).
* Introduce `Retrieval()` superclass for all retrieval and content classes.
* Refactor `Search()` superclass and all search classes internally.
* Implement scopus-specific exceptions.

1.2
~~~

2018-10-24

* In `AbstractRetrieval()`, users can now initate the class with DOI, Scopus ID, PII or Pubmed ID.  Parameter `EID` has hence been deprecatd in favor of the new parameter `identifier`.
* New properties for `AbstractRetrieval()`: `chemicals`, `contributor_group`, `funding`, `funding_text`, `isbn`, `sequencebank`.
* In `ContentAffiliationRetrieval(), return `None` rather than empty dict when no address is provided.
* In `AbstractRetrieval().confsponsor, return `None` when no confsponsor is provided.
* In `ScopusSearch().results`, return "afid" as part of namedtuple.
* Fix bug in `AbstractRetrieval().authorgroup` related to affiliation groups without authors.
* Fix bug in `AbstractRetrieval().affiliation` related to affiliations without Scopus ID.
* Fix bugs in `ScopusSearch().results` with duplicate authors, missing titles and unusual coverDates.
* `AuthorRetrieval()` warns User via UserWarnings if the supplied author ID is outdated or if it has been forwarded to a new profile.

1.1
~~~

2018-10-07

* Generate configuration file via separate method, not directly on import.

1.0
~~~

2018-10-06

* New class `AbstractRetrieval()` to replace `ScopusAbstract()`, with the following properties renamed: `affiliations`: `affiliation`, `bibtex`: `get_bibtex()`, `citationLanguage`: `language`, `citationType`: `srctype`, `citingby_url`: `citingby_link`, `html`: `get_html()`, `ris`: `get_ris()`, `latex`: `get_latex()`, `scopus_url`: `scopus_link`, `subjectAreas`: `subject_areas`.
* New class `AuthorRetrieval()` to replace `ScopusAuthor()`, with the following properties renamed: `author_id`: `identifier`, `coauthor_url`: `coauthor_link`, `current_affiliation`: `affiliation_current`, `firstname`: `given_name`, `hindex`: `h_index`, `lastname`: `surname`, `name`: `indexed_name`, `ncited_by`: `cited_by_count`, `ncoauthors`: `coauthor_count`, `ndocuments`: `document_count`, `publication_history`: `journal_history`.
* New class `ContentAffiliationRetrieval()` to replace `ScopusAffiliation()`, with  the following properties renamed: `api_url`: `self_link`, `nauthors`: `author_count`, `ndocuments`: `document_count`, `name`: `affiliation_name`, `org_url`: `org_URL`, `scopus_id`: `identifier`.
* Rewrite class `ScopusSearch()`: new property `results`, cache search results in json format with hex-ed filename and new method `get_eids()`, which replaces property `EIDS`.
* Use config.ini to store API Key (and if necessary, InstToken) as well as directories.
* Migration Guide to update code from scopus 0.x to 1.x

0.10
~~~~

2018-08-14

* In `ScopusAuthor()`, refactor generating abstracts lists into `get_journal_abstract()`.
* New properties for `ScopusAbstract()`: `citedby_url` and `scopus_url`.
* New property for `ScopusAffiliation()`: `state`.
* Correct property `citedby_url` from `ScopusAuthor()`.
* In all retrieval classes, remove underscore properties.

0.9
~~~

2018-07-23

* `SearchAffiliation()` to access the Affiliation Search API.
* Fix bug occuring with fields of length one in Author search.
* `ScopusAbstract()` returns abstract keywords if present.
* Refactor search classes to inherit from common auxiliary class.
* `ScopusAffiliation()` now accepts EID as well.

0.8
~~~

2018-06-18

* `ScopusAuthor()` now accepts EID as well.
* Fix bug occuring with non-existent journal abbreviations.
* `SearchAuthor()` class to access the Author Search API.
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

* `CitationOverview()` class to access the Abstract Citation View.

0.5
~~~

2017-09-28

* New properties for `ScopusAuthor()`: `publication_history` and `subject_areas`.
* Update namespace in `ScopusAbstract()` to retrieve affiliation information.
* Complete affiliation information in `ScopusAbstract()`.

0.4.4
~~~~~

2017-09-06

* Fix bugs related to unicode on Python2.7 and installation on Windows.

0.4.3
~~~~~

2017-08-30

* Update `ScopusAbstract()` to reflect change in the API.

0.4.2
~~~~~

2017-08-23

* Fix bug with generating `my_scopus.py` on Python 3.
* In `ScopusAbstract()`, do not raise TypeErrors for information not present in current view.

0.4.1
~~~~~

2017-08-20

* Remove unwanted `print()` statement.

0.4
~~~

2017-08-20

* Use `refresh_affiliation` parameter in `ScopusAuthor()`.
* Improve background service to load user's API key.
* Ask user for API key if it can't be found.
* New property for `ScopusAbstract()`: `citation_count`.

0.3.1
~~~~~

2017-08-09

* Update `ScopusAbstract()` to reflect change in the API.

0.3.0
~~~~~

2017-08-02

* Few bugfixes.
* New property for `ScopusAbstract()`: `abstract`.
* Change latex key in `ScopusAbstract().bibtex` to <FirstauthorYearTitlefirstwordTitlelastword>.
* Raise ValueError in `ScopusAbstract()` if .bibtex or .ris is called on an item whose aggregationType is not Journal.
* Improved docstrings for `ScopusAbstract()`.
* New properties for `ScopusAffiliation()`: `api_url`, `date_created`, `org_type`, `org_domain`, `org_url`.
* In `ScopusAffiliation()`, the `affiliation_id` returns the Scopus Affiliation ID from the result rather than the used aff_id.

0.2.1
~~~~~

2017-07-21

* Some bugfixes.
* Examples for all classes.
* Fix typos in docstrings.
* In `ScopusAuthor()`, the `author_id` returns the Scopus Author ID from the result rather than the used author_id.

0.2.0
~~~~~

2017-04-05

* Several bugfixes.
* Docstrings for all classes according to numpy standard.
* Outsourced help functions in module `utils`.
* Import classes in `__init__` to allow top level import.
* New methods for `ScopusAuthor()`: `n_yearly_publications()`.
* New properties for `ScopusAbstract()`: `citationType`, `citationLanguage`, `refcount`, `references`, `subjectAreas`, `website`.
* Raising exception when download status is not ok.
* Python2.7 compatibility.

0.1.0
~~~~~

2016-02-22

* Initial release.
