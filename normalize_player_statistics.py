# Eric McCord-Snook 3/6/2017
# github @ericMcCordSnook

import csv

HEADERS = ['Player','W/L%','WS','G','GS','MP','FG','FGA','2P','2PA','3P','3PA','FT','FTA','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','FG%','2P%','3P%','FT%']

def getPlayerStatDictsByYear(year):
    player_file = open("filtered_data/players-" + str(year) + "-filtered.csv", 'r')
    lines = player_file.read().splitlines()[1:]
    players = {}
    headers = HEADERS
    for player in lines:
        cur_player_dict = {}
        data = player.split(",")
        for i in range(2, len(data)):
            cur_player_dict[headers[i-1]] = data[i]
        players[data[0]] = cur_player_dict
    return players

def normalizeStatistics(players):
    headers = HEADERS
    for stat in headers[1:]:
        max_stat_val = 0.0
        for player in players:
            try:
                max_stat_val = max(max_stat_val, float(players[player][stat]))
            except:
                continue
        for player in players:
            try:
                players[player][stat] = round(float(players[player][stat]) / float(max_stat_val), 3)
            except:
                continue
    return players

def main():
    headers = HEADERS
    for year in range(1956, 2017):
        players = getPlayerStatDictsByYear(year)
        players = normalizeStatistics(players)
        player_row_list = []
        for player in players:
            cur_player_row = [player]
            for stat in headers[1:]:
                cur_player_row.append(players[player][stat])
            player_row_list.append(cur_player_row)
        with open("normalized_data/players-" + str(year) + "-normalized.csv",'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # Write headers
            csvwriter.writerow(headers)
            # Write lines of player data
            for player_row in player_row_list:
                csvwriter.writerow(player_row)

# call main method
if __name__ == "__main__": main()
