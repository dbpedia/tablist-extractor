# coding=utf-8

#import urllib.request, urllib.parse, urllib.error
import urllib
from urllib.request import urlopen
from urllib.parse import *
from urllib.error import *
import json
import time
import datetime
import lxml.html
import lxml.etree as etree
import os
import errno
import logging
import staticValues
import unicodedata
import sys
import socket
from domain_extractor import MapperTools
from collections import OrderedDict

class Utilities:

    def __init__(self, language, resource, collect_mode, ui=False):

        self.language = language
        self.resource = resource
        self.collect_mode = collect_mode
        self.resource_file = None

        # test if the directory ../Extracted exists (or create it)
        self.test_dir_existence('Extracted')

        if ui:
            #for using utility functions in UI
            self.extractor = False
        elif not self.language:
            resource, language, collect_mode, resource_file, toExtractTables, toExtractLists = Utilities.read_parameters_research()
            self.resource = resource
            self.language = language
            self.collect_mode = collect_mode
            self.resource_file = resource_file
            self.toExtractTables = toExtractTables
            self.toExtractLists = toExtractLists
            self.setup_log("extractor")
            self.extractor = True   # utilities called by extractor, so i need to update mapping rules
            self.mapper = MapperTools.MapperTools(self)
        else:
            self.setup_log("explorer")
            self.extractor = False

        # define a log
        self.logging = logging
        # use dbpedia_selection to set self.dbpedia and self.dbpedia_sparql_url
        self.dbpedia_sparql_url = self.dbpedia_selection()

        # These values are used to compose calls to services as Sparql endpoints or to a html wiki page
        self.call_format_sparql = staticValues.SPARQL_CALL_FORMAT

        # Parameters used in methods which need internet connection
        self.time_to_attend = staticValues.SECONDS_BTW_TRIES  # seconds to sleep between two internet service call
        self.max_attempts = staticValues.MAX_ATTEMPTS  # max number of internet service' call tries

        # check if user has written a class that exists in dbpedia ontology
        if self.collect_mode == "a":
            self.check_dbpedia_class()

        # self.dbpedia is used to contain which dbpedia to use Eg. dbpedia.org
        if self.language == "en":
            self.dbpedia = "dbpedia.org"
        else:
            self.dbpedia = self.language + ".dbpedia.org"

        # Instancing a lxml HTMLParser with utf-8 encoding
        self.parser = etree.HTMLParser(encoding='utf-8')

        self.html_format = "https://" + self.language + ".wikipedia.org/wiki/"

        if self.extractor:
            self.dictionary = self.mapper.update_mapping_rules()

        # define timeout for url request in order to don't wait too much time
        socket.setdefaulttimeout(staticValues.REQUEST_TIMEOUT)

        # Variables used in final report, see print_report()
        self.res_analyzed = 0
        self.res_collected = 0
        self.data_extracted = 0
        # data to map, that doesn't represents sum or mean of previous value
        self.data_extracted_to_map = 0
        self.tot_tables = 0
        self.tot_tables_analyzed = 0
        self.rows_extracted = 0
        self.data_extraction_errors = 0
        self.not_resolved_header_errors = 0
        self.headers_errors = 0
        self.no_mapping_rule_errors_headers = 0
        self.no_mapping_rule_errors_section = 0
        self.mapped_cells = 0
        self.triples_row = 0  # number of triples created for table's rows

    def setup_log(self, script_name):
        """
        Initializes and creates log file containing info and statistics
        """
        # getting time and date
        current_date_time = self.get_date_time()

        # obtain the current directory
        current_dir = self.get_current_dir()
        # composing the log filename as current_date_and_time + _LOG_T_EXT + chapter_chosen + topic_chosen
        if self.collect_mode == "w":
            filename = current_date_time + "_LOG_" + script_name + "_" + self.language + '_' + "custom" + ".log"
        else:
            filename = current_date_time + "_LOG_" + script_name + "_" + self.language + "_" + self.resource + ".log"
        # composing the absolute path of the log
        path_desired = self.join_paths(current_dir, 'Extracted/' + filename)

        # configuring logger
        logging.basicConfig(filename=path_desired, filemode='w', level=logging.DEBUG,
                            format='%(levelname)-3s %(asctime)-4s %(message)s', datefmt='%m/%d %I:%M:%S %p')

        # brief stat at the beginning of log, it indicates the  wiki/dbpedia chapter and topic selected
        logging.info("You're analyzing wiki lists and tables of wiki chapter: " + self.language + ", source: " + self.resource)

    @staticmethod
    def read_parameters_research():
        """
        Read parameters defined in header of settings file
        :return: set all parameters of research
        """
        # i'm in table_extractor folder so i have to go up
        if os.path.exists(staticValues.FILE_PATH_DOMAIN_EXPLORED):
            from domain_explorer import domain_settings
            for name, val in domain_settings.__dict__.items():
                # read domain
                if name == staticValues.DOMAIN_TITLE:
                    resource = val
                # read language
                elif name == staticValues.CHAPTER:
                    language = val
                # read research type (-s -t or -w)
                elif name == staticValues.COLLECT_MODE:
                    collect_mode = val
                # read name of resource's file
                elif name == staticValues.RESOURCE_FILE:
                    resource_file = val
                # read if tables data are to be extracted or not
                elif name == staticValues.TABLES_INCLUDED:
                    toExtractTables = val
                # read if lists data are to be extracted or not
                elif name == staticValues.LISTS_INCLUDED:
                    toExtractLists = val
        else:
            sys.exit("File " + staticValues.FILE_PATH_DOMAIN_EXPLORED + " not found. You should run pyDomainExplorer.")

        return resource, language, collect_mode, resource_file, toExtractTables, toExtractLists

    def dbpedia_selection(self):
        """
        Method used to set self.dbpedia and to return the URL to the correct dbpedia sparql endpoint depending on the
        chapter (self.language) used.
        :return: URL to the correct dbpedia sparql endpoint.
        """
        if self.language != "en":
            self.dbpedia = self.language + ".dbpedia.org"
        else:
            self.dbpedia = "dbpedia.org"
        return "http://" + self.dbpedia + "/sparql?default-graph-uri=&query="

    def test_dir_existence(self, directory):
        """
        Test if directory exists
        :param directory: name of directory
        :return:
        """
        current_dir = self.get_current_dir()
        dir_abs_path = self.join_paths(current_dir, directory)
        if not os.path.exists(dir_abs_path):
            print('Folder doesn\'t exist, creating..')
            try:
                os.makedirs(dir_abs_path)
                print('done')
            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

    def get_current_dir(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        return cur_dir

    def join_paths(self, path1, path2):
        destination = os.path.join(path1, path2)
        return destination

    def get_date_time(self):
        """
        It returns current YEAR_MONTH_DAY_HOUR_MINUTES as a string
        """
        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y_%m_%d-%H_%M')
        return date

    def get_date(self):
        """
        It returns current YEAR_MONTH_DAY as a string
        """
        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y_%m_%d')
        return date

    def check_dbpedia_class(self):
        """
        Check if user has written a class that is in dbpedia ontology
        :return: nothing
        """
        # uri of class
        class_uri = "http://dbpedia.org/ontology/" + self.resource
        result = self.ask_if_resource_exists(class_uri)
        if not result:
            sys.exit("Class " + self.topic + " defined in arguments doesn't exist in DBpedia ontology")

    def ask_if_resource_exists(self, resource):
        """
        This method asks to a dbpedia sparql endpoint if a resource exists or not.
        This is useful to compose the new dataset, so that it can be coherent with the DBpedia RDF dataset.

        :param resource: is the resource which existence you want to test
                        Eg.  Elezioni_presidenziali_negli_Stati_Uniti_d'America_del_1789 (it chapter) or
                             Bavarian_state_election,_2013 (en chapter)
        :return: response (true if the resource exists in the dataset, false otherwise)
        """
        try:
            query = "ASK { <" + resource + "> ?p ?o }"
            ask_url = self.url_composer(query, 'dbpedia')
            answer = self.json_answer_getter(ask_url)
            if "boolean" in answer:
                response = answer["boolean"]
                return response
            else:
                return False
        except:
            # print("Exception asking if %s exists" % resource)
            return False

    def url_composer(self, query, service):
        """
        This function is used to compose a url to call some web services, such as sparql endpoints.

        :param query: is the string used in some rest calls.
        :param service: type of service you request (dbpedia sparql endpoint)
        :return url: the url composed
        """
        # use quote_plus method from urllib to encode special character (must to do with web service)
        query = quote_plus(query)

        """
        The following if clause are differentiated by service requested Eg. 'dbpedia',..
            but in all the cases url is composed using pre formatted string along with the query
        """
        if service == 'dbpedia':
            url = self.dbpedia_sparql_url + query + self.call_format_sparql

        elif service == 'html':
            url = self.html_format + query

        else:
            url = "ERROR"
        return url

    def json_answer_getter(self, url_passed):
        """
        json_answer_getter is a method used to call a web service and to parse the answer in json.
        It returns a json parsed answer if everything is ok
        :param url_passed: type string,is the url to reach for a rest service
        :return json_parsed: the method returns the JSON parsed answer
        """
        attempts = 0
        result = ""
        while attempts < staticValues.MAX_ATTEMPTS:
            try:
                # open a call with urllib.urlopen and passing the URL
                with urllib.request.urlopen(url_passed) as call:
                #call = urllib.request.urlopen(url_passed)
                # read the answer
                    answer = call.read()
                # decode the answer in json
                json_parsed = json.loads(answer)
                # return the answer parsed
                result = json_parsed
                return result
            except IOError:
                print("Try, again, some problems due to Internet connection or empty url: " + url_passed)
                attempts += 1
                result = "Internet problems"
            except ValueError:
                # print ("Not a JSON object.")
                result = "ValueE"
                attempts += 1
            except:
                print("Exception with url:" + str(url_passed))
                result = "GeneralE"
                attempts += 1
        return result

    def tot_res_interested(self, query):
        """
        Method used to retrieve the total number of resources (wiki pages) interested.
        It uses url_composer passing by the query to get the number of res.
        Then it sets tot_res as the response of a call to dbpedia sparql endpoint.
        Last it sets the local instance of total_res_found.
        :return nothing
        """
        try:
            url_composed = self.url_composer(query, 'dbpedia')
            json_answer = self.json_answer_getter(url_composed)
            tot_res = json_answer['results']['bindings'][0]['res_num']['value']
            total_res_found = int(tot_res)
            return total_res_found
        except:
            logging.exception("Unable to find the total number of resource involved..")
            return 0

    def dbpedia_res_list(self, query, offset):
        """
        This method retrieve a list of 1000 resources using a SPARQL query.
        It composes the URL to be called, and then retrieve the JSON answer.
        Finally returns the result

        :param query: SPARQL query
        Eg. 'SELECT distinct ?s as ?res WHERE{?s a <http://dbpedia.org/ontology/Election>} LIMIT 1000 OFFSET '
        :param offset: is the offset served to sparql service in order to get res from "offset" to "offset"+1000
        :return: res_list is a list of resources, typically 1000 resources
        """
        try:
            # composing the url with the help of url_composer and passing the offset, along with the service required
            url_res_list = self.url_composer(query + str(offset), 'dbpedia')
            # call to the web service with json_answer_getter(url_res_list) and obtain a json answer
            answer = self.json_answer_getter(url_res_list)
            # the actual res_list resides in answer['results']['bindings']
            res_list = answer['results']['bindings']
            return res_list
        except:
            logging.info("Lost resources with this offset range: " + str(offset) + " / " + str(offset + 1000))
            print("ERROR RETRIEVING RESOURCES FROM " + str(offset) + " TO " + str(offset + 1000))

    def print_progress_bar(self, iteration, total, prefix='Progress: ', suffix='Complete', decimals=1, length=30,
                            fill='#'):
        """
        Call in a loop to create terminal progress bar
        @params:
            iteration   - Required  : current iteration (Int)
            total       - Required  : total iterations (Int)
            prefix      - Optional  : prefix string (Str)
            suffix      - Optional  : suffix string (Str)
            decimals    - Optional  : positive number of decimals in percent complete (Int)
            length      - Optional  : character length of bar (Int)
            fill        - Optional  : bar fill character (Str)
        """
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filled_length = int(length * iteration // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))

    def html_answer(self, url_passed):
        """
        Open url passed to method
        :param url_passed: url to analyze
        :return: html document of that url
        """
        try:
            call = urlopen(url_passed)
            html_document = lxml.html.parse(call, self.parser)
            #print(etree.tostring(html_document,pretty_print=True))
            return html_document
        except IOError:
            print("Try, again, some problems due to Internet connection, url: " + url_passed)

            return "Internet Error"
        except ValueError:
            print ("Not a HTML object.")
            return "Value Error"
        except:
            print("Exception with url:" + str(url_passed))
            return "General Error"

    def html_object_getter(self, resource):
        """
        Get html object of resource given in input
        :param resource: resource to transform in html
        :return: resource in html
        """
        html_url = self.url_composer(resource, 'html')
        is_answer_ok = False
        attempts = 0
        html_answer = None

        while is_answer_ok is not True and attempts < self.max_attempts:
            try:
                attempts += 1
                html_answer = self.html_answer(html_url)
                if type(html_answer) != str:
                    is_answer_ok = self.test_html_result(html_answer)
                else:
                    time.sleep(self.time_to_attend)
            except:
                print("Error trying to get html object")

        if is_answer_ok:
            print("Html document well formed..")
        else:
            print("Error trying to get html object : %s" % html_answer)
            html_answer = None
        return html_answer

    def test_html_result(self, html_doc):
        """
        Test if html document created is well-formed
        :param html_doc: html document to test
        :return:
            - True if html_doc is well-formed
            - False otherwise.
        """
        if type(html_doc) == str and "Error" in html_doc:
            return False
        else:
            return True

    def delete_accented_characters(self, text):
        """
        Method used to delete all accented characters from the name of resource.
        It takes in input one string called text and gives in output another string that doesn't have accented
        characters that it's similar to the previous form.
        :param text: string where you have to delete accented charactes
        :return:
        """
        try:
            text = str(text, "utf-8")
            #result = unicodedata.normalize('NFD', text).encode('ascii', 'ignore')
            result = unicodedata.normalize('NFD', text)
            return result
        except TypeError:
            return text

    def clean_dictionary(self, language, listDict) :
        ''' Deletes all entries with an empty values, thus 'cleaning' the dictionary.

        :param listDict: dictionary obtained from parsing.

        :return: a dictionary without empty values.
        '''
        for key in list(listDict.keys()) :
            if listDict[key] == '' :
                listDict.pop(key)
            #if key in EXCLUDED_SECTIONS[language]:  #remove excluded sections
            #	listDict.pop(key)
            else:
                listDict[key] = self.remove_symbols(listDict[key])

        return listDict


    def remove_symbols(self, listDict_key):
        ''' removes other sybols are garbage characters that pollute the values to be inserted .

        :param listDict_key: dictionary entries(values) obtained from parsing.

        :return: a dictionary without empty values.
        '''
        for i in range(len(listDict_key)):
            value = listDict_key[i]
            if type(value)==list:   #handle recursive list elements
                value=self.remove_symbols(value)
            else: #replace this symbol from list values; as it broke the code in some cases
                listDict_key[i] = value.replace('&nbsp;','')
        return listDict_key

    def json_req(self, req):
        ''' Performs a request to an online service and returns the answer in JSON.

        :param req: URL representing the request.

        :return: a JSON representation of data obtained from a call to an online service.
        '''
        try:
            call = urlopen(req)
            answer = call.read()
            json_ans = json.loads(answer)
            return json_ans
        except:
            err = str(sys.exc_info()[0])
            print("Error: " + err + " - on request " + req)
            raise

    @staticmethod
    def load_settings():
        ''' This function loads the mapping rules from the settngs.json file into ``MAPPING`` dict.

        :return: latest ``MAPPING`` dict.
        '''
        try:
            with open('configs.json') as settings_file:
                #global MAPPING
                settings = json.load(settings_file)  #load settings from file into the dict
                MAPPING = settings['MAPPING']
                return MAPPING
        except IOError:
            print("Settings files doesn't exist!!! ")
            sys.exit(1)

    @staticmethod
    def load_custom_mappers():
        ''' This function loads the user defined mapping functions from the ``custom_mappers.json``
        file into ``CUSTOM_MAPPERS`` dict.

        :return: Custom mapper function settings dict.
        '''
        try:
            with open('custom_mappers.json') as custom_mappers:
                #global CUSTOM_MAPPERS
                CUSTOM_MAPPERS = json.load(custom_mappers, object_pairs_hook=OrderedDict)  #load mappers from file into the dict
                return CUSTOM_MAPPERS
        except IOError:
            print("Custom mappers not found!")
            return dict()  #in case of failure, assume no user defined mappers and return empty dict

    def get_list_section_ontology_class(self, sect_name, mapper, CUSTOM_MAPPERS):
        """
        Get the corresponding ontology property for a word.

        :param sect_name: list section name
        :param mapper: mapper to be searched for
        :param CUSTOM_MAPPERS: dictionary
        :return: ontology value of a given word
        """
        ontology_class = None
        for class_type in CUSTOM_MAPPERS[mapper]["ontology"][self.language]:
            try:
                #find a matching sub-section from the ontology class
                if class_type.lower() in sect_name.lower():
                    ontology_class = class_type
            except UnicodeEncodeError:
                break

        if ontology_class == None:   #No possible mapping found; try default mapping
            if "default" in CUSTOM_MAPPERS[mapper]["ontology"][self.language]:
                if CUSTOM_MAPPERS[mapper]["ontology"][self.language]["default"] == "None":
                    return 0 #default wasn't allowed
                else:
                    ontology_class = "default"
            else:
                return 0
        
        return ontology_class

    def validate_user_input(self):
        """
        Verify each option of domain_settings file created. I have to notify user if he wrote something wrong in settings
        file's header
        :return: string that can be
            - 'valid_input' if it's all right
            - message that depend on type of error
        """
        result = "valid_input"
        # check chapter
        if len(self.language) != 2:
            result = "Chapter (" + self.language + ") is wrong, check domain_settings.py"
        # check research type
        if len(self.collect_mode) == 1:
            if self.collect_mode != "t" and self.collect_mode != "s" :
                result = "Research type (" + self.collect_mode + ") is wrong, check domain_settings.py"
        else:
            result = "Research type (" + self.collect_mode + ") is wrong, check domain_settings.py"
        # check resource file
        if self.collect_mode != "s" and not os.path.isfile(self.get_resource_file()):
            result = "Resource file doesn't exists, check domain_settings.py"
        return result

    def get_resource_file(self):
        """
        :return: resource file
        """
        return staticValues.PATH_FOLDER_RESOURCE_LIST + "/" + self.resource_file

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

        enc_query = quote_plus(query)
        endpoint_url = "http://" + local + "dbpedia.org/sparql?default-graph-uri=&query=" + enc_query + \
                       "&format=application%2Fsparql-results%2Bjson&debug=on"
        json_result = self.json_req(endpoint_url)
        return json_result

    def count_listelem_dict(self, res_dict):
        ''' Counts the total number of list elements from the dictionary representing the Wikipedia page.\
        It's used to know how many list elements in a page are actually extracted.

        :param res_dict: dictionary representing the resource (Wikipedia page).

        :return: total list elements.
        '''
        list_el_num = 0
        for k in list(res_dict.keys()):
            for el in res_dict[k]:
                list_el_num += 1
        return list_el_num

    def evaluate(self, lang, source, tot_res, tot_res_success, tot_extracted_elems, tot_elems, num_statements):
        ''' Evaluates the extaction process and stores it in a csv file.

        :param source: resource type(dbpedia ontology type).
        :param tot_extracted_elems: number of list elements extracted in the resources.
        :param tot_elems: total number of list elements present in the resources.

        :return: void.
        '''
        try:
            print("\nEvaluation:\n===========\n")
            print("Resource Type:", lang + ":" + source)
            print("Resources Found:", tot_res)
            print("Resources successfully processed:", tot_res_success)
            print("List elements found:", tot_elems)
            print("List elements extracted:", tot_extracted_elems)
            print("Triples Created:", num_statements)
            accuracy = (1.0*tot_extracted_elems)/tot_elems
            print("Accuracy:", accuracy)
            print("")

            #write the evaluation results in evaluation.csv
            with open('evaluation.csv', 'a') as csvfile:
                filewriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                filewriter.writerow([lang, source, tot_res, tot_res_success, tot_extracted_elems, tot_elems,
                                        num_statements, accuracy])
        except ZeroDivisionError:
            print('\nNo elements extracted!')