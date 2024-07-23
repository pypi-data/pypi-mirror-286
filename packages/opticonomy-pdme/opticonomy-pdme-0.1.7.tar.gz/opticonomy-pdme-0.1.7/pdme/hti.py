import requests

class HuggingFaceClient:
    def __init__(self, api_token, model_name):
        self.api_token = api_token
        self.model_name = model_name
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def post(self, payload):
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        return response.json()
