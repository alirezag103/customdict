from django.urls import path
from . import views
import dictionary

urlpatterns = [
    path('dictionaries/', views.get_dictionaries_list, name="user_dictionaries"),
    path('<str:username>/newdictionary/', views.create_dictionary),
    path('<str:dictionary_name>/', views.get_dictionary_content, name="dictionary_content"),
    path('<str:dictionary_name>/addtranslation', views.add_translation, name="add_translation"),
]