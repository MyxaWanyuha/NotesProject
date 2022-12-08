from django.contrib import admin
from django.urls import path, include, re_path

from notesapp.views import index, add_note, delete_note, NoteUpdateView, search, RegisterFormView, \
    logout_view, login_request

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('addnote/', add_note),
    path('deletenote/', delete_note),
    re_path(r'^tinymce/', include('tinymce.urls')),
    path('<int:pk>/update', NoteUpdateView.as_view()),
    path('search/', search),
    path('register/', RegisterFormView.as_view()),
    path('login/', login_request),
    path('logout/', logout_view),
]
