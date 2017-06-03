# Eric McCord-Snook 3/6/2017
# github @ericMcCordSnook
# Adapted from code by github user @jxmorris12

import csv
import requests
from bs4 import BeautifulSoup

# get the search url for the current year
# ordered by estimated win shares so as to include this important statistic
def getQueryUrlByYear(year):
    return "http://www.basketball-reference.com/play-index/psl_finder.cgi?request=1&type=totals&year_min=" + str(year) + "&year_max=" + str(year) + "&age_min=0&age_max=99&height_min=0&height_max=99&order_by=ws"

# Adapted from code by github user @andrewgiessel
def getSoupFromURL(url, suppressOutput=True):
    # This function grabs the url and returns and returns the BeautifulSoup object
    if not suppressOutput:
        print("Querying: " + url)
    try:
        r = requests.get(url)
        if not suppressOutput:
          print("Query successful.")
    except:
        if not suppressOutput:
            print("Query failed.")
        return None
    return BeautifulSoup(r.text, "html.parser")

# Load statistics for all players for a given year
def load_year_data(year):
    search_query = getQueryUrlByYear(year)
    soup = getSoupFromURL(search_query, False)
    if soup == None:
        print("Error getting data for year " + str(year))
        return
    # Get table
    table = soup.find('table', attrs={"class" : "sortable"})
    # Get headers
    headers = [header.text for header in table.find_all('th')]
    # Remove top headers and other irrelevant headers to just have statistics
    del headers[:5]
    del headers[32:]
    # Fill rows with data
    rows = []
    for row in table.find_all('tr'):
        data = [val.text for val in row.find_all('td')]
        if len(data) > 0:
            rows.append(data)
    table = [headers]
    table.extend(rows)
    return table

def main():
    # start with 1956
    for year in range(1956, 2018):
      # Load data for all players from current year
      player_data_for_year = load_year_data(year)
      # Set output file based on current year
      OUTPUT_FILE = "raw_data/players-" + str(year) + ".csv"
      # Export data to CSV file
      print("Writing to " + OUTPUT_FILE)
      with open(OUTPUT_FILE, 'w', newline='') as csvfile:
          csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
          # Write headers and all player data
          for row in player_data_for_year:
              csvwriter.writerow(row)
          # Finished
          print("Successfully wrote to " + OUTPUT_FILE)

# call main method
if __name__ == "__main__": main()
