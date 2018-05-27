import argparse
import sys
import rdflib
from collections import OrderedDict
import settings
import Utilities
import Selector, HtmlTableParser, wikiParser
import json

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
        self.output_format = self.set_output_format()
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

        # initialize a argparse.ArgumentParser with a general description coming from settings.GENERAL_DESCRIPTION
        parser = argparse.ArgumentParser(description=settings.GENERAL_DESCRIPTION, usage=settings.USAGE)

        parser.add_argument('collect_mode', help=settings.COLLECT_MODE_HELP,
                        choices=settings.COLLECT_MODE_CHOICES )

        parser.add_argument('source', type=lambda s: unicode(s, sys.getfilesystemencoding()),
                        help=settings.SOURCE_HELP)

        """ chapter input"""
        parser.add_argument('language', type=str, default=settings.CHAPTER_DEFAULT, help=settings.CHAPTER_HELP)

        """ output organization input"""
        parser.add_argument('-f', '--output_format', help=settings.OUTPUT_FORMAT_HELP, type=int,
                            choices=settings.OUTPUT_FORMAT_CHOICES, default=settings.OUTPUT_FORMAT_DEFAULT)

        parser.add_argument('-c', '--classname', type=str, help=settings.CLASSNAME_HELP)

        # parsing actual arguments and return them to the caller.
        args = parser.parse_args()
        return args

    def set_collect_mode(self):
        """
        Read and set collect_mode ('s' or 't').
        :return: collect mode value
        """
        if self.args.collect_mode:
            if self.args.collect_mode in settings.COLLECT_MODE_CHOICES:
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
            search = [x for x in settings.LANGUAGES_AVAILABLE if x == ch]
            if len(search) > 0:
                return search[0]
            else:
                sys.exit("Wrong chapter, languages available are: " + str(settings.LANGUAGES_AVAILABLE))

    def set_source(self):
        """
        Read source and set research_type to identify which input type is selected.
        :return: source value
        """
        if self.args.source:
            return self.args.source.encode('utf-8')

    def set_output_format(self):
        """
        Read and set output organization. I will use a default value if user makes a mistake.
        :return: output organization value
        """
        if self.args.output_format:
            # check if output_format is correct
            if len(str(self.args.output_format)) == 1 and self.args.output_format <= 2:
                return self.args.output_format
            else:
                # use default output format if user wrote a wrong value
                print "Wrong output format value, used default: " + settings.OUTPUT_FORMAT_DEFAULT
                return settings.OUTPUT_FORMAT_DEFAULT

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
                return html_table_parser.all_tables, html_table_parser.tableStrList
            # if there aren't tables to analyze result will be empty
            else:
                return "", ""
        # if html doc is not defined result will be empty
        else:
            return "", ""

    def wiki_parser(self, res_name):
        wiki_parser = wikiParser.wikiParser(self.language, res_name, self.utils)
        resDict = wiki_parser.main_parser()

        return resDict

    def write_parse_info(self, all_resources_parse_info):

        with open('Resources/'+self.resource+'.txt', 'w') as outfile:
            json.dump(all_resources_parse_info, outfile, indent=4)

    def append_parse_info(self, all_resources_parse_info):

        with open('Resources/'+self.resource+'.txt', 'r+') as outfile:
            outfile.seek(0,2)
            position = outfile.tell() -1
            outfile.seek(position)
            for key, value in all_resources_parse_info.items():
                outfile.write( ",\n\t\"{res_name}\":\n\t{parse_info}\n".format(res_name=key, parse_info=json.dumps(value)))
            outfile.write("}")
