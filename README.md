# Tablist-extractor : Unified Table and List Extractors

Tablist-extractor is a tool to extract the information present inside the lists and tables of Wiki pages and to form appropriate RDF triples. It is basically the fusion of existing two projects, namely **[table extractor](https://github.com/dbpedia/table-extractor)** and **[list extractor](https://github.com/dbpedia/list-extractor)**

## Get Started

The main idea of this project is to analyze the resources choosen by the user and to create appropriate RDF triples. This project mainly consists of two phases, exploring phase and extraction phase. During the first stage, we have to run `domainExplorer` with suitable arguments. This creates `domain_settings.py` file in `domain_explorer` folder. User has to edit this file before the next phase. The comments in the file will help the user to edit it accordingly. Then during extraction phase, we have to run `domainExtractor` that reads previously edited file and maps the data of the resources to form RDF triples which gets saved in the `Extracted` folder. 

### Requirements

The extractor is written in Python 2.7. All the requirements needed to run this project can be installed by executing the below line in the terminal.
`pip install -r requirements.txt`

### How to run tablist-extractor

#### Exploring Phase

In this phase, the program will analyze the tables, lists information present in wiki pages and collects all the ontology mappings required to form RDF triples.

`python domainExplorer.py [collect_mode] [resource] [language]`

* `collect_mode`: `s` or `t`
	* Use `s` for a single resource and `t` for a whole topic/ domain.

* `resource`: a string representing a class of resources from DBpedia ontology, or a single Wikipedia page of an actor/writer. 

* `language`: `en`, `it`, `de` etc. (for now, available only some languages, for selected domains)

    * a two-letter prefix corresponding to the desired language of Wikipedia pages and SPARQL endpoint to be queried.

By running the above command, the mappings required for creating triples are stored in `domain_settings.py` file of `domain_explorer` directory. `domain_settings.py` contains all sections and headers found in exploration of the domain. You will observe a dictionary structure and some fields that have to be filled.

* Next step is to fill `domain_settings.py`. Remember that you are writing mapping rules, so you are making an association between a table's/list's header (or sections) with a dbpedia ontology property.

* After completion of the above step, we are ready for the next phase.

#### Extraction Phase

This script reads all the parameters present in `domain_explorer/domain_settings.py` and saves a .ttl file that contains RDF triples obtained by domain's analysis.

`python domainExtractor.py`

The above command creates a .ttl file for the respective resources in the `Extracted` folder.

### Examples

* `python domainExplorer.py s Kobe_Bryant en`

* `python domainExplorer.py s William_Gibson en`

### How to run GUI of extraction process

* `python guiExtractor.py`

* Follow the instructions step by step as guided in the UI. For hints to fill the required fields, hover onto the field area.

### Notes

* If everything goes well, three files are created in `/Extracted` folder : two log file (one for domainExplorer and one for domainExtractor) and a .ttl file containing the serialized rdf data set.

### Attributions for 3rd party tools:

This project uses 2 other existing open source projects.

* **JSONpedia**, a framework designed to simplify access at MediaWiki contents transforming everything into JSON. Such framework provides a library, a REST service and CLI tools to parse, convert, enrich and store WikiText documents. 

The software is copyright of Michele Mostarda (me@michelemostarda.it) and released under Apache 2 License.
Link : [JSONpedia](https://bitbucket.org/hardest/jsonpedia)

* **JCommander**,  a very small Java framework that makes it trivial to parse command line parameters. 

Contact Cédric Beust (cedric@beust.com) for more information. Released under Apache 2 License.
Link : [JCommander](https://github.com/cbeust/jcommander)

## Progress page

* **[GSoC 2018 progress page](https://github.com/dbpedia/tablist-extractor/wiki/GSoC-18---Progress-Report)**
