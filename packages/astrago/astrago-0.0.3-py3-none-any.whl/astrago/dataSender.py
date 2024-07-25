import time
from typing import Dict
import requests
from . import val


class DataSender:
    def __init__(self):
        print(val.url)
        self.base_url = val.url
        self.start_time = time.time()

    def send_metric(self, data: Dict):
        url = f"{self.base_url}/api/v1/core/monitor/experiment"
        try:
            response = requests.post(url=url, json=data)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None
