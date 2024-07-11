from django.urls import path
from . import views

urlpatterns = [
    path('<str:username>/dictionaries/', views.get_dictionaries_list),
    path('<str:username>/newdictionary/', views.create_dictionary),
]