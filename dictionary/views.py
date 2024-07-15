import keyword
from django import forms
from django.http import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from dictionary.forms import AddTranslationFrom, NewDictionaryForm
from .models import Translation, User, Dictionary
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

# Create your views here.

def retrieve_user_by(*, username, error_msg="Username not found!"):
    try:
        user = User.objects.get(username=username)
        return user
    except ObjectDoesNotExist:
        return HttpResponseNotFound(error_msg)

def get_dictionaries_list(request, username):

    retrieve_user = User.objects.filter(username=username)[:1]
    
    if retrieve_user.exists():
        requested_user = retrieve_user.get()
        dictionary_list = Dictionary.objects.filter(user=requested_user)\
            .select_related('source_language')\
            .values('dictionary_name', 'source_language_id')
        
        template_name = 'dictionaries.html'
        template_context = {'dictionaries': dictionary_list,
                            'user': requested_user}
        
        return render(request, template_name, template_context)
    else:
        return HttpResponseNotFound("Username not found!")
    

def create_dictionary(request, username):
    if request.method == "POST":
        form = NewDictionaryForm(request.POST)

        user_dictionaries = User.objects.select_related("dictionary") \
            .values("id", "dictionary__dictionary_name").filter(username=username)

        form.is_valid()
        new_dictionary_name = form.cleaned_data["dictionary_name"]
        old_dictionary_names = [item.get("dictionary__dictionary_name") for item in user_dictionaries]

        if old_dictionary_names == [None] \
            or new_dictionary_name not in old_dictionary_names:

            with transaction.atomic():
                new_dictionary = Dictionary()
                new_dictionary.dictionary_name = form.cleaned_data["dictionary_name"]
                new_dictionary.source_language = form.cleaned_data["source_language"]
                new_dictionary.target_language = form.cleaned_data["target_language"]
                new_dictionary.user_id = user_dictionaries[0].get("id")
                new_dictionary.save()

            # return HttpResponse("Succeeded!")
            return redirect(reverse("user_dictionaries", kwargs={'username': username}))
        else:
            raise ValueError("Dictionary name already exists")
            

    else:
        try:
            user = User.objects.get(username=username)
            form = NewDictionaryForm()

            return render(request, "new_dictionary.html", {"form": form})
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Username not found!")
        

def get_dictionary_content(request, username, dictionary_name):
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return HttpResponseNotFound("Username not found!")
    try:
        user_dictionary = Dictionary.objects.filter(user=user).get(dictionary_name=dictionary_name)
    except ObjectDoesNotExist:
        return HttpResponse("The dictionary does not exist! <br>or You can not access that!")
    
    else:
        dictionary_content = Translation.objects.filter(dictionary=user_dictionary)
        template_name = 'dictionary.html'
        template_context = {
            'dictionary': user_dictionary,
            'translations': dictionary_content,
        }
        return render(request, template_name, template_context)
    


def add_translation(request, username, dictionary_name):

    try:
        requested_user = User.objects.filter(username=username).get()
        try:
            requested_dictionary = Dictionary.objects.filter(user=requested_user, dictionary_name=dictionary_name).get()

            if request.method == "POST":
                form = AddTranslationFrom(request.POST)
                form.is_valid()
                try:
                    current_translations = Translation.objects \
                        .filter(dictionary=requested_dictionary, keyword=form['keyword']).get()
                    return HttpResponseBadRequest(f'Keyword "{current_translations.keyword}" already exists!', status_code=400)
                except ObjectDoesNotExist:
                    pass
                Translation.objects.create(
                    dictionary=requested_dictionary,
                    keyword=form.cleaned_data['keyword'],
                    translation=form.cleaned_data['translation'],
                )
            else:
                form = AddTranslationFrom()

                template_name = 'new_translation.html'
                template_context = {
                'form': form,
                'dictionary':requested_dictionary,
            }
            return render(request, template_name, template_context)
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Dictionary Not Found!")
    except ObjectDoesNotExist:
        return HttpResponseNotFound("User Not Found!")