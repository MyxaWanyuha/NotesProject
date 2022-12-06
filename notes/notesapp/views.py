from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView, ListView

from notesapp.forms import NoteForm
from notesapp.models import Note


def search(request):
    error = ''
    if request.user.is_authenticated is False:
        return redirect('/auth')
    if request.method == 'GET':
        query = request.GET.get("q")
        context = {
         'notes': Note.objects.filter(Q(title__iregex=query) | Q(body__iregex=query))
        }
        return render(request, 'index.html', context)
    else:
        redirect('/')


class NoteUpdateView(UpdateView):
    model = Note
    template_name = 'addnote.html'
    form_class = NoteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['buttontext'] = 'Изменить'
        return context


def auth(request):
    return render(request, 'oauth.html')


def index(request):
    error = ''
    if request.user.is_authenticated is False:
        return redirect('/auth')

    context = {
         'notes': Note.objects.filter(owner=request.user).order_by('-id')
    }
    return render(request, 'index.html', context)


def add_note(request):
    error = ''
    if request.user.is_authenticated is False:
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
        'notes': Note.objects.all(),
        'buttontext': 'Создать'
    }
    return render(request, 'addnote.html', context)


def delete_note(request):
    if request.user.is_authenticated is False:
        return redirect('/auth')

    if request.method == 'POST':
        id = request.POST.get('id')
        instance = Note.objects.get(id=id)
        instance.delete()
    return redirect('/')
