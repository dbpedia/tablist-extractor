# coding = utf-8
import string
from collections import OrderedDict
from domain_explorer.ExplorerTools import ExplorerTools
from domain_explorer import WriteSettingsFile
import staticValues
import re

# All table's section found
all_sections = {}
# All headers found in tables analyzed
all_headers = {}
# All sections of lists found
all_list_sections = {}

def start_exploration():
    """
    Start domain exploration.
    It will take resources list and give in output a settings file organized
    like a dictionary ---> "Header name":"Ontology property associated"
    :return:
    """

    # Read uri resources
    uri_resource_list = explorer_tools.get_uri_resources()

    # If resources are found
    if uri_resource_list:
        # Analyze uri list
        analyze_uri_resource_list(uri_resource_list)

        write_sections_and_headers()
        # print report of extractor
        explorer_tools.utils.print_report()
    else:
        print("No resources found. Please check arguments passed to pyDomainExplorer")

def analyze_uri_resource_list(uri_resource_list):
    """
    Analyze each resource's uri to get sections and headers of related table/lists.
    :param uri_resource_list: list of all resource's uri
    :return:
    """
    total_resources = len(uri_resource_list)
    offset = 0

    for single_uri in uri_resource_list:
        print("Resource: ", single_uri)
        # check if tables data are to be extracted or not
        if explorer_tools.toExtractTables == "true":
            # get section and headers
            all_tables = get_resource_sections_and_headers(single_uri)
        else:
            all_tables=[]

        # check if lists data are to be extracted or not
        if explorer_tools.toExtractLists == "true":
            # get titles and list contents
            resDict = get_titles_and_list_contents(single_uri)
        else:
            resDict=[]

        # update number of resources analyzed
        explorer_tools.utils.res_analyzed += 1
        # progress bar to warn user about how many resources have been analyzed
        explorer_tools.print_progress_bar(explorer_tools.utils.res_analyzed, total_resources)
        # get table headers/sections and lists sections ontology mappings
        collect_table_and_list_ontology_mappings(all_tables, resDict, single_uri)

def get_resource_sections_and_headers(res_name):
    """
    Get all the tables information of that particular resource
    :param res_name: resource name that has to be analyzed
    :return: tables data from html table parser
    """
    # Get all tables
    all_tables = explorer_tools.html_table_parser(res_name)

    return all_tables

def collect_table_and_list_ontology_mappings(all_tables, resDict, single_uri):
    """
    Get ontology mappings of both lists and tables sections/headers to
    write them into a domain_settings.py file.
    :param all_tables: contains all the tables information
    :param resDict: list dictinoary from wikiParser
    :param single_uri: resource name that has to be analyzed
    :return:
    """

    # Obtain resource types associated with each resource
    if explorer_tools.collect_mode == 's':
        rdf_types = explorer_tools.get_resource_type(single_uri)
    else:
        rdf_types = [explorer_tools.resource]

    # Load configs.json file
    domains = explorer_tools.utils.load_settings()
    # Load custom_mappers.json file
    CUSTOM_MAPPERS = explorer_tools.utils.load_custom_mappers()

    if explorer_tools.toExtractTables == "true":
        # Get ontology mappings of tables headers/sections
        collect_table_sections_and_headers_mappings(all_tables, single_uri, rdf_types, domains, CUSTOM_MAPPERS)

    if explorer_tools.toExtractLists == "true":
        # Get ontology mappings of lists headers/sections
        collect_list_section_mappings(resDict, single_uri, rdf_types, domains, CUSTOM_MAPPERS)

def collect_table_sections_and_headers_mappings(all_tables, res_name, rdf_types, domains, CUSTOM_MAPPERS):
    """
    First, get all the mappers associated with that resource/domain.
    For each table in all_tables, get ontology mappings of each section/header with
    the help of their associated mappers.
    :param all_tables: contains all the tables information
    :param res_name: name of the resource
    :param rdf_types: associated rdf types with that resource
    :param domains: associated domains with that resource
    :param CUSTOM_MAPPERS: mappers present in custom_mappers.json
    :return:
    """
    mappers=[]
    mapped_domains=[]

    # Get mappers associated with resource domains.
    for rdf_type in rdf_types:
        if rdf_type in list(domains.keys()):
            mappers += domains[rdf_type]

    for mapper in mappers:
        if mapper not in mapped_domains:
            # table's section found
            table_sections = OrderedDict()
            # headers found in tables analyzed
            table_headers = OrderedDict()

            # For each table defined
            for table in all_tables:
                if table:
                    if mapper in CUSTOM_MAPPERS and table.table_section in CUSTOM_MAPPERS[mapper]["table_sections"][explorer_tools.language]:
                        actual_dictionary = CUSTOM_MAPPERS[mapper]["ontology"][explorer_tools.language]
                        # I won't get tables with only one row --> It can be an error during table's reading
                        if table.n_rows > 1:
                            check_if_section_is_present(table.table_section, table.headers_refined, res_name, actual_dictionary, table_sections, table_headers)

            if table_sections and table_headers:
                all_sections[res_name.translate(str.maketrans('', '', string.punctuation)).upper()+"___"+mapper] = table_sections
                all_headers[res_name.translate(str.maketrans('', '', string.punctuation)).upper()+"___"+mapper] = table_headers

            mapped_domains.append(mapper)

