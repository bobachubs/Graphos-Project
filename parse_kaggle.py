# From raw csv NBA dataset, build a new csv of games_details.csv with the
# addition of a time field mapped to the date of the game from games.csv
# nba dataset by Nathan Lauga
# https://www.kaggle.com/nathanlauga/nba-games

import csv
# same with data_manager.py, csv reading help and lambada from pythondoc
# but code self-written
# https://stackoverflow.com/questions/16310015/what-does-this-mean-key-lambda-x-x1

gameIdToDate = {}
with open('games.csv') as csvfile:
    csvfile.readline()
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        gameDate = row[0]
        gameId = row[1]
        gameIdToDate[gameId] = gameDate

fieldRow = None
dataRows = []
with open('games_details.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',') 

# line 23 help and guidance from acquaintance to help code flow
    fieldRow = next(reader)
    fieldRow.append('TIME')

    for row in reader:
        gameId = row[0]
        gameDate = gameIdToDate.get(gameId)
        if not gameDate:
            continue

        row.append(gameDate)
        dataRows.append(row)

fieldsToKeep = ['TEAM_ABBREVIATION', 'PLAYER_NAME', 'FGM', 'FGA', 'FTM', 'FTA', 'OREB', 'REB', 'AST', 'PTS', 'PLUS_MINUS', 'TIME']
fieldIndicesToRemove = [i for i,v in enumerate(fieldRow) if v not in fieldsToKeep]
fieldIndicesToRemove.reverse()

# sort rows based on time
dataRows.sort(key=lambda row: row[-1])

with open('nba_stats.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(fieldsToKeep)
    for row in dataRows:
        for idx in fieldIndicesToRemove:
            row.pop(idx)
        writer.writerow(row)
