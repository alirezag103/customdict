from django.forms import (ModelForm, DateInput, TimeInput,
                          TextInput, IntegerField)
from django.core.exceptions import ValidationError

from .models import Dictionary


class NewDictionaryForm(ModelForm):

    class Meta:
        model = Dictionary
        fields = ['dictionary_name', 'source_language', 'target_language']


        