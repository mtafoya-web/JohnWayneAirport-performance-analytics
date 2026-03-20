from webscraper import Webscraper
from clean_data import Cleandata
from datetime import datetime
import logging 
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("pipeline.log"),
        logging.StreamHandler()
    ]
)


SNA_URL_API = "https://s3-us-west-2.amazonaws.com/files.ocair.com/data/sna_export.js"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.ocair.com/",
    "Origin": "https://www.ocair.com",
}

today = datetime.today().strftime("%Y-%m-%d")
path = "./data/"
filename = f"JohnWayneFlights_{today}.csv"

def run_pipeline():
    scraper = Webscraper(SNA_URL_API, HEADERS)
    scraper.run()
    cleaner = Cleandata(path + filename)
    cleaner.run()

if __name__ == "__main__":
    run_pipeline()