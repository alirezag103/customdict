from django.http import HttpResponseNotFound
from django.shortcuts import render
from dictionary.forms import NewDictionaryForm
from .models import User, Dictionary
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def retrieve_user_by(*, username, error_msg="Username not found!"):
    try:
        user = User.objects.get(username=username)
        return user
    except ObjectDoesNotExist:
        return HttpResponseNotFound(error_msg)

def get_dictionary_list(request, username):

    retrieve_user = User.objects.filter(username=username)[:1]
    
    if retrieve_user.exists():
        requested_user = retrieve_user.get()
        dictionary_list = Dictionary.objects.filter(user=requested_user)\
            .select_related('source_language')\
            .values('dictionary_name', 'source_language_id')
        return render(request, 'dictionaries.html', {'dictionaries': dictionary_list,
                                                     'user': requested_user})
    else:
        return HttpResponseNotFound("Username not found!")
    

def create_dictionary(request, username):
    if request.method == "POST":
        form = NewDictionaryForm(request.POST)
        # if form.is_valid():
        if False:
            form.save()
            return redirect("welcome")
        # pass

    else:
        try:
            user = User.objects.get(username=username)
            form = NewDictionaryForm()
            return render(request, "new_dictionary.html", {"form": form})
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Username not found!")
        

    