import requests
import base64
from .config import LF_ENDPOINT




class AgentForce:
    def __init__(self,latent_force_api_key):
        
        self.backend_url=LF_ENDPOINT
        self.latent_force_api_key=latent_force_api_key
   
    def load_and_process_image(self,image_path):

        with open(image_path, 'rb') as image_file:
                image = image_file.read()

        encoded_image = base64.b64encode(image).decode('utf-8')

        return encoded_image
         

    def agent_force_model_results(self, data):

            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }

            url = f"{self.backend_url}/api/get-agent-predictions"
            response = requests.post(url, json=data, headers=headers,timeout=100)
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Failed to get prediction. Status Code: {response.status_code}"}


    def process(self, model_name,agent_inputs=None):
        if model_name is None:
            return "No Model name  ! "
        if agent_inputs is None:
                return "No agent inputs ! "
             
        self.api_key=self.latent_force_api_key
        self.model_name=model_name
        self.agent_inputs=agent_inputs
        data = {
            "api_key": self.latent_force_api_key,
            "model_name": self.model_name,
            "agent_inputs":self.agent_inputs,
                }
 
        response=self.agent_force_model_results(data)
   

        return response



