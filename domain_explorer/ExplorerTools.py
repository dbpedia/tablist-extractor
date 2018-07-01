import argparse
import sys
import rdflib
from collections import OrderedDict
import staticValues
import Utilities
import Selector, HtmlTableParser, wikiParser
import json
import urllib

class ExplorerTools:
    """
    ExplorerTools implements all methods to support DomainExplorer.py
    In this script you will find functions that goes from parsing arguments given by user to get dbpedia resources.
    This is also an interface to class Utilities, HtmlTableParser from table_extractor, because
    I used some methods from those classes.

    """

    def __init__(self):
        """
        Initialize Explorer Tools, that will:
        - parse arguments given by user.
        - get an instance of Utilities.
        - get an instance of Selector, that will fetch dbpedia resources.
        """
        self.args = self.parse_arguments()
        self.collect_mode = self.set_collect_mode()
        self.resource = self.set_source()
        self.language = self.set_language()
        self.classname = self.set_classname()

        self.utils = Utilities.Utilities(self.language, self.resource, self.collect_mode)

        # if user doesn't choose for single resource
        if self.args.collect_mode != 's':
            self.selector = Selector.Selector(self.utils)

    def parse_arguments(self):
        """
        Parse arguments given by user. You can observe three different inputs:
        - mutual exclusive group:
            - s: single resource.
            - t: dbpedia ontology class.
            - w: where clause of sparql query built by user.
        - language: language specified by two letters.
        - output organization: number that can be 1 or 2, that will change settings file format.
        - classname: Provide a classname from settings.json and use its mapper functions.

        :return: arguments passed by user
        """

        # initialize a argparse.ArgumentParser with a general description coming from staticValues.GENERAL_DESCRIPTION
        parser = argparse.ArgumentParser(description=staticValues.GENERAL_DESCRIPTION, usage=staticValues.USAGE)

        parser.add_argument('collect_mode', help=staticValues.COLLECT_MODE_HELP,
                        choices=staticValues.COLLECT_MODE_CHOICES )

        parser.add_argument('source', type=lambda s: unicode(s, sys.getfilesystemencoding()),
                        help=staticValues.SOURCE_HELP)

        """ chapter input"""
        parser.add_argument('language', type=str, default=staticValues.CHAPTER_DEFAULT, help=staticValues.CHAPTER_HELP)


        parser.add_argument('-c', '--classname', type=str, help=staticValues.CLASSNAME_HELP)

        # parsing actual arguments and return them to the caller.
        args = parser.parse_args()
        return args

    def set_collect_mode(self):
        """
        Read and set collect_mode ('s' or 't').
        :return: collect mode value
        """
        if self.args.collect_mode:
            if self.args.collect_mode in staticValues.COLLECT_MODE_CHOICES:
                return self.args.collect_mode
            else:
                sys.exit("Wrong collect_mode, available collect_mode are: "+str(ettings.COLLECT_MODE_CHOICES))

    def set_language(self):
        """
        Read and set language.
        :return: language value
        """
        if self.args.language:
            ch = self.args.language.lower()
            # search if language is available
            search = [x for x in staticValues.LANGUAGES_AVAILABLE if x == ch]
            if len(search) > 0:
                return search[0]
            else:
                sys.exit("Wrong chapter, languages available are: " + str(staticValues.LANGUAGES_AVAILABLE))

    def set_source(self):
        """
        Read source and set research_type to identify which input type is selected.
        :return: source value
        """
        if self.args.source:
            return self.args.source.encode('utf-8')

    def set_classname(self):
        """
        Read and set classname.
        :return: classname value if mentioned or else return none.
        """
        if self.args.classname:
            return self.args.classname
        else:
            return None

    def get_uri_resources(self):
        """
        Read from Selector class resources that have been found.
        uri_resource_file stands for file that contain uri's list.
        uri_resource_list will contain a uri's list represented all resources.
        :return: list of uri
        """
        uri_resource_list = []
        # if it's not a single resource
        if self.args.collect_mode != 's':
            # if there are resource
            if self.selector.tot_res_interested > 0:
                self.selector.collect_resources()
                uri_resource_file = self.selector.res_list_file
                uri_resource_list = self.extract_resources(uri_resource_file)
            else:
                sys.exit("No resources found. Please check arguments passed to pyDomainExplorer")
        else:
            uri_resource_list.append(self.args.source)
        return uri_resource_list

    def extract_resources(self, uri_resource_file):
        """
        From uri_resource_file extract all resources.
        Delete last element that is empty due to '\n'
        :param uri_resource_file: file that contains resources' uri
        :return: list of uri
        """
        content = open(uri_resource_file).read().split('\n')
        # Last resource is empty due to '\n'
        content = content[:-1]
        return content

    def print_progress_bar(self, iteration, total):
        """
        Print iterations progress
        :param iteration: number of actual iteration
        :param total: total iteration to do
        :return: nothing, print progress bar
        """
        self.utils.print_progress_bar(iteration, total)

    def html_object_getter(self, name):
        """

        :param name: resource
        :return: html object that represents resource
        """
        return self.utils.html_object_getter(name)

    def html_table_parser(self, res_name):
        """
        Method to instantiate HtmlTableParser, analyze tables and then give in output a list of tables.
        :param res_name: resource that has to be analyzed
        :return: list of tables found
        """
        html_doc_tree = self.html_object_getter(res_name)
        # if html doc is defined
        if html_doc_tree:
            graph = rdflib.Graph()
            # instantiate html table parser
            html_table_parser = HtmlTableParser.HtmlTableParser(html_doc_tree, self.language, graph,
                                                                self.resource, res_name, self.utils, False)

            # if there are tables to analyze
            if html_table_parser.tables_num>0:
                # analyze and parse tables
                html_table_parser.analyze_tables()
                return html_table_parser.all_tables
            # if there aren't tables to analyze result will be empty
            else:
                return ""
        # if html doc is not defined result will be empty
        else:
            return ""

    def wiki_parser(self, res_name):
        wiki_parser = wikiParser.wikiParser(self.language, res_name, self.utils)
        resDict = wiki_parser.main_parser()

        return resDict

    def make_sparql_dbpedia(self, service, data):
        """
        Method for making a sparql query on dbpedia endpoint.

        :param service: type of service, in order to create a unique method to make sparql query.
        :param data: information to use in sparql query.
        :return: response given by dbpedia endpoint
        """
        url = ""
        if service == "check_property":
            # header as wrote in table
            query = staticValues.SPARQL_CHECK_PROPERTY[0] +\
                    '{' + staticValues.SPARQL_CHECK_PROPERTY[1] + '"' + data + '"@' + self.language + "} UNION " +\
                    '{' + staticValues.SPARQL_CHECK_PROPERTY[1] + '"' + data.lower() + '"@' + self.language + "}" +\
                    staticValues.SPARQL_CHECK_PROPERTY[2]
            # If I change chapter language of Utilities I will make a sparql query to dbpedia.org ontology
            self.utils.language = "en"
            self.utils.dbpedia_sparql_url = self.utils.dbpedia_selection()
            url = self.utils.url_composer(query, "dbpedia")
            # restore chapter given by user
            self.utils.language = self.language
            self.utils.dbpedia_sparql_url = self.utils.dbpedia_selection()
        # get endpoint's answer
        answer = self.utils.json_answer_getter(url)
        return answer

    def get_ontology_name_from_uri(self, uri):
        """
        Function to read only ontology property.

        :param uri: uri's resource
        :return: property name
        """
        # split by '/', i need last two elements (e.g. 'resource/Kobe_Bryant' or 'ontology/weight')
        split_uri = uri.split("/")
        res_name = split_uri[-1].encode('utf-8')
        return res_name

    def get_resource_type(self, resource):
        ''' Asks all rdf:type of current resource to the local SPARQL endpoint.

        :param resource: current resource with unknown type.
        :param lang: language/endpoint.

        :return: a list containing all types associated to the resource in the local endpoint.
        '''
        lang = self.language
        if lang == 'en':
            local = ""
        else:
            local = lang + "."
        type_query = "SELECT distinct ?t WHERE {<http://" + local + "dbpedia.org/resource/" + resource + "> a ?t}"
        answer = self.sparql_query(type_query, lang)
        results = answer['results']['bindings']
        types = []
        for res in results:
            full_uri = res['t']['value']  # e.g. http://dbpedia.org/ontology/Person
            class_type = full_uri.split("/")[-1]  # e.g Person
            types.append(class_type)
        return types

    def sparql_query(self, query, lang):
        ''' Returns a JSON representation of data from a query to a given SPARQL endpoint.

        :param query: string containing the query.
        :param lang: prefix representing the local endpoint to query (e.g. 'en', 'it'..).

        :return: JSON result obtained from the endpoint.
        '''
        if lang == 'en':
            local = ""
        else:
            local = lang + "."
        
        enc_query = urllib.quote_plus(query)
        endpoint_url = "http://" + local + "dbpedia.org/sparql?default-graph-uri=&query=" + enc_query + \
                       "&format=application%2Fsparql-results%2Bjson&debug=on"
        json_result = self.utils.json_req(endpoint_url)
        return json_result

    def get_res_list_file(self):
        """
        Get file that contains all resources.
        :return: file with resources
        """
        result = ""
        if self.args.collect_mode != 's':
            result = self.selector.res_list_file.split(staticValues.PATH_FOLDER_RESOURCE_LIST)[1].replace("/", "")
        return result

    def replace_accents(self, string):
        """
        Function that replace accented letters with the associated not accented letters

        :param string: string where you have to replace accents
        :return:  string without accents
        """
        return self.utils.delete_accented_characters(string)
