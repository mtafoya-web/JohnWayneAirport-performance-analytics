import logging
from datetime import datetime

import pandas as pd
import requests

logger = logging.getLogger(__name__)


class Webscraper:
    def __init__(self, url, headers):
        logger.info("Initializing Webscraper")
        self.url = url
        self.headers = headers
        self.response = None
        self.data = None
        logger.info(f"Scraper configured with URL: {self.url}")

    def fetch_data(self):
        logger.info("Sending GET request to flight data source")
        try:
            self.response = requests.get(self.url, headers=self.headers, timeout=20)
            self.response.raise_for_status()
            logger.info(f"Request successful with status code {self.response.status_code}")

            logger.info("Parsing response body as JSON")
            self.data = self.response.json()
            logger.info("JSON data loaded successfully")

        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except ValueError as e:
            logger.error(f"Failed to decode response as JSON: {e}")
            raise

    def log_status(self):
        if self.response is None:
            logger.warning("No response available yet. Run fetch_data() first.")
            return

        logger.info(f"Response status code: {self.response.status_code}")
        logger.info(f"Response content type: {self.response.headers.get('Content-Type')}")

    def log_top_level_keys(self):
        if self.data is None:
            logger.warning("No data available yet. Run fetch_data() first.")
            return

        logger.info("Listing top-level keys from JSON response")
        for key in self.data.keys():
            logger.info(f"Top-level key: {key}")

    def __create_data(self):
        logger.info("Transforming raw JSON into tabular flight records")

        flights = self.data.get("flights", {})
        airports = self.data.get("airports", {})

        arrivals = flights.get("arrivals", [])
        departures = flights.get("departures", [])

        logger.info(f"Found {len(arrivals)} arrivals")
        logger.info(f"Found {len(departures)} departures")

        arrival_rows = []
        departure_rows = []

        for flight in arrivals:
            city = "NAN"
            route = flight.get("route")

            if route is not None:
                code = route[0]
                city = airports.get(code, "NAN")
            else:
                code = "NAN"

            arrival_rows.append({
                "id": flight.get("id"),
                "flight_type": "arrival",
                "city": city,
                "status": flight.get("status"),
                "gate": flight.get("gate"),
                "claim": flight.get("Claim"),
                "scheduled_time": flight.get("times", {}).get("scheduled"),
                "actual_time": flight.get("times", {}).get("actual"),
                "flight_codes": ", ".join(flight.get("codes", [])),
                "route_airport_code": ", ".join(flight.get("route", [])),
            })

        for flight in departures:
            city = "NAN"
            route = flight.get("route")

            if route is not None:
                code = route[0]
                city = airports.get(code, "NAN")
            else:
                code = "NAN"

            departure_rows.append({
                "id": flight.get("id"),
                "flight_type": "departure",
                "city": city,
                "status": flight.get("status"),
                "gate": flight.get("gate"),
                "claim": flight.get("Claim"),
                "scheduled_time": flight.get("times", {}).get("scheduled"),
                "actual_time": flight.get("times", {}).get("actual"),
                "flight_codes": ", ".join(flight.get("codes", [])),
                "route_airport_code": ", ".join(flight.get("route", [])),
            })

        df = pd.DataFrame(arrival_rows + departure_rows)
        logger.info(f"Created DataFrame with shape: {df.shape}")
        return df

    def export_data(self):
        if self.data is None:
            logger.warning("No data available to export. Run fetch_data() first.")
            return

        logger.info("Creating DataFrame for CSV export")
        df = self.__create_data()

        today = datetime.today().strftime("%Y-%m-%d")
        path = "./data/"
        filename = f"JohnWayneFlights_{today}.csv"
        full_path = path + filename

        logger.info(f"Exporting scraped data to {full_path}")
        df.to_csv(full_path, index=False)
        logger.info("CSV export completed successfully")

    def run(self):
        logger.info("Starting scraper pipeline")
        self.fetch_data()
        self.log_status()
        self.log_top_level_keys()
        self.export_data()
        logger.info("Scraper pipeline finished successfully")