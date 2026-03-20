# John Wayne Airport Performance Analytics

<<<<<<< HEAD
A data engineering and analytics project that collects live flight data from John Wayne Airport (SNA) and analyzes operational performance metrics such as delays, flight volume, and route trends.
=======
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)
![Data Pipeline](https://img.shields.io/badge/Pipeline-ETL-blueviolet)
![Power BI](https://img.shields.io/badge/Visualization-Power%20BI-yellow)

A data engineering and analytics project that collects live flight data from **John Wayne Airport (SNA)** and analyzes operational performance metrics such as delays, flight volume, and route trends.
>>>>>>> 521f9b49f3cad5aaa88c1f330ae6d13865da69e1

This project simulates a real-world airport performance management system, including data ingestion, cleaning, KPI generation, and dashboard reporting.

--------------------------------------------------

## Project Overview

Airports rely on performance metrics to understand:

- Flight delays and schedule reliability
- Busiest routes and destinations
- Gate utilization
- Airline performance trends

This project builds a data pipeline that collects live flight data, cleans and validates it, and transforms it into analytics-ready datasets used for KPI reporting and dashboards.

--------------------------------------------------

## Data Pipeline Architecture

Airport API (AWS JSON endpoint)
        ↓
Python Web Scraper (requests)
        ↓
Raw Flight Data (CSV)
        ↓
Data Cleaning and Validation (pandas)
        ↓
Cleaned Dataset (CSV or Parquet)
        ↓
KPI Computation (Python)
        ↓
Power BI Dashboard
        ↓
Operational Performance Insights

--------------------------------------------------

## Data Source

Flight data is collected from the John Wayne Airport public flight data endpoint.

The scraper retrieves:

- arrivals and departures
- flight numbers and airline codes
- airport routes
- scheduled and actual times
- gate assignments
- flight status

The pipeline stores daily snapshots of flight activity, enabling trend and performance analysis over time.

--------------------------------------------------

## Data Cleaning and Transformation

A dedicated cleaning pipeline standardizes raw data into a structured format.

Key transformations include:

- Parsing timestamps into datetime format
- Calculating flight delay in minutes
- Normalizing flight status into Early, On Time, Delayed, and Cancelled
- Handling missing values such as id = -1 and N/A claims
- Extracting airline and flight number from flight codes
- Creating derived features such as hour, day of week, and month
- Generating KPI flags such as on-time, delayed, and cancelled

--------------------------------------------------

## Example Dataset Fields

- flight_type: Arrival or departure
- city: Origin or destination city
- route_airport_code: Airport code for route
- scheduled_time: Scheduled arrival or departure
- actual_time: Actual arrival or departure
- delay_min: Delay in minutes
- status_clean: Standardized performance status
- airline: Airline name
- gate: Assigned gate
- claim: Baggage claim for arrivals

--------------------------------------------------

## Key Metrics

- On-Time Performance (OTP within 15 minutes)
- Average delay in minutes
- Cancellation rate
- Delay rate
- Flight volume by hour
- Delay rate by airline
- Arrival versus departure performance

--------------------------------------------------

## Example Analytics Questions

- What percentage of flights are on time
- Which airlines contribute most to delays
- What are the busiest hours at SNA
- Which routes experience the highest delays
- How do arrival and departure performance compare

--------------------------------------------------

## Project Structure

data
  raw
  processed

notebooks
  cleaning notebook
  analysis notebook

py_files
  webscraper
  main pipeline script

dashboard
  Power BI files

README
requirements

--------------------------------------------------

## How to Run the Pipeline

1. Clone the repository

git clone https://github.com/mtafoya-web/JohnWayneAirport-performance-analytics.git
cd JohnWayneAirport-performance-analytics

2. Create a virtual environment

python -m venv .venv

Activate the environment

Windows:
.venv\Scripts\activate

Mac or Linux:
source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Run the pipeline

<<<<<<< HEAD
python py_files/main.py
=======
```
python py_files/pipeline.py
```
>>>>>>> 521f9b49f3cad5aaa88c1f330ae6d13865da69e1

This will scrape the latest flight data, save the raw dataset, clean and transform the data, and generate an analytics-ready dataset.

--------------------------------------------------

## Dashboard

The processed dataset is used to build a Power BI dashboard showing delay trends, flight volume, route distribution, and airline performance.

--------------------------------------------------

## Technologies Used

- Python
- Pandas
- Requests
- Jupyter Notebook
- Power BI
- Git and GitHub

--------------------------------------------------

## Future Improvements

- Automate pipeline with scheduled jobs
- Store historical data in PostgreSQL
- Build automated KPI reporting
- Add anomaly detection for delays
- Develop delay prediction models

--------------------------------------------------

## License

MIT License