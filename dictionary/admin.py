from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']

@admin.register(models.OriginLanguage)
class OriginLanguageAdmin(admin.ModelAdmin):
    search_fields = ['language_code', 'locale_code']
    ordering = ['language_name']

@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    autocomplete_fields = ['origin_language', 'user']
    ordering = ['language_name']