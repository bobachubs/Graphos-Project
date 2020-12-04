'''
From raw csv NBA dataset, build a new csv of games_details.csv with the
addition of a time field mapped to the date of the game from games.csv
'''

import csv

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

    fieldRow = next(reader)
    fieldRow.append('TIME')

    for row in reader:
        gameId = row[0]
        gameDate = gameIdToDate.get(gameId)
        if not gameDate:
            continue

        row.append(gameDate)
        dataRows.append(row)

# sort rows based on time
dataRows.sort(key=lambda row: row[-1])

with open('nba_stats.csv', 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(fieldRow)
    for row in dataRows:
        writer.writerow(row)
