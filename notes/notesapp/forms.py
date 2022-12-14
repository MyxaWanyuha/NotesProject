import django.forms

import notesapp.models
from django.forms import ModelForm, TextInput, Textarea, CharField
from notesapp.models import Note


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body', 'tags', 'isPrivate', 'uploadedFile']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),

            'body': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            }),

            'uploadedFile': django.forms.ClearableFileInput(attrs={
                'multiple': True
            }),
        }
        