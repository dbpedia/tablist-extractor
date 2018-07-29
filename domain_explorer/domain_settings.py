# coding:utf-8 

# Comments below will help you in filling this file settings. Remember to change only dictionary values.
# Please do not modify DomainExplorer parameters. 

# DomainExplorer parameters 
DOMAIN_EXPLORED = "William_Gibson" 
CHAPTER = "en" 
COLLECT_MODE = "s" 
TABLES_INCLUDED ="false" 
LISTS_INCLUDED ="true" 
RESOURCE_FILE = "" 

# Writing mapping rules is simple --> you have to fill all empty fields remembering this structure:
# 'table's header / list's section':'ontology property' (Example:  'year':'Year', 'GP':'gamesPlayed','High school name':'nameSchool'). 

# Elements which are already depicts that they have already been found in the common dictionary
# or on dbpedia ontology.
# If you empty a field that was filled, you will delete that rule from dictionary.


#Following are section mappings of lists found:
#Mapper used for the following are: BIBLIOGRAPHY_MAPPER

WILLIAM_GIBSON___BIBLIOGRAPHY_MAPPER___LISTS = {
'Selected bibliography - Short stories': 'ShortStory', 
'Selected bibliography - Novels': 'Novel', 
'Nonfiction': 'Nonfiction', 
} 

# END OF FILE 
