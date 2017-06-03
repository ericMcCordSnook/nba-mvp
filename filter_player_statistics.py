# Eric McCord-Snook 3/6/2017
# github @ericMcCordSnook
# Inspired by code from github user @jxmorris12

import csv

HEADERS = ['Player','Tm','W/L%','WS','G','GS','MP','FG','FGA','2P','2PA','3P','3PA','FT','FTA','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','FG%','2P%','3P%','FT%']

def main():
    for year in range(1956, 2018):
        # Read in raw player data lines
        player_file = open("raw_data/players-" + str(year) + ".csv", 'r')
        player_lines_data = player_file.readlines()
        orig_headers = player_lines_data[0].split(",");
        headers = HEADERS
        player_lines = player_lines_data[1:]
        # Read in team win percentages
        team_file = open("raw_data/league-" + str(year) + ".csv", 'r')
        team_lines = team_file.readlines()
        # Put team win percentages into a dictionary
        win_loss_pcts = {}
        for line in team_lines:
            data = line.split(",")
            win_loss_pcts[data[0]] = data[1]
        # Write filtered data to CSV
        with open("filtered_data/players-" + str(year) + "-filtered.csv",'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            # Write headers
            csvwriter.writerow(headers)
            # Write lines of player data
            for line in player_lines:
                row = []
                vals = line.split(",")
                for i in range(len(vals)):
                    key = orig_headers[i]
                    val = vals[i]
                    if key in headers:
                        row.append(val)
                        if key == 'Tm':
                            i -= 1
                            try:
                                row.append("".join(win_loss_pcts[val].split()))
                            except:
                                row.append('')
                csvwriter.writerow(row)
        print("Successfully wrote to file filtered_data/players-" + str(year) + "-filtered.csv")

# call main method
if __name__ == "__main__": main()
