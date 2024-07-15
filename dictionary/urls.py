from django.urls import path
from . import views
import dictionary

urlpatterns = [
    path('<str:username>/dictionaries/', views.get_dictionaries_list, name="user_dictionaries"),
    path('<str:username>/newdictionary/', views.create_dictionary),
    path('<str:username>/<str:dictionary>/', views.get_dictionary_content, name="dictionary_content"),
    path('<str:username>/<str:dictionary>/addtranslation', views.add_translation, name="add_translation"),
]