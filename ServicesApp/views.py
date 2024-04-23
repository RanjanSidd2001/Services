from django.http import JsonResponse
from .models import MLOPS
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ServicesApp.modules.regression import Regression
from ServicesApp.modules.decision_tree import DecisionTree
from ServicesApp.modules.random_forest import RandomForest

@csrf_exempt # This decorator exempts the view from CSRF verification.
@api_view(['POST'])
def save_model(request):
    # This view function handles the creation of a new model instance.
    if request.method == 'POST':  # Check if the request method is POST.
        try:
            # Load the JSON data from the request body.
            data = json.loads(request.body)
            
            # Extract the relevant information from the data.
            model_name = data.get('model_name')
            model_category = data.get('model_category')
            metadata = data.get('metadata')
            created_user = data.get('created_user')
            model = data.get('model')
            model_description = data.get('model_description')
            modified_timestamp = data.get('modified_timestamp')
            modified_user = data.get('modified_user')
            
            # Create a new MLOPS instance with the extracted data.
            _model = MLOPS(
                model_name=model_name,
                model_category=model_category,
                metadata=metadata,
                model=model,
                created_user=created_user,
                model_description=model_description,
                modified_timestamp=modified_timestamp,
                modified_user=modified_user
            )
            _model.save()  # Save the new instance to the database.

            # Return a success response.
            return JsonResponse({'message': 'POST request processed successfully'})
        except Exception as e:
            # If an error occurs, log it and return an error response.
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=500)
    else:
        # If the request method is not POST, return an error response.
        return JsonResponse({'error': 'Unsupported HTTP method'}, status=405)
@api_view(['GET'])
def view_model_details(request):
    # This view handles the GET request for viewing a specific ML model's details.
    if request.method == 'GET':
        try:
            # Attempt to retrieve the model by its name from the query parameters.
            model_name = request.GET.get('model_name')
            # Query the MLOPS model for the given model name.
            _model = MLOPS.objects.get(model_name=model_name)
            # Prepare the data dictionary with the model's details.
            data = {
                'model_name': _model.model_name,  # Name of the model.
                'model_category': _model.model_category,  # Category of the model.
                'metadata': _model.metadata,  # Metadata associated with the model.
                'created_user': _model.created_user,  # User who created the model.
                'model_description': _model.model_description,  # Description of the model.
                'modified_timestamp': _model.modified_timestamp,  # Timestamp of last modification.
                'modified_user': _model.modified_user  # User who last modified the model.
            }
            # Return the data as a JSON response.
            return JsonResponse(data)
        except MLOPS.DoesNotExist:
            # If the model is not found, return a 404 error in JSON format.
            return JsonResponse({'error': 'Model not found'}, status=404)
        except Exception as e:
            # If any other exception occurs, print the error and return a 500 error in JSON format.
            print(f"An error occurred: {str(e)}")
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=500)

@api_view(['GET'])        
def view_model_list(request):
    # This view returns a list of all ML model names stored in the database.
    if request.method == 'GET':  # Check if the request method is GET.
        try:
            # Query the database to retrieve all instances of the MLOPS model.
            all_models = MLOPS.objects.all()
            # Initialize an empty list to store the names of the models.
            model_names_list = []
            # Iterate over each model instance retrieved from the database.
            for _model in all_models:
                # Append the name of the model to the model_names_list.
                model_names_list.append(_model.model_name)
            # Convert the list of model names to JSON format and return it as a response.
            return JsonResponse({'models': model_names_list})
        except Exception as e:
            # If an exception occurs, print the error message to the console.
            print(f"An error occurred: {str(e)}")
            # Return a JSON response with an error message and a 500 status code indicating a server error.
            return JsonResponse({'error': 'An error occurred while processing the request'}, status=500)
        
        
@csrf_exempt # This decorator exempts the view from CSRF verification.        
def predict(request):
    # This function defines a view that handles predictions based on the model category.

    if request.method == 'POST':  # Check if the request method is POST.
        
        # Parse the JSON data from the request body.
        data = json.loads(request.body)

        # Retrieve the 'model_name' from the parsed data.
        model_name = data.get('model_name')
        
        # Retrieve the 'inputs' from the parsed data, which are the features for prediction.
        inputs = data.get('inputs')

        # Retrieve the 'output' from the parsed data, which is the target variable for prediction.
        output = data.get('output')
        
        # Query the MLOPS model to get the entry that matches the given model name.
        selected_model = MLOPS.objects.get(model_name=model_name)
        

    if selected_model.model_category == 'Regression':

        # Create an instance of the Regression class
        regressor = Regression()
        
        # Initialize the regressor with inputs, output, and configuration
        regressor.initialize(inputs, output, selected_model.model)
        
        # Execute the regression to get the prediction
        prediction = regressor.execute()
        
        # Return the prediction as a JSON response
        return JsonResponse({'predictions': prediction})

    # Check if the model category is 'RandomForest'.
    elif selected_model.model_category == 'RandomForest':

        # Create an instance of the RandomForest class.
        rf = RandomForest()
        
        # Initialize the random forest with inputs, output, and the model details.
        rf.initialize(inputs, output, selected_model.model)
        
        # Execute the random forest model to get the prediction.
        prediction = rf.execute()
        
        return JsonResponse({'Prediction': prediction})
        
    # Check if the model category is 'DecisionTree'.
    elif selected_model.model_category == 'DecisionTree':
        
        # Create an instance of the DecisionTree class.
        dectree = DecisionTree()
        
        # Initialize the decision tree with inputs, output, and the model details.
        dectree.initialize(inputs, output, selected_model.model)
        
        # Execute the decision tree model to get the prediction.
        prediction = dectree.execute()
        
        return JsonResponse({'Prediction': prediction})
            
@api_view(['GET'])
# This decorator specifies that this view function only accepts GET requests.
def view_model_by_category(request):
    # This function defines a view that returns models by their category.

    if request.method == 'GET':
        # Check if the incoming request is a GET request.

        try:
            # Try block to attempt the following operations.
            # Retrieve the 'model_category' parameter from the query string of the GET request.
            model_category = request.GET.get('model_category')
            
            # Query the MLOPS model to get all entries that match the given category.
            models = MLOPS.objects.filter(model_category=model_category)
            
            # Create a list of model names from the queried models.
            model_names = [model.model_name for model in models]
            
            # Return a successful HTTP response with the list of model names.
            return Response({'models': model_names})
            
        except MLOPS.DoesNotExist:
            # If no model is found for the given category, handle the DoesNotExist exception.

            return Response({'error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)
            # Return an HTTP 404 Not Found response with an error message.

        except Exception as e:
            # Catch any other exceptions that may occur.

            print(f"An error occurred: {str(e)}")
            # Print the error message to the console or log.

            return Response({'error': 'An error occurred while processing the request'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            # Return an HTTP 500 Internal Server Error response with an error message.
        
