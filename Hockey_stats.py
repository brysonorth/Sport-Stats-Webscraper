import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from datetime import datetime
x = 0
currentYear = datetime.now().year
print ('\033[1m' + 'NHL Stat Finder' + '\033[0m')

while True: #Loop that ensures stats dictionary is full with stats from season
    #stat dictionary will be empty if stat was not recorded for the given season 
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
    #url = 'https://www.hockey-reference.com/leagues/NHL_2020_skaters.html#stats::points' #all skater stats 19/20
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    #putting html into beautiful soup

    tags = soup('tr') #finds all 'tr' tags within soup
    stats = dict()
    pointTypeDic = {'games played' : 'games_played', 
    'age' : 'age',
    'goals' : 'goals',
    'assists' : 'assists',
    'points' : 'points',
    'plus/minus' : 'plus_minus',
    'penalty minutes' : 'pen_min',
    'shots' : 'shots',
    'blocks' : 'blocks',
    'hits' : 'hits',
    'faceoff percentage' : 'faceoff_percentage'}

    while True: #Loop to ensure stat is available from scraped stats
        pointType = input('Which stat do you want to see? ')
        pointType = pointType.lower()
        if pointType not in pointTypeDic:
            print('\n')
            print(pointType, '''is not an available stat. Select a stat from the list
    Games Played 
    Age 
    Goals
    Assists
    Points 
    Plus/Minus
    Penalty Minutes 
    Shots 
    Blocks
    Hits 
    Faceoff Percentage ''')
            continue
        else:
            break

    for tag in tags: 
        name = tag.find('a') #finds 'a'attr within 'tr' tag
        points = tag.find('td', {'data-stat':pointTypeDic[pointType]}) #finds pointTypea within 'td' tag
        try:
            points = int(points.string) #if int: convert to int for sorting later
            stats[name.string] = points #addds to dict
        except:
            try: 
                points = float(points.string) #if float: convert to float for sorting later
                stats[name.string] = points #addds to dict
            except:
                continue
    if not bool(stats): # if stats is empty - continue loop
        print(pointType.capitalize(), 'not available for that season.')
        continue
    else:
        break

orderedByPoints = list()
for k,v in stats.items():
    temp = (v,k)
    orderedByPoints.append(temp)
    #appends dict items into list of tuples

while True:
    numberPlayers = input('How many players do you want to see? ')
    try:
        numberPlayers = int(numberPlayers)
        numberPlayers = abs(numberPlayers)
        break
    except ValueError:
        print('Enter an integer.')
        continue

print('\n')
print ('\033[1m' + 'Most ' + pointType.capitalize() + '\033[0m') #bolds text 'Most 'pointType'

orderedByPoints = sorted(orderedByPoints, reverse = True)
for k,v in orderedByPoints[:numberPlayers]:
    print(v,k) #prints players name then the corresponding stat from list of reversed tuples