import os
import shutil
from datetime import datetime
import json
import logging

import schedule 
import time

# load config
with open("config.json") as f:
    config = json.load(f)

SOURCE_FOLDER = config["source_folder"]
BACKUP_FOLDER = config["backup_folder"]

# logging setup
logging.basicConfig(
    filename="logs/backup.log", 
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
    )

def create_backup():
    try: 
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_name = f"backup_{timestamp}"
        backup_path = os.path.join(BACKUP_FOLDER, backup_name)

        shutil.make_archive(backup_path, 'zip', SOURCE_FOLDER)

        logging.info("Backup successful!")
        print("✅Backup created successful!")
    
    except Exception as e:
        logging.error(f"Backup failed: {e}")
        print(f"❌Backup failed!: {e}")

def run_scheduler():
    schedule.every().day.at("22:00").do(create_backup)

    print("⏳Backup Scheduler Started...")
    logging.info("Backup scheduler started")

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    run_scheduler()
