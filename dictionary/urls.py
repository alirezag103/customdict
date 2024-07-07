from django.urls import path
from . import views

urlpatterns = [
    path('dictionaries/<str:user_name>', views.get_dictionary_list)
]