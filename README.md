# John Wayne Airport Performance Analytics

A data engineering and analytics project that collects live flight data from **John Wayne Airport (SNA)** and analyzes operational performance metrics such as delays, flight volume, and route trends.

The goal of this project is to simulate how airports and airlines monitor **operational efficiency and on-time performance** using automated data pipelines and business intelligence dashboards.

---

## Project Overview

Airports rely on performance metrics to understand:

* Flight delays and schedule reliability
* Busiest routes and destinations
* Gate utilization
* Airline performance trends

This project builds a **data pipeline that collects live flight data and transforms it into analytics-ready datasets** used to generate insights and dashboards.

---

## Data Pipeline Architecture

```
Airport API (AWS JSON endpoint)
            │
            ▼
Python Web Scraper (requests)
            │
            ▼
Data Cleaning + Transformation (pandas)
            │
            ▼
Historical Flight Dataset (CSV storage)
            │
            ▼
Power BI Dashboard
            │
            ▼
Operational Performance Insights
```

---

## Data Source

Flight data is collected from the **John Wayne Airport public flight data endpoint**.

The scraper retrieves:

* arrivals
* departures
* flight numbers
* airline codes
* airport routes
* scheduled times
* actual times
* gate assignments
* flight status

The script runs periodically and stores daily snapshots of flight activity.

---

## Example Dataset Fields

| Column         | Description                            |
| -------------- | -------------------------------------- |
| id             | Flight identifier                      |
| city           | Destination or origin city             |
| status         | Flight status (on time, delayed, etc.) |
| gate           | Assigned gate                          |
| scheduled_time | Scheduled departure or arrival         |
| actual_time    | Actual departure or arrival            |
| flight_codes   | Airline flight codes                   |
| airport_code   | Route airport codes                    |

---

## Key Metrics Analyzed

This project focuses on operational KPIs commonly used in airport management:

* **On-time performance rate**
* **Average delay by airline**
* **Flight volume by route**
* **Arrival vs departure distribution**
* **Busiest hours of airport traffic**

---

## Example Analytics Questions

* Which airlines have the highest delay rates?
* What are the busiest flight hours at SNA?
* Which routes have the most traffic?
* Are delays increasing over time?

---

## Project Structure

```
JohnWayneAirport-performance-analytics
│
├── data
│   └── daily flight data CSVs
│
├── notebooks
│   └── exploratory analysis and visualizations
│
├── py_files
│   ├── webscraper.py
│   └── main.py
│
├── dashboard
│   └── Power BI dashboard files
│
├── README.md
└── requirements.txt
```

---

## How to Run the Scraper

### 1. Clone the repository

```
git clone https://github.com/mtafoya-web/JohnWayneAirport-performance-analytics.git
cd JohnWayneAirport-performance-analytics
```

### 2. Create a virtual environment

```
python -m venv .venv
```

Activate the environment

Windows:

```
.venv\Scripts\activate
```

Mac/Linux:

```
source .venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the scraper

```
python py_files/main.py
```

The script will collect the latest flight data and export a CSV file into the `data/` directory.

---

## Dashboard (Power BI)

The collected dataset is used to build a Power BI dashboard showing:

* Delay trends
* Flight volume over time
* Route distribution
* Airline performance metrics

*Dashboard screenshots coming soon.*

---

## Technologies Used

Python
Pandas
Requests
Jupyter Notebook
Power BI
Git / GitHub

---

## Future Improvements

* Automate the scraper with a daily scheduler
* Store historical data in a database (PostgreSQL)
* Build automated delay detection alerts
* Deploy dashboards to a cloud environment
* Add machine learning models for delay prediction

---

## License

MIT License
