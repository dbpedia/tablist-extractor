# coding=utf-8

import sys
import rdflib
from domain_explorer import HtmlTableParser

__author__ = 'papalinis - Simone Papalini - papalini.simone.an@gmail.com'


class Analyzer:
    """
    Analyzer class takes resources from a list and call a HtmlTableParser  over them.

    It takes resources from .txt file (generally created by Selector objects) or from a string if a single_resource is
     involved.
    Therefore a Table Parser object is called over their wiki page representation.
     This representation is retrieved by a utilities object (calling html_object_getter()).
    Once the list of resources is finished or the analysis of a resource is done some useful statistics values are set.
    Some of them are passed to the utilities object (res_analyzed), as they are useful to print a final cumulative
     report, while some others (headers with no mapping rules found) are just print out and to the log.
    They are used to give to the user an idea of which headers he can find in tables but which has not yet a
     corresponding mapping rule. This is so important, as tables in wiki pages (even in pages with same topic
     or describing the same phenomenons) are as well heterogeneous as the taste of users who wrote them.

    Public Methods:
        -analyze(): it is used to analyze a list of resources(or a single resource) passed once analyzer has been
            initialized. Once you have created Analyzer object simply call this method to begin the analysis.
            This method doesn't return nothing by itself as useful informations are printed out both in the log and
            in the console.

        -serialize(): method used to serialize the RDF graph fulfilled with triples during analysis (mapping) phase.
            it creates a .ttl file (serialization of the RDF graph).
            Filename and directory (it should be /Extractions) are reported in the log.
            Please call serialize() after analyze() method!
    """

    def __init__(self, language, resource, utils, filename=None, single_res=None):
        """
        Analyzer object takes resources from a list and call a TableParser (html |json) over them.

        Please, after initialization, use the analyze() method to start the analysis and the serialize() one to
         serialize the RDF graph.
        During the initialization a rdf graph is created (the class need rdflib to work) and a iterator is set over the
         list of resources or over the single_resource passed.

        Arguments:
        :param chapter (str): a two alpha-characters string representing the chapter of wikipedia user chose.
        :param topic (str): a string representing the common topic of the resources considered.
        :param utils (Utilities object): utilities object used to access common log and to set statistics values used to
                print a final report.
        :param filename (str): DEFAULT:None filename of a resources' list. It should be a .txt file containing name
            of wiki pages (with spaces replaced by underscores Eg. Elezioni_amministrative_italiane_del_2016).
            Note that filename is mutual exclusive with single_res (if one is set, the other should not)
        :param single_res (str): DEFAULT:None string with a single resource name, as for list of resources file,
            the name should have spaces replaced by underscores Eg. Elezioni_amministrative_italiane_del_2016
            Note that single_res is mutual exclusive with filename (if one is set, the other should not)

        """
        # parameters are registered in the object
        self.language = language
        self.resource = resource
        self.utils = utils
        self.logging = self.utils.logging  # just for reading comfort
        self.filename = filename
        self.single_res = single_res

        # These values are used to statistics purposes
        self.res_analyzed = 0  # number of resources correctly analyzed
        self.total_table_num = 0  # Extraction tables number

        self.res_list = None

        # setup a list of resources  from the file (filename) passed to __init__
        if self.filename:
                self.open_stream()
        else:
            # if self.filename == None, the single_res should be set, so use a iterator over it.
            self.res_iterator = iter([self.single_res])

        # boolean value to check if others lines are in the list file
        self.lines_to_read = True

        # Set a RDF graph, using rdflib. Ensure to have rdflib installed!
        self.graph = rdflib.Graph()

    def open_file(self):
        """
        open_file is used to open a input stream from a file.
        Filename has to be set in self.filename, and the file should exists or an IOError Exception is raised.
        :return: the function returns lines from the file opened.
        """
        try:
            # open file in read mode
            file_opened = open(self.filename, 'r')
            return file_opened.readlines()
        except IOError:
            print "IOError opening the file: " + str(self.filename)

    def setup_iterator(self):
        """
        setup_iterator tries to make a iterable object from self.res_list.

        Note: res_list should be set to a list of string (use open_file() method)
        :return:
        """
        try:
            res_iterator = iter(self.res_list)
            return res_iterator
        except TypeError:
            print "Check file's existence. "
            sys.exit(0)

    def open_stream(self):
        """
        open_stream() is used to set res_list (with a stream coming from file) and a res_iterator (see setup_iterator())

        If filename is set, setup res_list with a input stream coming from file (filename) and res_iterator with
         setup_iterator().
        :return: nothing
        """
        if self.filename:
            # set lines to be read
            self.res_list = self.open_file()
            # set the iterator from that self.res_list
            self.res_iterator = self.setup_iterator()
        else:
            print " File name not set, please check it. "
            sys.exit(0)

    def get_filename(self):
        """
        It returns the filename set to this analyzer.
        It is intended to be a txt file with a list of wiki resources divided by newline tag.
        :return: filename
        """
        return self.filename
