from django.http import HttpResponseNotFound
from django.shortcuts import render

import dictionary
from .models import User, Dictionary

# Create your views here.

def get_dictionary_list(request, username):

    retrieve_user = User.objects.filter(username=username)
    
    if retrieve_user.exists():
        requested_user = retrieve_user[:1].get()
        dictionary_list = Dictionary.objects.filter(user=requested_user)\
            .select_related('source_language')\
            .values('dictionary_name', 'source_language_id')
        return render(request, 'dictionaries.html', {'dictionaries': dictionary_list,
                                                     'user': requested_user})
    else:
        return render(request, HttpResponseNotFound("User name not found!"))