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

if __name__ == "__main__":
    # instantiate tools that are useful for domain exploration
    explorer_tools = ExplorerTools()
    start_exploration()
