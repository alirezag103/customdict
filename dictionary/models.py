from csv import Dialect
from django.utils import timezone
from django.db import models
import uuid
import json

from customdict.settings import BASE_DIR

# Create your models here.

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, db_column="username", unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=256, db_column="password")


    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    # add django getter/setter for username and password,
    # normal python getter/setter didn't work
        

    def defiened_languages(self):
        user_langs = User.objects.filter(id=self.id).select_related('user__language')
        return user_langs



# def get_language_list():
    # return {lan_code: lan_description for lan_code in language_list.json}

class UserMetaData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    sign_up_time = models.DateTimeField(default=timezone.now)


class AbstractOriginLanguage(models.Model):
    with open( BASE_DIR / 'dictionary/lang_list.json', 'r', encoding='utf-8') as language_json:
        language_list = json.load(language_json)

    with open( BASE_DIR / 'dictionary/locale_list.json', 'r', encoding='utf-8') as locale_json:
        locale_list = json.load(locale_json)

    language_name = models.CharField(max_length=100)
    language_code = models.CharField(max_length=3, choices=language_list)
    locale = models.CharField(max_length=100)
    locale_code = models.CharField(max_length=4, choices=locale_list)
    dialect = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.language_code}-{self.locale_code} ({self.language_name})'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language_code', 'locale_code', 'dialect'], name='unique_language')
        ]
        abstract = True

class OriginLanguage(AbstractOriginLanguage):
    locale = None
    dialect = None

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language_code', 'locale_code'], name='unique_local_language_code')
        ]

class Language(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    language_name = models.CharField(max_length=100, unique=True)
    origin_language = models.ForeignKey(OriginLanguage, on_delete=models.PROTECT, related_name='+', null=True)
    description = models.CharField(null=True, max_length=1024)

    def __str__(self) -> str:
        return f'{self.origin_language}: {self.language_name}'
    
    class Meta:
        constraints = []

class Dictionary(models.Model):
    dictionary_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    source_language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='+')
    target_language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='+')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['dictionary_name', 'user'], name='unique_dictionary_per_user')
        ]

class Translation(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name='+')
    keyword = models.CharField(max_length=255)
    translation = models.CharField(max_length=1024)


