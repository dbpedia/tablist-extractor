import argparse
import sys
import rdflib
from collections import OrderedDict
import settings


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
        if self.args.collect_mode:
            if self.args.collect_mode in settings.COLLECT_MODE_CHOICES:
                return self.args.collect_mode
            else:
                sys.exit("Wrong collect_mode, available collect_mode are: "+sstr(ettings.COLLECT_MODE_CHOICES))

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

        if self.args.classname:
            return self.args.classname
        else:
            return None
