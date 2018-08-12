# coding:utf-8 

# Comments below will help you in filling this file settings. Remember to change only dictionary values.
# Please do not modify DomainExplorer parameters. 

# DomainExplorer parameters 
DOMAIN_EXPLORED = "BaseballPlayer" 
CHAPTER = "en" 
COLLECT_MODE = "t" 
RESOURCE_FILE = "2018_08_12_BaseballPlayer_en.txt" 

TABLES_INCLUDED = "true" 
LISTS_INCLUDED = "true" 
# The entry named sectionProperty represents ontology property associated to table's section.
# (Eg. in basket domain, section named playoff can be mapped with something like 'playoff' or  'playoffMatch').
# Triple example: <http://dbpedia.org/resource/Kobe_Bryant> <http://dbpedia.org/ontology/playoffMatch>
# <http://dbpedia.org/resource/Kobe_Bryant__1>

# Writing mapping rules is simple --> you have to fill all empty fields remembering this structure:
# 'table's header / list's section':'ontology property' (Example:  'year':'Year', 'GP':'gamesPlayed','High school name':'nameSchool'). 

# Elements which are already depicts that they have already been found in the common dictionary
# or on dbpedia ontology.
# If you empty a field that was filled, you will delete that rule from dictionary.

AJHINCH___BASEBALL_PLAYER_MAPPER___TABLES = {
'Managerial record': 'ManagerialRecord', 
'Team': 'team', 
'From': 'from', 
'To': 'to', 
'Regular season record - G': '', 
'Regular season record - W': 'BaseballSeasonWon', 
'Regular season record - L': 'BaseballSeasonLost', 
'Regular season record - Win%': 'BaseballSeasonWonPercentage', 
'Post-season record - G': '', 
'Post-season record - W': 'PostSeasonWon', 
'Post-season record - L': 'PostSeasonLost', 
'Post-season record - Win%': 'PostSeasonWonPercentage', 
} 
BARRYBONDS___BASEBALL_PLAYER_MAPPER___TABLES = {
'Other accomplishments': 'achievement', 
'Category': 'category', 
'Times': 'Count', 
'Seasons': 'BaseballSeason', 
'Award': 'Award', 
'# of Times': 'count', 
'Dates': 'TimePeriod', 
'Refs': 'reference', 
} 
BOBBYCOX___BASEBALL_PLAYER_MAPPER___TABLES = {
'Managerial record': 'ManagerialRecord', 
'Team': 'team', 
'From': 'from', 
'To': 'to', 
'Regular season record - G': '', 
'Regular season record - W': 'BaseballSeasonWon', 
'Regular season record - L': 'BaseballSeasonLost', 
'Regular season record - Win%': 'BaseballSeasonWonPercentage', 
'Post-season record - G': '', 
'Post-season record - W': 'PostSeasonWon', 
'Post-season record - L': 'PostSeasonLost', 
'Post-season record - Win%': 'PostSeasonWonPercentage', 
} 
BRYCEHARPER___BASEBALL_PLAYER_MAPPER___TABLES = {
'Career accomplishments': 'achievement', 
'Year': 'Year', 
'Award / Honor': 'award', 
'Refs': 'reference', 
} 
CLAYTONKERSHAW___BASEBALL_PLAYER_MAPPER___TABLES = {
'Awards': 'award', 
'Name of award': 'award', 
'Times': 'Count', 
'Dates': 'TimePeriod', 
'Ref': 'reference', 
'Annual statistical achievements': 'achievement', 
'Category': 'category', 
} 
CLINTHURDLE___BASEBALL_PLAYER_MAPPER___TABLES = {
'Managerial record': 'ManagerialRecord', 
'Team': 'team', 
'From': 'from', 
'To': 'to', 
'Regular season record - W': 'BaseballSeasonWon', 
'Regular season record - L': 'BaseballSeasonLost', 
'Regular season record - Win%': 'BaseballSeasonWonPercentage', 
'Post-season record - W': 'PostSeasonWon', 
'Post-season record - L': 'PostSeasonLost', 
'Post-season record - Win%': 'PostSeasonWonPercentage', 
} 
DAVIDORTIZ___BASEBALL_PLAYER_MAPPER___TABLES = {
'Annual statistical achievements': 'achievement', 
'Category': 'category', 
'Times': 'Count', 
'Dates': 'TimePeriod', 
'Ref': 'reference', 
} 
DEREKJETER___BASEBALL_PLAYER_MAPPER___TABLES = {
'Awards': 'award', 
'Award / Honor': 'award', 
'Time(s)': 'time', 
'Date(s)': 'date', 
} 
EARLWEAVER___BASEBALL_PLAYER_MAPPER___TABLES = {
'Managerial record': 'ManagerialRecord', 
'Team': 'team', 
'From': 'from', 
'To': 'to', 
'Regular season record - W': 'BaseballSeasonWon', 
'Regular season record - L': 'BaseballSeasonLost', 
'Regular season record - Win%': 'BaseballSeasonWonPercentage', 
'Post-season record - W': 'PostSeasonWon', 
'Post-season record - L': 'PostSeasonLost', 
'Post-season record - Win%': 'PostSeasonWonPercentage', 
} 
JAKEARRIETA___BASEBALL_PLAYER_MAPPER___TABLES = {
'Accomplishments and awards': 'award', 
'Award/Honor': 'award', 
'Date': 'date', 
'Ref': 'reference', 
} 
JOHNMCGRAW___BASEBALL_PLAYER_MAPPER___TABLES = {
'Statistics': 'statistics', 
'Year': 'Year', 
'Age': 'age', 
'Team': 'team', 
'Lg': 'MinorLeagueLevel', 
'G': 'Games', 
'AB': 'AtBats', 
'R': 'Runs', 
'H': 'Hits', 
'2B': 'Doubles', 
'3B': 'Triples', 
'HR': 'HomeRuns', 
'RBI': 'RunsBattedIn', 
'SB': 'StolenBases', 
'SO': 'StrikeOuts', 
'BA': '', 
'OBP': 'OnBasePercentage', 
'SLG': 'SluggingPercentage', 
'OPS': 'OnBasePlusSlugging', 
'Overall record': 'record', 
'From': 'from', 
'To': 'to', 
'Regular season record - G': '', 
'Regular season record - W': 'BaseballSeasonWon', 
'Regular season record - L': 'BaseballSeasonLost', 
'Regular season record - Win%': 'BaseballSeasonWonPercentage', 
'Post-season record - G': '', 
'Post-season record - W': 'PostSeasonWon', 
'Post-season record - L': 'PostSeasonLost', 
'Post-season record - Win%': 'PostSeasonWonPercentage', 
} 
MIKETROUT___BASEBALL_PLAYER_MAPPER___TABLES = {
'Statistical achievements': 'achievement', 
'Category': 'category', 
'Times': 'Count', 
'Seasons': 'BaseballSeason', 
} 
TERRYFRANCONA___BASEBALL_PLAYER_MAPPER___TABLES = {
'Managerial record': 'ManagerialRecord', 
'Team': 'team', 
'From': 'from', 
'To': 'to', 
'Regular season record - G': 'BaseballSeasonGames', 
'Regular season record - W': 'BaseballSeasonWon', 
'Regular season record - L': 'BaseballSeasonLost', 
'Regular season record - Win%': 'BaseballSeasonWonPercentage', 
'Post-season record - G': 'PostSeasonGames', 
'Post-season record - W': 'PostSeasonWon', 
'Post-season record - L': 'PostSeasonLost', 
'Post-season record - Win%': 'PostSeasonWonPercentage', 
} 
ZACKGREINKE___BASEBALL_PLAYER_MAPPER___LISTS = {
'Pitching style': 'throwingSide', 
} 
DEREKJETER___BASEBALL_PLAYER_MAPPER___LISTS = {
'Career highlights - Statistical highlights': 'achievements', 
} 

# END OF FILE 
