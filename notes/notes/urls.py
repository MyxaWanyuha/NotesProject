from django.contrib import admin
from django.urls import path, include, re_path

from notesapp.views import auth, index, add_note, delete_note, NoteUpdateView, search

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('auth/', auth),
    path('addnote/', add_note),
    path('deletenote/', delete_note),
    re_path(r'^tinymce/', include('tinymce.urls')),
    path('<int:pk>/update', NoteUpdateView.as_view()),
    path('search/', search),
]
