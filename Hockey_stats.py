import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from datetime import datetime
currentYear = datetime.now().year
stats = dict()
listOfStatDic = list()

#Dictionary to convert user input into HTML attribute format
pointTypeDic = {'games played' : 'games_played', 
'age' : 'age',
'goals' : 'goals',
'assists' : 'assists',
'points' : 'points',
'plus/minus' : 'plus_minus',
'penalty-minutes' : 'pen_min',
'shots' : 'shots',
'blocks' : 'blocks',
'hits' : 'hits',
'faceoff-%' : 'faceoff_percentage'}
print ('\033[1m' + 'NHL Stat Finder' + '\033[0m')

while True: #Loop that ensures stats dictionary is full with stats from season
    #stat dictionary will be empty if stat was not recorded for the given season 

    #block checks if season entry is in range
    urlPart1 = 'https://www.hockey-reference.com/leagues/NHL_'
    urlPart2 = '_skaters.html#stats::points'
    while True: 
        season = input('Select a season: ')
        try: #try/except to make sure season is an int between 1918 and the current year
            season = int(season)
            if season < 1918 or season > currentYear:
                print('Season needs to be between 1918 and', currentYear)
                continue
            else:
                break
        except ValueError:
            print('Season needs to be between 1918 and', currentYear)
            continue
     
    season = str(season)
    url = urlPart1 + season + urlPart2
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    #putting html into beautiful soup
    tags = soup('tr') #finds all 'tr' tags within soup

    def statChecker(statList): #function checks if input stats are in pointTypeDic
        for statType in statList:
            if statType not in pointTypeDic:
                print('\n')
                print(statType, '''is not an available stat. Select a stat from the list
            Games Played 
            Age 
            Goals
            Assists
            Points 
            Plus/Minus
            Penalty-Minutes 
            Shots 
            Blocks
            Hits 
            Faceoff-% ''')
                return None
        return statList

    while True: #Loop checks if input stats are available to view in pointTypeDic
        pointType = input('Which stats do you want to see? ')
        pointType = pointType.lower()
        statList = pointType.split() #splits pointType inputs into list

        if statChecker(statList) == None:
             #checks return of statChecker. If no error breaks loop, else continue
            continue
        else:
            break

    
    #function scrapes site and creates a dictionary of player names as keys and pointType as the value
    def webScraper(stat):     
        for tag in tags: 
            name = tag.find('a') #finds 'a'attr within 'tr' tag
            points = tag.find('td', {'data-stat':pointTypeDic[stat]}) #finds pointTypea within 'td' tag
            try:
                points = int(points.string) #if int: convert to int for sorting later
                stats[name.string] = points #addds to dict
            except:
                try: 
                    points = float(points.string) #if float: convert to float for sorting later
                    stats[name.string] = points #addds to dict
                except:
                    continue
        return stats

    #checks if stat is available for season then appends stat dictionary to list
    def statAppend(statList): 
        for stat in statList:
            if not bool(webScraper(stat)): # if stats is empty returns None and loop continues from start
                print(stat.capitalize(), 'not available for', season)
                return None
            else:
                statsCopy = webScraper(stat).copy()
                listOfStatDic.append(statsCopy) #appends stats dict copy for each stat type. Now have list of dicitonaries
                stats.clear() 
        return listOfStatDic
    
    if statAppend(statList) == None:
        continue 
    else: 
        break

while True:
    numberPlayers = input('How many players do you want to see? ')
    try:
        numberPlayers = int(numberPlayers)
        numberPlayers = abs(numberPlayers)
        break
    except ValueError:
        print('Enter an integer.')
        continue

i=0
#block orders listOfStatDic by values and prints to screen based on highest values
for dictIndex in listOfStatDic: #dictIndex is the dictionary in the list of dictionaries
    orderedByPoints = list()
    for k,v in dictIndex.items():
        temp = (v,k)
        orderedByPoints.append(temp)
        #appends dict items into list of tuples

    if i < len(statList):
        print('\n')
        print('\033[1m'  + statList[i].capitalize() +  ' Leaders ' + season + '\033[0m') #bolds text 'Most 'pointType'
        i = i + 1

    orderedByPoints = sorted(orderedByPoints, reverse = True)
    for k,v in orderedByPoints[:numberPlayers]:
        print(v,k) #prints players name then the corresponding stat from list of reversed tuples

