from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, CreateView
from taggit.models import Tag

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
        context['isCreating'] = 0
        return context

    def get(self, request, *args, **kwargs):
        pk = kwargs['pk']
        note = Note.objects.get(id=pk)
        if request.user != note.owner:
            return redirect('/')
        return super(NoteUpdateView, self).get(self, request, args, kwargs)


def note(request, pk):
    if request.user.is_authenticated is False:
        return redirect('/login')
    error = ''
    note = Note.objects.get(id=pk)
    if note.isPrivate is True and note.owner != request.user:
        note = None

    if note is None:
        error = 'Can\'t find note'
    return render(request, 'note.html', {'error': error, 'el': note})


def index(request):
    error = ''
    if request.user.is_authenticated is False:
        return redirect('/login')

    sort_by = 'title'
    group_by = ''
    if request.method == 'POST':
        sort_by = request.POST['sort_by']
        group_by = request.POST['group_by']

    notes = None
    if group_by == '':
        notes = Note.objects.filter(owner=request.user).order_by(sort_by)
    else:
        notes = Note.objects.filter(owner=request.user, tags__name__in=[group_by]).order_by(sort_by)

    context = {
        'notes': notes,
        'sort_option': sort_by,
        'tags': Tag.objects.filter(note__owner=request.user),
        'group_option': group_by,
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
        'isCreating': 1
    }
    return render(request, 'addnote.html', context)


def delete_note(request, pk):
    if request.user.is_authenticated is False:
        return redirect('/login')

    if request.method == 'POST':
        instance = Note.objects.get(owner=request.user, id=pk)
        instance.delete()
    return redirect('/')


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepassword.html', {
        'form': form
    })
