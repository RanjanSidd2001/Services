import numpy as np

# Define a class named 'Regression' to encapsulate the regression model functionality
class Regression:
    # Constructor to initialize the Regression object
    def __init__(self) -> None:
        self.inputs = []  # List to store input feature data
        self.output = None  # Variable to store the output feature data
        self.configuration = None  # Variable to store the model configuration
    
    # Method to initialize the regression model with input features, output feature, and model configuration
    def initialize(self, input_features, output_features, model):
        self.inputs = input_features  # Set the input features
        self.output = output_features  # Set the output feature
        self.configuration = model  # Set the model configuration
        
    # Method to execute the regression prediction
    def execute(self):
        # Check if the configuration is a dictionary or a JSON string
        # If it's a JSON string, convert it to a dictionary using json.loads(self.configuration)
        scaling_method = self.configuration['scaling_method']  # Retrieve the scaling method from the configuration
        coefficients = self.configuration['coefficients']  # Retrieve the model coefficients
        intercept = self.configuration['intercept']  # Retrieve the model intercept
        scaler_params = self.configuration['scaler_params']  # Retrieve the scaler parameters

        # Scale the input data according to the specified scaling method
        if scaling_method == 'standard':
            # Standard scaling: (data - mean) / scale
            scaled_data = (self.inputs - scaler_params['mean']) / scaler_params['scale']
        elif scaling_method == 'min_max':
            # Min-max scaling: (data - data_min) / (data_max - data_min)
            data_min = scaler_params['data_min'][0]  # Extract the minimum value from the list
            data_max = scaler_params['data_max'][0]  # Extract the maximum value from the list
            scaled_data = (self.inputs - data_min) / (data_max - data_min)
        else:
            # If the scaling method is not supported, print an error message and return None
            print("Unsupported scaling method.")
            return None

        # Calculate the prediction using the scaled data, coefficients, and intercept
        prediction = np.dot(coefficients, scaled_data.T) + intercept  # Transpose scaled_data to match the shape
        return prediction
        
        # Update the output variable in the variable manager with the prediction
        # variable_manager.update_variable_value(self.output, prediction) 

    # String representation method to describe the Regression class
    def __str__(self) -> str:
        return "Regression Class"