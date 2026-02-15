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
    # Schedule backup
    backup_interval = config.get("backup_interval_minutes", 1)
    schedule.every(backup_interval).minutes.do(create_backup)

    # Schedule cleanup
    cleanup_interval = config.get("cleanup_interval_minutes", 60)
    schedule.every(cleanup_interval).minutes.do(clean_old_backups)

    print(f"⏳Backup Scheduler Started (every {backup_interval} minute(s))")
    logging.info("Backup scheduler started")

    while True:
        schedule.run_pending()
        time.sleep(1)


def clean_old_backups():
    MAX_BACKUPS = 3 

    files = os.listdir(BACKUP_FOLDER)
    zip_files = [f for f in files if f.endswith(".zip")]

    filename_with_modified_time = {}

    for f in zip_files:
        modified_time = os.path.getmtime(os.path.join(BACKUP_FOLDER, f))
        filename_with_modified_time[f] = modified_time
        
    dict_items = filename_with_modified_time.items()
    filename_with_time_list = list(dict_items)
    
    sorted_files = sorted(filename_with_time_list, key=lambda x: x[1])
    
    if len(sorted_files) <= MAX_BACKUPS:
        print("🟢No Old backups to delete")
        return

    files_to_delete = sorted_files[:-MAX_BACKUPS]

    # Actual deletion
    for filename, _ in files_to_delete:
        file_path = os.path.join(BACKUP_FOLDER, filename)
        os.remove(file_path)
        logging.info(f"Deleted old backup: {filename}")
        print(f"🗑️ Deleted old backup: {filename}")


if __name__ == "__main__":
    run_scheduler()
    