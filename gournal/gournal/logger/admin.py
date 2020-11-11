from django.apps import AppConfig
from django.contrib import admin
from .models import Word


class LoggerConfig(AppConfig):
    name = 'logger'
class WordAdmin(admin.ModelAdmin):
    list_filter = ['sub_date']
admin.site.register(Word, WordAdmin)