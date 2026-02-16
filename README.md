# Automated Backup Manager

Automated Backup Manager is a Python-based CLI tool that automatically creates scheduled backups of a specified folder, compresses them, and manages backup retention by deleting old backups based on configurable limits.

---

## Why This Project?

Manual backups are easy to forget and inefficient to manage. This project automates the entire backup lifecycle by:
- Running backups at fixed intervals
- Compressing files to save storage
- Automatically cleaning up old backups
- Allowing full control through a configuration file

It mimics how real-world backup systems work at a basic level.

---

## Features

- Scheduled automated backups
- ZIP compression for backups
- Configurable backup and cleanup intervals
- Automatic deletion of old backups
- Detailed logging of operations
- CLI-based execution

---

## Tech Stack

- Python 3
- schedule
- shutil
- os
- logging
- json

---

## Project Structure

automated-backup-manager/
│
├── backend/
│ ├── backup.py
│ ├── config.json
│ └── logs/
│ └── backup.log
│
├── backups/
├── data/
└── README.md



---

## Configuration

All settings are controlled using `config.json`.

Example:

```json
{
  "source_folder": "data",
  "backup_folder": "backups",
  "backup_format": "zip",
  "backup_interval_minutes": 1,
  "cleanup_interval_minutes": 60,
  "max_backups": 5
}
