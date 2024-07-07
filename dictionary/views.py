from django.http import HttpResponseNotFound
from django.shortcuts import render

import dictionary
from .models import User, Dictionary

# Create your views here.

def get_dictionary_list(request, user_name):

    requested_user = User.objects.filter(_username=user_name)
    
    if requested_user.exists():
        dictionary_list = Dictionary.objects.filter(user__in=requested_user)
        return render(request, 'dictionaries.html', {'dictionaries': dictionary_list,
                                                     'user': requested_user})
    else:
        return render(request, HttpResponseNotFound("User name not found!"))