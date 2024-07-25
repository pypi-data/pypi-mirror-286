from typing import List
import requests

base_url = "https://api.saldor.com"


class SaldorClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def scrape_url(self, url: str, params: dict) -> List[str]:
        headers = {"x-api-key": self.api_key, "Content-Type": "application/json"}

        payload = {"url": url}

        # Use the base_url variable
        response = requests.post(f"{base_url}/scrape", json=payload, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Assuming the response contains a JSON array of strings
            return response.json()
        else:
            # Handle error appropriately
            response.raise_for_status()

        return []
