from django.forms import ModelForm, TextInput, Textarea
from notesapp.models import Note


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'body']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название'
            }),
            'body': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание'
            }),
        }
        