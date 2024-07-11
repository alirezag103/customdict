from django import forms
from django.core.exceptions import ValidationError
from pkg_resources import require

from .models import Dictionary, User


class NewDictionaryForm(forms.ModelForm):

    class Meta:
        model = Dictionary
        fields = ['dictionary_name', 'source_language', 'target_language', 'user']
        widgets = {
            'user': forms.HiddenInput(),
        }



