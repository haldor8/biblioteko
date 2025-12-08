import os
from datetime import datetime


class Log:
    """
    Centralized logging utility.
    Generates a unique log file per execution.
    """

    LOG_DIR = "../../data/sequestre/logs"

    # Generate unique filename at import time
    _unique_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    LOG_FILE = os.path.join(LOG_DIR, f"copyright_check_{_unique_id}.log")

    # Ensure directory exists
    os.makedirs(LOG_DIR, exist_ok=True)

    @staticmethod
    def write(message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {message}\n"

        with open(Log.LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)

        print(entry.strip())