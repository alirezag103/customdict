import keyword
from django import forms
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from dictionary.forms import AddTranslationFrom, NewDictionaryForm
from .models import Translation, User, Dictionary
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, models

# Create your views here.

def retrieve_user_by(*, username, error_msg="Username not found!"):
    try:
        user = User.objects.get(username=username)
        return user
    except ObjectDoesNotExist:
        return HttpResponseNotFound(error_msg)


class DictionariesList(View):

    def get(self, request, username):
        retrieve_user = User.objects.filter(username=username)[:1]
        
        if retrieve_user.exists():
            requested_user = retrieve_user.get()
            dictionary_list = Dictionary.objects.filter(user=requested_user) \
                .values('dictionary_name')
            
            template_name = 'dictionaries.html'
            template_context = {'dictionaries': dictionary_list,
                                'user': requested_user}
            
            return render(request, template_name, template_context)
        else:
            return HttpResponseNotFound("Username not found!")
    

class CreateDictionary(View):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            form = NewDictionaryForm()

            return render(request, "new_dictionary.html", {"form": form})
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Username not found!")


    def post(self, request, username):
        form = NewDictionaryForm(request.POST)

        user_dictionaries = User.objects.select_related("dictionary") \
            .filter(username=username).values("id") \
                .annotate(dictioanry_name=models.F('dictionary__dictionary_name'))

        form.is_valid()
        new_dictionary_name = form.cleaned_data["dictionary_name"]
        old_dictionary_names = [item.get("dictionary_name") for item in user_dictionaries]

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

class DictionaryContent(View):

    def get(self, request, username, dictionary_name):
        try:
            requested_user = User.objects.filter(username=username).get()
            try:
                requested_dictionary = Dictionary.objects.filter(user=requested_user, dictionary_name=dictionary_name).get()
            except ObjectDoesNotExist:
                return HttpResponseBadRequest("The dictionary does not exist! <br>or You can not access that!")
        except ObjectDoesNotExist:
            return HttpResponseNotFound("Username not found!")
        else:
            dictionary_content = Translation.objects.filter(dictionary=requested_dictionary)
            form = AddTranslationFrom()
            template_name = 'dictionary.html'
            template_context = {
                'dictionary': requested_dictionary,
                'translations': dictionary_content,
                'form': form,
            }
            return render(request, template_name, template_context)

    def post(self, request, username, dictionary_name):

        try:
            requested_user = User.objects.filter(username=username).get()
            try:
                requested_dictionary = Dictionary.objects.filter(user=requested_user, dictionary_name=dictionary_name).get()
                form = AddTranslationFrom(request.POST)
                form.is_valid()
                try:
                    duplicate_translation = Translation.objects \
                        .filter(dictionary=requested_dictionary, keyword=form.cleaned_data['keyword']).get()
                    return HttpResponseBadRequest(f'Keyword "{duplicate_translation.keyword}" already exists!')
                except ObjectDoesNotExist:
                    pass
                Translation.objects.create(
                    dictionary=requested_dictionary,
                    keyword=form.cleaned_data['keyword'],
                    translation=form.cleaned_data['translation'],
                )
                return self.get(request, username, dictionary_name)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Dictionary not found!")
        except ObjectDoesNotExist:
            return HttpResponseNotFound("User not found!")