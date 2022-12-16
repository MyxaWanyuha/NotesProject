from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

from notesapp import views
from notesapp.views import index, add_note, delete_note, NoteUpdateView, search, RegisterFormView, \
    logout_view, login_request, note, user_account

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    re_path('', include('social_django.urls', namespace='social')),
    path('addnote/', add_note),
    path('<int:pk>/deletenote/', delete_note, name='deletenote'),
    re_path(r'^tinymce/', include('tinymce.urls')),
    path('<int:pk>/update', NoteUpdateView.as_view()),
    path('<int:pk>', note, name='notelink'),
    path('search/', search),
    path('register/', RegisterFormView.as_view()),
    path('login/', login_request),
    path('logout/', logout_view),
    re_path(r'^password/$', views.change_password, name='change_password'),
    path('user_account/', user_account),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
