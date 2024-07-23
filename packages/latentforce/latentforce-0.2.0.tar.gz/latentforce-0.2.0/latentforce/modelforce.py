import requests
from .config import LF_ENDPOINT



import base64
from PIL import Image
import io

class ModelForce:
    def __init__(self, api_key, project_name):
        self.api_key = api_key
        self.project_name = project_name
        # self.backend_url = "http://app.latentforce.ai/log"  # URL of your Flask app logging endpoint
        self.backend_url = LF_ENDPOINT  # URL of your Flask app logging endpoint


    def log_llm_v1(self, data):

        response = requests.post(f"{self.backend_url}/api/log_llm_v1", json=data)

        
        if response.status_code == 200:
            print("Logged Successfully..")
        else:
            error_message = response.json().get('error', 'No error message provided')
            print(f"Error: {error_message}. The data is not Logged ")
            
    def latent_force_model_results(self, data):

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            url = f"{self.backend_url}/api/model_predict"
            response = requests.post(url, json=data, headers=headers,timeout=100)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get prediction. Status Code: {response.status_code}"}

