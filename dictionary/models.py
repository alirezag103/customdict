from django.db import models
import uuid


# Create your models here.

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    _username = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    _password = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
    
    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, password, new_username):
        if password == self._password:
            self._username = new_username
            return f'User name of \"{self.__str__()}\" has been changed!'
        else:
            raise ValueError("Wrong password provided!")
        
# def get_language_list():
    # return {lan_code: lan_description for lan_code in language_list.json}

class AbstractOriginLanguage(models.Model):
    language_list = {
        "en": "American English",
        "zh": "Chinese",
        "ar": "Arabic",
        "fa": "Persian",
        "fr": "French",
        "es": "Spanish",
        "ru": "Russian",
        "de": "German",
        "ja": "Japanese",
        "it": "Italian",
        "pt": "Portuguese",
        "hi": "Hindi",
    }
    locale_list = {
        "US": "United States",
        "CN": "simplified, PRC",
        "RU": "Russia",
        "FR": "France",
        "ES": "Spain",
        "GB": "United Kingdom",
        "DE": "Germany",
        "BR": "Brazil",
        "CA": "Canada",
        "MX": "Mexico",
        "IT": "Italy",
        "JP": "Japan",
        "IN": "India",
    }
    language_name = models.CharField(max_length=100)
    language_code = models.CharField(max_length=2, choices=language_list)
    locale = models.CharField(max_length=100)
    locale_code = models.CharField(max_length=2, choices=locale_list)

    def __str__(self) -> str:
        return f'{self.language_code}-{self.locale_code} ({self.language_name})'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['language_code', 'locale_code'], name='unique_local_language_code')
        ]
        abstract = True

class OriginLanguage(AbstractOriginLanguage):
    pass

class Language(AbstractOriginLanguage):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='+')
    language_name = models.CharField(max_length=100, unique=True)
    # language_code = models.ForeignKey(OriginLanguage.language_code, on_delete=models.PROTECT, related_name='+')
    # locale_code = models.ForeignKey(OriginLanguage.locale_code, on_delete=models.PROTECT, related_name='+')
    description = models.CharField(null=True, max_length=1024)
    
    class Meta:
        constraints = []

class Dictionary(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    source_language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='+')
    target_language = models.ForeignKey(Language, on_delete=models.PROTECT, related_name='+')

class Translation(models.Model):
    dictionary = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name='+')
    keyword = models.CharField(max_length=255)
    translation = models.CharField(max_length=1024)



