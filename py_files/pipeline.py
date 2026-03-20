from webscraper import Webscraper
from clean_data import Cleandata
from datetime import datetime
import logging 
from apscheduler.schedulers.blocking import BlockingScheduler
from pathlib import Path


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

DATA_DIR = Path("./data")


def run_pipeline():
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)

        today = datetime.today().strftime("%Y-%m-%d")
        filename = f"JohnWayneFlights_{today}.csv"
        file_path = DATA_DIR / filename

        logging.info("Starting pipeline")

        scraper = Webscraper(SNA_URL_API, HEADERS)
        scraper.run()

        cleaner = Cleandata(str(file_path))
        cleaner.run()

        logging.info("Pipeline completed successfully")

    except Exception as e:
        logging.exception(f"Pipeline failed: {e}")


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_pipeline, "cron", hour=23, minute=59)

    try:
        logging.info("Scheduler started")
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler stopped")