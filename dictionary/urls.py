from django.urls import path
from . import views

urlpatterns = [
    path('dictionaries/<str:username>', views.get_dictionary_list)
]