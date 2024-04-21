import numpy as np

# Define a class Regression 
class Regression:
    # Constructor to initialize the Regression object
    def __init__(self) -> None:
        self.inputs = {}  # List to store input feature data
        self.output = None  # Variable to store the output feature data
        self.configuration = None  # Variable to store the model configuration
    
    # Method to initialize the regression model with input features, output feature, and model configuration
    def initialize(self, input_features, output_features, model_json_dict):
        self.inputs = input_features  # Set the input features
        self.output = output_features  # Set the output feature
        self.configuration = model_json_dict  # Set the model configuration
        
    # Method to execute the regression prediction
    def execute(self):
        prediction = self.predict_from_json()
        return prediction
    
    def predict_from_json(self):
    # Extract model information from the dictionary
        feature_columns = self.configuration['feature_columns']
        scaling_method = self.configuration['scaling_method']
        coefficients = np.array(self.configuration['coefficients'])
        intercept = self.configuration['intercept']
        scaler_params = self.configuration.get('scaler_params', None)

        # Scale the input data if scaling parameters are provided
        if scaling_method == 'StandardScaler' and scaler_params:
            mean_ = np.array(scaler_params['mean_'])
            scale_ = np.array(scaler_params['scale_'])
            input_values = [self.inputs[col] for col in feature_columns]
            input_scaled = (np.array(input_values) - mean_) / scale_
        elif scaling_method == 'MinMaxScaler' and scaler_params:
            min_ = np.array(scaler_params['min_'])
            max_ = np.array(scaler_params['max_'])
            input_values = [self.inputs[col] for col in feature_columns]
            input_scaled = (np.array(input_values) - min_) / (max_ - min_)
        else:
            input_scaled = [self.inputs[col] for col in feature_columns]  # No scaling

        # Make predictions
        prediction = np.dot(input_scaled, coefficients) + intercept
        return prediction

    
    # String representation method to describe the Regression class
    def __str__(self) -> str:
        return "Regression Class"
