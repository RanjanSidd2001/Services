"""
Class to get authentication token from the API
This token will be used for reading and writing datausing API
"""

import requests
import yaml
import os

class AuthenticationService:

    def __init__(self):
            self.token_url = None
            self.username = None
            self.password = None
            self.read_from_config()
            self.token = self.get_token()

    def get_token(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = requests.post(self.token_url, data=data)
        response.raise_for_status()
        token = response.json()['access_token']
        return token
    
    def read_from_config(self):
        current_directory= os.path.dirname(os.path.realpath(__file__))
        configure_path=os.path.join(current_directory, 'configure.yaml')
    
        with open(configure_path, 'r') as file:
            config = yaml.safe_load(file)
        self.token_url = config['token_url'] 
        self.username = config['username']
        self.password = config['password']
        

auth = AuthenticationService()
print(auth.token)