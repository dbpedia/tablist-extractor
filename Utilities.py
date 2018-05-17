# coding=utf-8

import urllib
import json
import time
import datetime
import lxml.html
import lxml.etree as etree
import os
import errno
import logging
import settings
import unicodedata
import sys
import socket

class Utilities:

	def __init__(self, language, resource, collect_mode):
		self.language = language
		self.resource = resource
		self.collect_mode = collect_mode

		# test if the directory ../Extracted exists (or create it)
		self.test_dir_existence('Extracted')

		self.setup_log("Explorer")
		self.extractor = False

		# define a log
		self.logging = logging
		# use dbpedia_selection to set self.dbpedia and self.dbpedia_sparql_url
		self.dbpedia_sparql_url = self.dbpedia_selection()

		# These values are used to compose calls to services as Sparql endpoints or to a html wiki page
		self.call_format_sparql = settings.SPARQL_CALL_FORMAT

		# Parameters used in methods which need internet connection
		self.time_to_attend = settings.SECONDS_BTW_TRIES  # seconds to sleep between two internet service call
		self.max_attempts = settings.MAX_ATTEMPTS  # max number of internet service' call tries

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

		# define timeout for url request in order to don't wait too much time
		socket.setdefaulttimeout(settings.REQUEST_TIMEOUT)

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
			filename = current_date_time + "_LOG_" + script_name + "_" + self.chapter + '_' + "custom" + ".log"
		else:
			filename = current_date_time + "_LOG_" + script_name + "_" + self.language + '_' + self.resource + ".log"
		# composing the absolute path of the log
		path_desired = self.join_paths(current_dir, 'Extracted/' + filename)

		# configuring logger
		logging.basicConfig(filename=path_desired, filemode='w', level=logging.DEBUG,
		                    format='%(levelname)-3s %(asctime)-4s %(message)s', datefmt='%m/%d %I:%M:%S %p')

		# brief stat at the beginning of log, it indicates the  wiki/dbpedia chapter and topic selected
		logging.info("You're analyzing wiki lists and tables of wiki chapter: " + self.language + ", source: " + self.resource)

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
		query = urllib.quote_plus(query)

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
		while attempts < settings.MAX_ATTEMPTS:
			try:
				# open a call with urllib.urlopen and passing the URL
				call = urllib.urlopen(url_passed)
				# read the answer
				answer = call.read()
				# decode the answer in json
				json_parsed = json.loads(answer)
				# return the answer parsed
				result = json_parsed
				return result
			except IOError:
				print ("Try, again, some problems due to Internet connection or empty url: " + url_passed)
				attempts += 1
				result = "Internet problems"
			except ValueError:
				# print ("Not a JSON object.")
				result = "ValueE"
				attempts += 1
			except:
				print "Exception with url:" + str(url_passed)
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
			print ("ERROR RETRIEVING RESOURCES FROM " + str(offset) + " TO " + str(offset + 1000))