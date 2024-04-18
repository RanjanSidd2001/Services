import numpy as np

class RandomForest:
    def __init__(self) -> None:
      self.inputs= {}
      self.output=None
      self.configuration=None
    
    def initialize(self,input_features,output_features,model):
        self.inputs = input_features
        self.output = output_features
        self.configuration =model
        
    
    def execute(self):
        
        prediction = self.predict_with_forest()
        return prediction
        # variable_manager.update_variable_value(self.output, prediction)
   
    def predict_with_forest(self):
        predictions = []
        for tree_json in self.configuration:
            predictions.append(self.predict_with_tree(tree_json))
        # Aggregate predictions (e.g., take the mean for regression)
        return np.mean(predictions) # <------aggregate of Decision Tree's predictions
    
    def predict_with_tree(self,tree_json):
        def recurse(node):
            if 'value' in node:
                return node['value']
            else:
                feature_name = node['name']
                threshold = node['threshold']
                if self.inputs[feature_name] <= threshold:
                    return recurse(node['left'])
                else:
                    return recurse(node['right'])
        return recurse(tree_json)