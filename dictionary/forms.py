from django import forms
from django.core.exceptions import ValidationError
from pkg_resources import require

from .models import Dictionary, Translation, User


class NewDictionaryForm(forms.ModelForm):

    class Meta:
        model = Dictionary
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
        }


class AddTranslationFrom(forms.ModelForm):

    class Meta:
        model = Translation
        fields = ['keyword', 'translation']
        # widgets = {
        #     'dictionary': forms.HiddenInput()
        # }

# translation_formset = forms.formset_factory(AddTranslationFrom)
