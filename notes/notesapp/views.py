from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from notesapp.forms import NoteForm
from notesapp.models import Note
from notesapp.permissions import IsOwner
from notesapp.serializers import NoteSerializer


class NoteList(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['title']
    search_fields = ['date', 'body']
    ordering_fields = ['title']
    permission_classes = [IsOwner]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


def auth(request):
    return render(request, 'oauth.html')


def index(request):
    error = ''
    if request.user.is_authenticated is False:
        error = 'Пользователь не авторизован!'
        return redirect('/auth')

    context = {
         'notes': Note.objects.filter(owner=request.user).order_by('-id')
    }
    # order_by('id')
    return render(request, 'index.html', context)


def add_note(request):
    error = ''
    if request.user.is_authenticated is False:
        error = 'Пользователь не авторизован!'
        return redirect('/auth')

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect('/')
        else:
            error = 'Форма невалидна!'

    form = NoteForm()
    context = {
        'error': error,
        'form': form,
        'is_authenticated': request.user.is_authenticated,
        'notes': Note.objects.all()
    }
    return render(request, 'addnote.html', context)
