from django.contrib import admin
from django.contrib.admin import ModelAdmin

from notesapp.models import Note


@admin.register(Note)
class NoteAdmin(ModelAdmin):
    pass
