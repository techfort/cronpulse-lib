import requests
from datetime import datetime

class CronPulse:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.cronpulse.com"  # Replace with your API URL

    def create_monitor(self, name: str, interval: int, email: str, expires_at: datetime):
        response = requests.post(
            f"{self.base_url}/monitors",
            json={"name": name, "interval": interval, "email": email, "expires_at": expires_at.isoformat()},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return Monitor(response.json()["id"], self.api_key)

class Monitor:
    def __init__(self, monitor_id, api_key):
        self.monitor_id = monitor_id
        self.api_key = api_key

    def ping(self):
        response = requests.post(
            f"{self.base_url}/monitors/{self.monitor_id}/ping",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()

    def delete(self):
        response = requests.delete(
            f"{self.base_url}/monitors/{self.monitor_id}",
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
