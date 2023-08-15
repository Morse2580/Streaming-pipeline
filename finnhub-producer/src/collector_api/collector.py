import requests
from src.entities.entity_models import TradeEventMessage

"""
 def __init__(
            self, base_url, api_key
    ):
"""


class CollectorAPIClient:
    def __init__(self):
        self.base_url = "http://localhost:9000"
        self.endpoint = "v1/collector"
        self.headers = {
            "Content-Type": "application/json"
        }

    def post(
            self, data: TradeEventMessage
    ):
        url = f"{self.base_url}/{self.endpoint}"
        try:
            # Convert TradeEventMessage instance to a dictionary
            data_dict = data.model_dump()

            # Make the POST request
            response = requests.post(url, json=data_dict, headers=self.headers)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Failed to post data to {url}: {e}")
            return None
