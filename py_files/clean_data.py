import os
import logging
import pandas as pd
import numpy as np
from datetime import datetime


logger = logging.getLogger(__name__)


class Cleandata:
    def __init__(self, csv):
        logger.info(f"Loading raw CSV file: {csv}")
        self.df = pd.read_csv(csv)
        logger.info(f"Loaded DataFrame with {len(self.df)} rows and {len(self.df.columns)} columns")

    def run(self):
        logger.info("Starting full cleaning pipeline")

        self.__clean()
        self.__key_performance_indicators()
        self.__quality_checks()
        self.__inspect_delays()
        self.__export_to_csv()

        logger.info("Cleaning pipeline completed successfully")

    def __normalize_status(self, row):
        status = row["status"]
        delay = row["delay_min"]

        if status == "Cancelled":
            return "Cancelled"
        if pd.isna(delay):
            return "Unknown"
        if delay <= -15:
            return "Early"
        if delay <= 15:
            return "On Time"
        return "Delayed"

    def __clean(self):
        logger.info("Step 1: Starting data cleaning")

        logger.info(f"Initial DataFrame shape: {self.df.shape}")
        logger.info(f"Columns before cleaning: {list(self.df.columns)}")

        # Standardize columns
        self.df.columns = (
            self.df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_", regex=False)
        )
        logger.info(f"Columns after cleaning: {list(self.df.columns)}")

        # Missing values
        logger.info("Checking missing values")
        logger.info(f"\n{self.df.isna().sum()}")

        # Convert datetime
        logger.info("Converting scheduled_time and actual_time to datetime")
        self.df["scheduled_time"] = pd.to_datetime(self.df["scheduled_time"], errors="coerce")
        self.df["actual_time"] = pd.to_datetime(self.df["actual_time"], errors="coerce")

        # Create delay
        logger.info("Calculating delay in minutes")
        self.df["delay_min"] = (
            (self.df["actual_time"] - self.df["scheduled_time"]).dt.total_seconds() / 60
        )

        # Clean ID
        logger.info("Cleaning ID column (convert to numeric, replace -1 with NaN)")
        self.df["id"] = pd.to_numeric(self.df["id"], errors="coerce")
        self.df["id"] = self.df["id"].replace(-1, np.nan)
        logger.info(f"Missing IDs: {self.df['id'].isna().sum()}")

        # Clean claim
        logger.info("Cleaning claim column")
        self.df["claim"] = self.df["claim"].replace("N/A", np.nan)
        self.df["claim"] = pd.to_numeric(self.df["claim"], errors="coerce")

        # Clean gate
        logger.info("Cleaning gate column")
        self.df["gate"] = self.df["gate"].astype(str).str.strip().str.upper()

        # Clean status
        logger.info("Standardizing status column")
        self.df["status"] = self.df["status"].astype(str).str.strip().str.title()
        logger.info(f"Unique statuses: {self.df['status'].unique()}")

        # Flight codes
        logger.info("Extracting primary flight code")
        self.df["primary_flight_code"] = (
            self.df["flight_codes"].astype(str).str.split(",").str[0].str.strip()
        )

        # Airline + flight number
        logger.info("Extracting airline code and flight number")
        self.df["airline_code"] = self.df["primary_flight_code"].str.extract(r"^([A-Z]+)")
        self.df["flight_number"] = self.df["primary_flight_code"].str.extract(r"(\d+)$")

        # Airline mapping
        airline_map = {
            "WN": "Southwest",
            "AA": "American",
            "UA": "United",
            "AC": "Air Canada",
            "DL": "Delta",
            "AS": "Alaska",
            "NK": "Spirit",
            "F9": "Frontier",
            "G4": "Allegiant",
            "MX": "Breeze",
            "WS": "WestJet"
        }

        logger.info("Mapping airline codes to airline names")
        self.df["airline"] = self.df["airline_code"].map(airline_map).fillna("Other")

        # Normalize status
        logger.info("Creating cleaned status column")
        self.df["status_clean"] = self.df.apply(self.__normalize_status, axis=1)

        # Time features
        logger.info("Creating time-based features")
        self.df["flight_date"] = self.df["scheduled_time"].dt.date
        self.df["hour"] = self.df["scheduled_time"].dt.hour
        self.df["day_of_week"] = self.df["scheduled_time"].dt.day_name()
        self.df["month"] = self.df["scheduled_time"].dt.month

        logger.info("Step 1 complete: Data cleaning finished")

    def __key_performance_indicators(self):
        logger.info("Step 2: Creating KPI columns")

        self.df["is_cancelled"] = (self.df["status_clean"] == "Cancelled").astype(int)
        self.df["is_delayed"] = (self.df["status_clean"] == "Delayed").astype(int)
        self.df["is_ontime"] = (self.df["status_clean"] == "On Time").astype(int)
        self.df["is_early"] = (self.df["status_clean"] == "Early").astype(int)

        logger.info("KPI flags created")

        # OTP 15
        logger.info("Calculating OTP (On-Time Performance within 15 minutes)")
        self.df["otp_15_flag"] = np.where(
            self.df["status_clean"] != "Cancelled",
            (self.df["delay_min"] <= 15).astype(int),
            np.nan
        )

        logger.info("Step 2 complete")

    def __quality_checks(self):
        logger.info("Step 3: Running data quality checks")

        logger.info(f"Rows: {len(self.df)}")
        logger.info(f"Missing IDs: {self.df['id'].isna().sum()}")
        logger.info(f"Missing claims: {self.df['claim'].isna().sum()}")
        logger.info(f"Missing scheduled_time: {self.df['scheduled_time'].isna().sum()}")
        logger.info(f"Missing actual_time: {self.df['actual_time'].isna().sum()}")

        logger.info(f"Status distribution:\n{self.df['status_clean'].value_counts()}")
        logger.info(f"Flight type distribution:\n{self.df['flight_type'].value_counts()}")
        logger.info(f"Airline distribution:\n{self.df['airline'].value_counts()}")

        logger.info("Step 3 complete")

    def __inspect_delays(self):
        logger.info("Step 4: Inspecting top 10 delays")

        top_delays = self.df.sort_values("delay_min", ascending=False)[
            ["flight_type", "city", "airline", "scheduled_time", "actual_time", "delay_min", "status_clean"]
        ].head(10)

        logger.info(f"\nTop 10 delayed flights:\n{top_delays}")

        logger.info("Step 4 complete")

    def __export_to_csv(self):
        logger.info("Step 5: Exporting cleaned data")

        today = datetime.today().strftime("%Y-%m-%d")
        output_dir = "./data/processed"
        os.makedirs(output_dir, exist_ok=True)

        filename = f"JohnWayneFlights_{today}.csv"
        full_path = f"{output_dir}/{filename}"

        self.df.to_csv(full_path, index=False)

        logger.info(f"Data exported successfully to: {full_path}")