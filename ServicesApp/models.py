from django.db import models

class MLOPS(models.Model):
    # Stores the category of the ML model
    model_category = models.CharField(max_length=100)

    # Stores the name of the ML model
    model_name = models.CharField(max_length=100)

    # Records the timestamp when the ML model entry was first created (set automatically)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    # Stores additional metadata in JSON format (e.g., training parameters)
    metadata = models.JSONField()

    # Stores the ML model details in JSON format (e.g., model structure, weights)
    model = models.JSONField()
    
    # Stores the username of the person who created the ML model entry
    created_user = models.CharField(max_length=100)

    # Stores a brief description of the ML model
    model_description = models.CharField(max_length=200)
    
    # Records the timestamp when the ML model entry was last modified (set automatically)
    modified_timestamp = models.DateTimeField(auto_now_add=True)
    
    # Stores the username of the person who last modified the ML model entry
    modified_user = models.CharField(max_length=100)
    
    
    def __str__(self) -> str:
        return f"""
    Model name = {self.model_name}
    Model Category = {self.model_category}
    """