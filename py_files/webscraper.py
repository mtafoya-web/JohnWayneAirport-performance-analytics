import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

### Collects json data from aws ###
class Webscraper:
    def __init__(self, url, headers):
        ### Needs the API URL ###
        self.url = url
        self.headers = headers
        self.response = None
        self.data = None

    def fetch_data(self):
        self.response = requests.get(self.url, headers=self.headers, timeout=20)
        self.response.raise_for_status()
        self.data = self.response.json()

    def printStatus(self):
        if self.response is None:
            print("No response yet, run fetch_data() first")
        print("Status code", self.response.status_code)
        print("Content Type", self.response.headers.get("Content-Type"))
    
    def printTopLevelKeys(self):
        if self.response is None:
            print("No data yet. run fetch_data() first.")
        print("Top-Level keys")
        for key in self.data.keys():
            print("-", key)
    
    def exportData(self):
        df = self.__createData()
        today = datetime.today().strftime("%Y-%m-%d")
        path = "./data/"
        filename = f"JohnWayneFlights_{today}.csv"
        df.to_csv(path + filename, index = False)
    
    def __createData(self):
        arrivals = self.data.get("flights").get("arrivals")
        departures = self.data.get("flights").get("departures")
        arrival_rows = list()
        departures_rows = list()
        for flight in arrivals:
            city = "NAN"
            if flight.get("route") != None:
                code = flight.get("route")
                code = code[0]
                city = self.data.get("airports").get(code)
            else:
                code = "NAN"
            arrival_rows.append({
                "id": flight.get("id"),
                "city": city,
                "status": flight.get("status"),
                "gate": flight.get("gate"),
                "claim": flight.get("Claim"),
                "scheduled_time": flight.get("times", {}).get("scheduled"),
                "actual_time": flight.get("times", {}).get("actual"),
                "flight_codes": ", ".join(flight.get("codes", [])),
                "arrival_airport_code": ", ".join(flight.get("route", [])),
            })

        for flight in departures:
            city = "NAN"
            if flight.get("route") != None:
                code = flight.get('route')
                ### route containse the airport code ###
                code = code[0]
                city = self.data.get("airports").get(code)
            else:
                code = "NAN"
            departures_rows.append({
                "id": flight.get("id"),
                "city": city,
                "status": flight.get("status"),
                "gate": flight.get("gate"),
                "claim": flight.get("Claim"),
                "scheduled_time": flight.get("times", {}).get("scheduled"),
                "actual_time": flight.get("times", {}).get("actual"),
                "flight_codes": ", ".join(flight.get("codes", [])),
                "arrival_airport_code": ", ".join(flight.get("route", [])),
            })
        
        df = pd.DataFrame(arrival_rows + departures_rows)
        return df
    
    def run(self):
        self.fetch_data()
        self.printStatus()
        self.exportData()