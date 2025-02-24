from django.urls import path
from . import views
import dictionary

urlpatterns = [
    path('<str:username>/dictionaries/', views.DictionariesList.as_view(), name="user_dictionaries"),
    path('<str:username>/newdictionary/', views.CreateDictionary.as_view()),
    path('<str:username>/<str:dictionary_name>/', views.DictionaryContent.as_view(), name="dictionary_content"),
]