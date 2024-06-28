from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.OriginLanguage)
class OriginLanguageAdmin(admin.ModelAdmin):
    ordering = ['language_name']

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    ordering = ['language_name']