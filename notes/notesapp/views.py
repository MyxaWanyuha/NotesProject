import sys

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, FormView, CreateView
from notesapp.forms import NoteForm
from notesapp.models import Note
from django.contrib import messages

def logout_view(request):
    if request.user.is_authenticated is False:
        return redirect('/login')
    logout(request)
    return redirect('/login')


class RegisterFormView(CreateView):
    form_class = UserCreationForm
    success_url = '/login'
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated is True:
            return redirect('/')
        return super(RegisterFormView, self).get(self, request, args, kwargs)

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterFormView, self).form_invalid(form)


def login_request(request):
    if request.user.is_authenticated is True:
        return redirect('/')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form": form})


def search(request):
    error = ''
    if request.user.is_authenticated is False:
        return redirect('/login')
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


def index(request):
    error = ''
    print(request.user)
    if request.user.is_authenticated is False:
        return redirect('/login')

    context = {
        'notes': Note.objects.filter(owner=request.user).order_by('-id')
    }
    return render(request, 'index.html', context)


def add_note(request):
    error = ''
    if request.user.is_authenticated is False:
        return redirect('/login')

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
        return redirect('/login')

    if request.method == 'POST':
        id = request.POST.get('id')
        instance = Note.objects.get(id=id)
        instance.delete()
    return redirect('/')
