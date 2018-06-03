# Tablist-extractor : Unified Table and List Extractors


## Get Started

### How to run tablist-extractor

`python domainExplorer.py [collect_mode] [resource] [language] [-f output_format]`

* `collect_mode`: `s` or `t`
	* Use `s` for a single resource and `t` for a whole topic/ domain.

* `resource`: a string representing a class of resources from DBpedia ontology, or a single Wikipedia page of an actor/writer. 

* `language`: `en`, `it`, `de` etc. (for now, available only some languages, for selected domains)

    * a two-letter prefix corresponding to the desired language of Wikipedia pages and SPARQL endpoint to be queried.

* `-f --output_format`: `1` or `2`.
	* Integer which can be 1 or 2. Each value corresponds to a different organization of output file.

By running the above command, a `domain_settings.py` file is created in `domain_explorer` directory. `domain_settings.py` contains all sections and headers found in exploration of the domain. You will observe a dictionary structure and some fields that have to be filled.

* Next step is to fill `domain_settings.py`. Remember that you are writing mapping rules, so you are making an association between a table's/list's header (or sections) with a dbpedia ontology property.

### Examples

* `python domainExplorer.py s Kobe_Bryant en -f 2`