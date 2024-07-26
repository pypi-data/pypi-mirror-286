import requests

class Prenzl:
    def __init__(self, api_key,base_url):
        self.api_key = api_key
        self.base_url = base_url

    def prenzl_observe(self, data):
        headers = {"Content-Type": "application/json"}
        payload = {"apiKey": self.api_key, "data": data}
        response = requests.post(f"{self.base_url}/log", json=payload, headers=headers)
        
        if response.ok:
            try:
                return response.json()
            except requests.JSONDecodeError:
                return {"error": "Response is not valid JSON", "content": response.text}
        else:
            return {"error": f"Request failed with status code {response.status_code}", "content": response.text}