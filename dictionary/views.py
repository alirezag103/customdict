from django.http import HttpResponse, HttpResponseNotFound
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

        user_dictionaries = User.objects.select_related("dictionary") \
            .values("id", "dictionary__dictionary_name").get(username=username)
        
        form.is_valid()
        new_dictionary_name = form.cleaned_data["dictionary_name"]
        old_dictionary_names = user_dictionaries.get("dictionary__dictionary_name")
        # if form.is_valid():
        if old_dictionary_names is None \
            or new_dictionary_name not in old_dictionary_names:

            form.cleaned_data['user'] = user_dictionaries.get("id")
            # raise IndexError(form.cleaned_data)
            form.save()
            return HttpResponse("Succeeded!")
        else:
            raise ValueError("Dictionary name already exists")
            
            # return redirect("welcome")

    else:
        try:
            user = User.objects.get(username=username)
            form = NewDictionaryForm()
            return render(request, "new_dictionary.html", {"form": form})
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Username not found!")
        

    