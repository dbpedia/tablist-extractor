# coding:utf-8 

# Comments below will help you in filling this file settings. Remember to change only SECTION_ variables.
# Please do not modify pyDomainExplorer parameters. 

# pyDomainExplorer parameters 
DOMAIN_EXPLORED = "Kobe_Bryant" 
CHAPTER = "en" 
COLLECT_MODE = "s" 
RESOURCE_FILE = "" 

# The entry named sectionProperty represents ontology property associated to table's section.
# (Eg. in basket domain, section named playoff can be mapped with something like 'playoff' or  'playoffMatch').
# Triple example: <http://dbpedia.org/resource/Kobe_Bryant> <http://dbpedia.org/ontology/playoffMatch>
# <http://dbpedia.org/resource/Kobe_Bryant__1>

# Writing mapping rules is simple --> you have to fill all empty field remembering this structure:
# 'table's header':'ontology property' (Example:  'year':'Year', 'GP':'gamesPlayed','High school name':'nameSchool'). 

# Elements already filled  means that I have already found that header in pyTableExtractor dictionary
# or on dbpedia ontology.
# If you empty a field that was filled, you will delete that rule from dictionary.

KOBE_BRYANT___BASKETBALL_PLAYER_MAPPER___TABLES = {
'GS': 'gamesStarted', 
'BPG': 'blocksPerGame', 
'GP': 'gamesPlayed', 
'Team': 'team', 
'FG%': 'fieldGoal', 
'MPG': 'minutesPerGame', 
'PPG': 'pointsPerGame', 
'APG': 'assistsPerGame', 
'Regular season': 'regularSeason', 
'FT%': 'freeThrow', 
'Playoffs': 'playoff', 
'RPG': 'reboundsPerGame', 
'Year': 'Year', 
'3P%': 'threePoints', 
'SPG': 'stolePerGame', 
} 

# END OF FILE 
