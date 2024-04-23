# """
# Class to fetch data from hierarchy
# NOTE: 
# 1. Authentication type needs an update
# 2. Overall Aggregation to be added
# 3. Timezone parameter for calculating time range is hardcoded atm (US/Eastern)
# 4. Need to account for custom time range
# """
# # IMPORTS
# import requests
# import pandas as pd
# from DateTimeFilter import TimeRange
# import json
# import yaml

# class RequestGenerator:
#     """
#     Class to generate parameters from config, to pass to the URL
#     # TODO Add conditional filter
#     """
#     @staticmethod
#     def generate_param(id, start_date, end_date, condition):
#         return {'id': id, 
#                 'from_date': start_date,
#                 'to_date': end_date,
#                 'condition': condition}
    

# class Reader:
#     """
#     Class to retrieve data and convert them into python dataframes from
#     incoming JSON requests (Configurations). 
#     """
#     def __init__(self, token):
#         self.data_url = self.read_from_config()
#         self.token = token
    
#     def read_from_config(self):
#         with open('config.yaml', 'r') as file:
#             config = yaml.safe_load(file)
#         return config['data_url']

#     def retrieve_data_from_url(self, config):
#         """
#         Function to build a request to get the data from DataService API
#         """

#         headers = {'Content-Type': 'application/json',
#                    'Authorization': f'Bearer {self.token}'}
        
#         # Fetching from Config - JSON
#         # Might need to work on conditions to get it to specific format
#         # Need to add data aggregation to the config
#         time_range = config.get('time_range')
#         start_date, end_date = TimeRange.get_range(time_range)
#         response = requests.get(self.data_url,
#                                 params=RequestGenerator.generate_param(config.get('id'),
#                                 start_date,
#                                 end_date,
#                                 config.get('condition')),
#                                 headers=headers)
        
#         if response.status_code == 200:
#             # Convert Response to Dataframe
#             converted_dataframe = self.json_to_dataframes(response.json())
#             return converted_dataframe
        
#         else:
#             print(f"Failed to retrieve data from the URL: {response.content}")
#             return None

#     def json_to_dataframes(self, jsonData):
#         """
#         Convert the JSON Response to DataFrame with multiple columns

#         EXAMPLE JSON FROM SERVICE:
#         {
#         "data": {
#             "30": [
#                 {
#                     "date_time": "2024-03-25T00:00:00",
#                     "value": 432.06
#                 },
#                 {
#                     "date_time": "2024-03-25T00:05:00",
#                     "value": 265.25
#                 }
#             ],
#             "31": [
#                 {
#                     "date_time": "2024-03-25T00:00:00",
#                     "value": 5.95
#                 },
#                 {
#                     "date_time": "2024-03-25T00:05:00",
#                     "value": 5.08
#                 }
#             ]
#         },
#         "param_mapping": {
#             "30": "NCV-01_TUR_Active_Power_Generation_FiveMinutes_Avg",
#             "31": "NCV-01_NAC_Wind_Speed_Outside_FiveMinutes_Avg"
#         }
#         }
#         """
#         dataframes = {}
#         # Check the type of input passed to the function
#         # if jsonData is a string load it using json.loads
#         # else pass directly

#         if isinstance(jsonData, str):
#             json_string = json.loads(jsonData)
#         elif isinstance(jsonData, dict):
#             json_string = jsonData
#         else:
#             raise ValueError("JSON Data must be a string or a dictionary.")
        
#         data = json_string.get('data')

#         for tag in data:
#             # Create a DataFrame for each tag
#             tag_df = pd.DataFrame(data[tag])
#             # Convert 'date_time' to datetime and set as index
#             tag_df['date_time'] = pd.to_datetime(tag_df['date_time'])
#             tag_df.set_index('date_time', inplace=True)
#             # Rename the 'value' column to the tag name
#             tag_df.rename(columns={'value': tag}, inplace=True)
#             dataframes[tag] = tag_df
        
#         # Concat all dataframes
#         data = pd.concat(dataframes.values(), axis=1)

#         return data