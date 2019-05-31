from django.urls import path

from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.HomeNoteView.as_view(), name='home_notes'),
    path('list-notes/', views.NoteListView.as_view(), name='listview_notes'),
    path('create-note/', views.NoteCreateView.as_view(), name='create_note'),
    path('signup/', views.signup, name='signup'),
]
