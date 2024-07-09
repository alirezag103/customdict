from django.forms import (HiddenInput, ModelForm, DateInput, TimeInput,
                          TextInput, IntegerField, UUIDField, Widget)
from django.core.exceptions import ValidationError

from .models import Dictionary


class NewDictionaryForm(ModelForm):

    class Meta:
        model = Dictionary
        fields = ['dictionary_name', 'source_language', 'target_language', 'user']
        Widgets = {
            'user': HiddenInput(),
        }
