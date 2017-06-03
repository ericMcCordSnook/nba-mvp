# Eric McCord-Snook 3/6/2017
# github @ericMcCordSnook

import csv

HEADERS = ['Player','W/L%','WS','G','GS','MP','FG','FGA','2P','2PA','3P','3PA','FT','FTA','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','FG%','2P%','3P%','FT%']

def getPastMvps():
    mvp_file = open("learning_data/past-mvps.csv",'r')
    lines = mvp_file.read().splitlines()
    past_mvps = {}
    for line in lines:
        data = line.split(",")
        past_mvps[data[0]] = data[1]
    return past_mvps

def createInitialWeightVector():
    headers = HEADERS
    weight_vector = {}
    for i in range(2,len(headers)):
        weight_vector[headers[i]] = 1
    return weight_vector

def getPlayerStatDictsByYear(year):
    player_file = open("normalized_data/players-" + str(year) + "-normalized.csv", 'r')
    lines = player_file.read().splitlines()[1:]
    players = {}
    headers = HEADERS
    for player in lines:
        cur_player_dict = {}
        data = player.split(",")
        for i in range(2, len(data)):
            cur_player_dict[headers[i]] = data[i]
        players[data[0]] = cur_player_dict
    return players

def getPlayerScore(player_stats, weight_vector):
    score = 0
    sum_of_weights = 0
    for stat in player_stats:
        try:
            score += float(player_stats[stat]) * float(weight_vector[stat])
            sum_of_weights += weight_vector[stat]
        except:
            continue
    return score / sum_of_weights

def getErrorForRanking(player_rank_list, mvp):
    i = 0
    while not player_rank_list[i][0] == mvp:
        i += 1
    return i

def main():
    past_mvps = getPastMvps()
    weight_vector = createInitialWeightVector()
    for year in range(1956, 2017):
        players = getPlayerStatDictsByYear(year)
        player_rank_list = []
        max_score = 0
        for player in players:
            player_score = getPlayerScore(players[player], weight_vector)
            player_rank_list.append((player, player_score))
            max_score = max(max_score, player_score)
        player_rank_list.sort(key=lambda tup:tup[1], reverse=True)
        # player_rank_list = [(player, round(score / max_score * 100, 3)) for (player, score) in player_rank_list]
        error = getErrorForRanking(player_rank_list, past_mvps[str(year)])
        print(str(year) + " : " + str(error))

        # Use batch/stochastic gradient descent to minimize this error
        # Predict the next mvp

# call main method
if __name__ == "__main__": main()
