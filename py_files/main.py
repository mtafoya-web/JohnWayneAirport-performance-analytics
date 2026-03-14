from webscraper import Webscraper

URL = "https://s3-us-west-2.amazonaws.com/files.ocair.com/data/sna_export.js"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.ocair.com/",
    "Origin": "https://www.ocair.com",
}

def main():
    scraper = Webscraper(URL, HEADERS)
    scraper.run()

if __name__ == "__main__":
    main()