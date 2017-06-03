# Eric McCord-Snook 3/7/2017
# github @ericMcCordSnook

import csv
import re
import requests
from bs4 import BeautifulSoup

# get the search url for the current year
def getQueryUrlByYear(year):
    return "http://www.basketball-reference.com/leagues/NBA_" + str(year) + ".html"

# Adapted from code by github user @andrewgiessel
def getSoupFromURL(url, suppressOutput=True):
    # This function grabs the url and returns and returns the BeautifulSoup object
    if not suppressOutput:
        print("Querying: " + url + ".")
    try:
        r = requests.get(url)
        if not suppressOutput:
          print("Query successful.")
    except:
        if not suppressOutput:
            print("Query failed.")
        return None
    return BeautifulSoup(r.text, "html.parser")

def load_win_loss_pcts(year):
    search_query = getQueryUrlByYear(year)
    soup = getSoupFromURL(search_query, False)
    if soup == None:
        print("Error getting data for year " + str(year))
        return
    # Get win-loss percentages for each team in the league and put in dictionary
    rows = soup.find_all('tr', attrs={"class" : "full_table"})
    win_loss_pcts = []
    for row in rows:
        teamId = row.find('a').get('href')[7:10]
        win_loss_pct = row.find('td', attrs={"data-stat" : "win_loss_pct"}).string
        if not [teamId, win_loss_pct] in win_loss_pcts:
            win_loss_pcts.append([teamId, win_loss_pct])
    return win_loss_pcts

def main():
    for year in range(1956, 2018):
        # Load league data for current year
        win_loss_pcts = load_win_loss_pcts(year)
        # Set output file based on current year
        OUTPUT_FILE = "raw_data/league-" + str(year) + ".csv"
        # Export data to CSV file
        with open(OUTPUT_FILE, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting = csv.QUOTE_MINIMAL)
            # Write headers and all league data
            for curTeam in win_loss_pcts:
                csvwriter.writerow(curTeam)
            # Finished
            print("Successfully wrote to " + OUTPUT_FILE)

# call main method
if __name__ == "__main__": main()
