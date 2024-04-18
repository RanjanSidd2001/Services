"""
URL configuration for Services project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from ServicesApp import views

urlpatterns = [
    path('Create/',views.save_model, name='create_view'),
    path('ViewModels/',views.view_model_details, name='view_models'),
    path('ModelList/',views.view_model_list, name='model_list'),
    path('Predict/',views.predict,name='predict'),
    path('ViewModelByCatogory/',views.view_model_by_category,name='categorylist')
]