def check_if_section_is_present(string_to_check, headers_refined, res_name, actual_dictionary, table_sections, table_headers):
    """
    Check if section is already presents in all_sections dictionary.
    I do this in order to create a dictionary that group similar section.
    Think that this action will help user in filling all fields
    :param string_to_check: section name to check
    :param headers_refined: all headers of this sections (JSON object that contains properties like 'colspan', etc..)
    :param res_name: resource name that has to be analyzed
    :param actual_dictionary: mapping rules defined in pyTableExtractor dictionary
    :param table_sections: all table sections found
    :param table_headers: all table headers found
    :return:
    """
    # get section name of resource (that can be a single value or grouped and so separated by _tte_
    section_name = check_if_similar_section_is_present(string_to_check, res_name, actual_dictionary, table_sections, table_headers)
    # Check if this section was already created, if not it will create another dictionary
    check_if_headers_not_present_then_add(headers_refined, section_name, actual_dictionary, table_sections, table_headers)

def check_if_similar_section_is_present(string_to_check, res_name, actual_dictionary, table_sections, table_headers):
    """
    Check if there are sections that are similar.
    (For example 'College' and 'College statistics' will be joint in one unique section to map)
    :param string_to_check: section name to check
    :param res_name: resource name that has to be analyzed
    :param actual_dictionary: mapping rules defined in pyTableExtractor dictionary
    :param table_sections: all table sections found
    :param table_headers: all table headers found
    :return: section name that can be:
                - already defined in all_sections dictionary.
                - same as before.
                - joint with others sections that has similar name.
    Note:
    Each section will be separated by a unique group of characters, defined in settings.py file. (now is _tte_)
    """
    # Get all_sections
    keys = list(table_sections.keys())
    new_key = string_to_check
    # similar key
    similar_key = [key for key in keys if string_to_check.lower() in key.lower() or key.lower()
                   in string_to_check.lower()]
    # key that is equal to that passed
    equal_key = search_equal_key(keys, string_to_check)
    # if there isn't an equal key, I have to search on similar key
    if not equal_key:
        # if there is a similar key I have to create another key that contains current key.
        # I have also to delete previous key value in favour of the new key.
        if similar_key:
            # crete new key
            new_key = similar_key[0] + staticValues.CHARACTER_SEPARATOR + string_to_check
            # delete previous dictionary and create a new one with this new key
            app_dict = dict(table_sections[similar_key[0]])
            del table_sections[similar_key[0]]
            table_sections[new_key] = OrderedDict()
            # search if this new_key is defined in actual_dictionary
            if new_key in actual_dictionary:
                table_sections[new_key].__setitem__(staticValues.SECTION_NAME_PROPERTY, actual_dictionary[new_key])
            else:
                table_sections[new_key].__setitem__(staticValues.SECTION_NAME_PROPERTY, "")
            table_sections[new_key].update(app_dict)
        # If there isn't similar key, I simply create a new one in all_sections dictionary.
        else:
            table_sections[new_key] = OrderedDict()
            # search if this new_key is defined in actual_dictionary
            section_rule = "" + new_key
            if section_rule in actual_dictionary:
                table_sections[new_key].__setitem__(staticValues.SECTION_NAME_PROPERTY, actual_dictionary[section_rule])
            else:
                table_sections[new_key].__setitem__(staticValues.SECTION_NAME_PROPERTY, "")
            # example of wiki pages where i found a particular section
            table_sections[new_key].__setitem__("exampleWiki", res_name)
    else:
        new_key = equal_key
        # check if there is already an example page of wikipedia and i want at most NUMBER_OF_WIKI_EXAMPLES examples
        if "exampleWiki" in table_sections[new_key] and len(table_sections[new_key]["exampleWiki"].split(",")) <\
                staticValues.NUMBER_OF_WIKI_EXAMPLES:
            old_example = table_sections[new_key]["exampleWiki"]
            table_sections[new_key].__setitem__("exampleWiki", old_example + ", " + res_name)
    return new_key


def check_if_headers_not_present_then_add(headers, section_name, actual_dictionary, table_sections, table_headers):
    """
    Check if headers passed are already defined in the section that you are analyzing.

    :param headers: all table's headers
    :param section_name: section name to analyze
    :param actual_dictionary: mapping rules defined in pyTableExtractor dictionary
    :return:
    """
    #
    for row in headers:
        header = row['th']
        # character "'" will produce a wrong output file
        header = header.replace("'", "")
        # search for equal header
        check_if_header_already_exists(header, section_name, actual_dictionary, table_sections, table_headers)


