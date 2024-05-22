import time
import requests
from datetime import datetime
import logging
import os


class UptimeLogger:
    def __init__(self, status_url: str, log_url: str, server_id: str):
        self.status_url = status_url
        self.log_url = log_url
        self.server_id = server_id
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def get_status_code(self) -> int:
        try:
            response = requests.get(self.status_url)
            response.raise_for_status()
            return response.status_code
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching status URL: {e}. Retrying in 20 seconds...")
            time.sleep(20)
            try:
                response = requests.get(self.status_url)
                response.raise_for_status()
                return response.status_code
            except requests.exceptions.RequestException as e:
                logging.error(f"Retry failed: {e}")
                return None

    def post_uptime(self) -> None:
        status_code = self.get_status_code()
        if status_code == 200:
            log = {
                "server_id": self.server_id,
                "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "status": True
            }
            try:
                response = requests.post(self.log_url, json=log)
                response.raise_for_status()
                logging.info(f"Uptime logged successfully: {response.json()}")
            except requests.exceptions.RequestException as e:
                logging.error(f"Error posting uptime: {e}")
        else:
            logging.warning("Failed to get status code 200 from the status URL.")


# Example usage:
if __name__ == "__main__":
    # It's good practice to use environment variables for sensitive or configurable information.
    status_url = os.getenv("STATUS_URL", "localhost:8000/uptime")
    log_url = os.getenv("LOG_URL", "localhost:8000/log_uptime")
    server_id = os.getenv("SERVER_ID", "test")

    logger = UptimeLogger(status_url=status_url, log_url=log_url, server_id=server_id)
    logger.post_uptime()
