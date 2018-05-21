# coding = utf-8

from collections import OrderedDict
from domain_explorer.ExplorerTools import ExplorerTools
__author__ = "sachinmalepati - Sachin Malepati (sachinmalepati@gmail.com)"

def start_exploration():
	"""
	Start domain exploration.
	It will take resources list and give in output a settings file organized
	like a dictionary ---> "Header name":"Ontology property associated"
	:return:
	"""

	# Read pyTableExtractor dictionary
	#actual_dictionary = explorer_tools.read_actual_dictionary()
	# Read uri resources
	uri_resource_list = explorer_tools.get_uri_resources()
	# If resources are found
	if uri_resource_list:
		# Analyze uri list
		analyze_uri_resource_list(uri_resource_list)
		# print report of extractor
		#explorer_tools.utils.print_report()
	else:
		print "No resources found. Please check arguments passed to pyDomainExplorer"

def analyze_uri_resource_list(uri_resource_list):
	"""
	Analyze each resource's uri to get sections and headers of related table.
	:param uri_resource_list: list of all resource's uri
	:param actual_dictionary: mapping rules defined in pyTableExtractor dictionary
	:return:
	"""
	total_resources = len(uri_resource_list)
	for single_uri in uri_resource_list:
		print "Resource: ", single_uri
		# update number of resources analyzed
		explorer_tools.utils.res_analyzed += 1
		# progress bar to warn user about how many resources have been analyzed
		explorer_tools.print_progress_bar(explorer_tools.utils.res_analyzed, total_resources)
		# get section and headers
		get_resource_sections_and_headers(single_uri)
		# get titles and list contents
		get_titles_and_list_contents(single_uri)

def get_resource_sections_and_headers(res_name):
	"""
	If there are defined tables, I will analyze each of them.
	First of all I will study section's table, then I will go on headers' table.
	:param res_name: resource name that has to be analyzed
	:param actual_dictionary: mapping rules defined in pyTableExtractor dictionary
	:return:
	"""
	# Get all tables
	all_tables = explorer_tools.html_table_parser(res_name)

def get_titles_and_list_contents(res_name):
	resDict = explorer_tools.wiki_parser(res_name)

	print(resDict)

if __name__ == "__main__":
    # instantiate tools that are useful for domain exploration
    explorer_tools = ExplorerTools()
    start_exploration()