def check_if_header_already_exists(header, section_name, actual_dictionary, table_sections, table_headers):
    """
    Check if section contains this header.
    :param header: single table header
    :param section_name: section name to analyze
    :param actual_dictionary: mapping rules defined in pyTableExtractor dictionary
    :return:
    """
    if header not in table_sections[section_name]:
            # check if this header is already defined in actual_dictionary
        if (section_name + "_" + header) in actual_dictionary:
            # if it's associated to section (depend on output format value)
            header_property = actual_dictionary[section_name + "_" + header]
        elif header in actual_dictionary:
            # if it's not related to section
            header_property = actual_dictionary[header]
        else:
            # check if it's already defined a property for this header on dbpedia
            header_property = check_if_property_exists(header, table_sections, table_headers)

        table_sections[section_name].__setitem__(header, header_property)
        # verify if in all_headers is already defined
        if header not in table_headers:
            table_headers.__setitem__(header, header_property)
            #explorer_tools.print_log_msg("info", "New header found: " + header)


def check_if_property_exists(header, table_sections, table_headers):
    """
    Query dbpedia endpoint in order to search if a particular property is defined.
    This method search if in dbpedia ontology there is a property that has a label (in chapter language)
    that has same name of header's table.
    This will be useful for user so that filling settings file will be easier.
    :param header: property to check
    :return:
    """
    property_to_check = ""
    # check if it's already defined
    if header in table_headers:
        property_to_check = table_headers[header]
    else:
        answer = explorer_tools.make_sparql_dbpedia("check_property", header)
        # if answer contains something useful
        if not isinstance(answer, str):
            property_found = 0
            for row in answer["results"]["bindings"]:
                # sparql results can be wikidata or dbpedia uri, i have to filter to catch only dbpedia ontology uri
                for property_type in staticValues.ONTOLOGY_TYPE:
                    if property_type in row["s"]["value"] and property_found == 0:
                        property_to_check = explorer_tools.get_ontology_name_from_uri(row["s"]["value"])
                        property_found = 1
    return property_to_check


def search_equal_key(array_string, string_to_check):
    """
    Method to search over a string list to check if a particular string is equal to
    an element of this list.

    :param array_string: string list
    :param string_to_check:  string to check if there is an equal in string list
    :return: result can be:
                - empty -> there isn't an equal key.
                - equal key found.
    """
    result = ""
    for string in array_string:
        # split by _tte_ to get each sections
        keys = string.split(staticValues.CHARACTER_SEPARATOR)
        for key in keys:
            if key == string_to_check:
                result = string
    return result

def get_titles_and_list_contents(res_name):
    """
    Method to get lists content from wikipedia pages.

    :param res_name: name of resource
    :return: dictionary containing all lists contents found in the wiki page.
    """
    resDict = explorer_tools.wiki_parser(res_name)

    return resDict

def collect_list_section_mappings(resDict, res_name, rdf_types, domains, CUSTOM_MAPPERS):
    """
    Method to get ontology mappings of lists sections found.

    :param resDict: dictionary of lists content of that resource
    :param res_name: name of resource
    :param rdf_types: rdf types associated with the resource
    :param domains: domains associated with the resource
    :param CUSTOM_MAPPERS: mappers present in custom_mappers.json
    :return: dictionary containing all lists contents found in the wiki page.
    """
    mappers=[]
    mapped_domains=[]

    print('List sections found: ' + str(resDict.keys()))

    for rdf_type in rdf_types:
        if rdf_type in list(domains.keys()):
            mappers+=domains[rdf_type]

    for mapper in mappers:
        if mapper not in mapped_domains and mapper in list(CUSTOM_MAPPERS.keys()):
            list_sections = OrderedDict()
            domain_keys = CUSTOM_MAPPERS[mapper]["list_headers"][explorer_tools.language]

            for res_key in list(resDict.keys()):
                mapped = False
                for dk in domain_keys:
                    if not mapped and re.search(dk, res_key, re.IGNORECASE):
                        ontology_class = explorer_tools.utils.get_list_section_ontology_class(res_key, mapper, CUSTOM_MAPPERS)
                        if ontology_class:
                            ontology_property = CUSTOM_MAPPERS[mapper]["ontology"][explorer_tools.language][ontology_class]
                            list_sections.__setitem__(ontology_class, ontology_property)
                            mapped = True
                        else:
                            list_sections.__setitem__(res_key, "")
                            mapped = True

            if list_sections:
                all_list_sections[res_name.translate(str.maketrans('', '', string.punctuation)).upper()+"___"+mapper] = list_sections

            mapped_domains.append(mapper)

def write_sections_and_headers():
    """
    Write sections and headers found. I will use WriteSettingsFile to create output file.
    :return:
    """
    # write output file
    WriteSettingsFile.WriteSettingsFile(all_sections, all_headers, all_list_sections, explorer_tools)

if __name__ == "__main__":
    # instantiate tools that are useful for domain exploration
    explorer_tools = ExplorerTools()
    start_exploration()
