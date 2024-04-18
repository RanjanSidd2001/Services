from sklearn.neural_network import MLPRegressor
import json
import numpy as np

class ANN:
    def __init__(self) -> None:
      self.inputs= []
      self.output=None
      self.configuration=None
      self.model = None
    
    def initialize(self,input_features,output_features,model):
        self.inputs = input_features
        self.output = output_features
        self.configuration =model
        
        self.load_model_from_json()
    
    def load_model_from_json(self):
        data = json.loads(self.configuration)

        # Extract model parameters
        architecture = data['model_params']['architecture']
        out_activation_ = data['model_params']['out_activation_']
        optimizer = data['model_params']['optimizer']
        coefs = data['model_params']['coefs']
        intercepts = data['model_params']['intercepts']
        n_layers = data['model_params']['n_layers']

        self.model = MLPRegressor(hidden_layer_sizes=architecture, activation=out_activation_,
                                          solver=optimizer, max_iter=10000, random_state=42)

        # Set model coefficients and intercepts
        self.model.coefs_ = [np.array(layer_coef) for layer_coef in coefs]
        self.model.intercepts_ = [np.array(layer_intercept) for layer_intercept in intercepts]
        self.model.n_layers_ = n_layers
        self.model.out_activation_ = out_activation_
    
       
    def execute(self, variable_manager):
        
        prediction = self.model.predict(self.inputs)
        variable_manager.update_variable_value(self.output, prediction)


def __str__(self) -> str:
        return"""
        ANN Class
    """