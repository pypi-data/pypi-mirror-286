from openai import OpenAI as oi
from .modelforce import ModelForce
from datetime import datetime
from .config import LF_ENDPOINT
class OpenAI:
    def __init__(self, api_key,latent_force_api_key,project_name):
        
        self.client = oi(api_key=api_key)
        self.latent_force_api_key=latent_force_api_key
        self.project_name=project_name
        self.model_force_instance = ModelForce(self.latent_force_api_key, self.project_name)

    def chat_completions(self, model_name,messages,lora_id=None):
       
        self.llm_input=None
        self.llm_output=None
        self.promt=None
        self.api_key=self.latent_force_api_key
        self.project_name=self.project_name
        self.message=messages
        self.model_name=model_name
        self.lora_id=lora_id


        answer=None
        return_response=None
        if model_name.startswith("latentforce/"):
            self.model_name=model_name[len("latentforce/"):]
            data={
                "model_name":self.model_name,
                "model_inputs":self.message,
                "project_name":self.project_name,
                "api_key": self.api_key
            }
            if self.lora_id is not None:
                data["lora_id"] = self.lora_id
            response=self.model_force_instance.latent_force_model_results(data)
            answer=response
            return_response=response
        else:

            response = self.client.chat.completions.create(
                model= self.model_name,
                messages=messages
                
            )
            return_response=response
            answer=response
            

        self.llm_output=answer
   
        data = {
            "api_key": self.latent_force_api_key,
            "project_name": self.project_name,
            "model_name": self.model_name,
            "messages":self.message,
            "output":self.llm_output,
            "score" : None
                }
        self.model_force_instance.log_llm_v1(data)
        return return_response

