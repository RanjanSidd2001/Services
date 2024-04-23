"""
Class to write data to Hierarchy
Uses Authentication token to write a single value to Hierarchy's computed tag
"""

import requests
import yaml

class Writer:
    def __init__(self, token) -> None:
        self.data_url = self.read_from_config()
        self.token = token

    def read_from_config(self):
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config['data_url']

    def write_data(self, id, value):
        headers = {'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'}
        data = {'id': id, 'value': value}
        response = requests.post(self.data_url, headers=headers, json=data)
        response.raise_for_status()

        if response.status_code == 200:
            return "Data written successfully"
        else:
            return f"Failed to write data: {response.content}"