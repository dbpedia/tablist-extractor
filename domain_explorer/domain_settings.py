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

#Mapper used for the following are: BASKETBALL_PLAYER_MAPPER

BASKETBALL_PLAYER_MAPPER = {
# Example page where it was found this section: Kobe_Bryant
'SECTION_Regular_season' : 'regularSeason', 
'Year': 'Year', 
'Team': 'team', 
'GP': 'gamesPlayed', 
'GS': 'gamesStarted', 
'MPG': 'minutesPerGame', 
'FG%': 'fieldGoal', 
'3P%': 'threePoints', 
'FT%': 'freeThrow', 
'RPG': 'reboundsPerGame', 
'APG': 'assistsPerGame', 
'SPG': 'stolePerGame', 
'BPG': 'blocksPerGame', 
'PPG': 'pointsPerGame', 
# Example page where it was found this section: Kobe_Bryant
'SECTION_Playoffs' : 'playoff', 
} 

# END OF FILE 
