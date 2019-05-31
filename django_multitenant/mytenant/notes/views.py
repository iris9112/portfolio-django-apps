from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Note


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "notes/note_listview.html"


class HomeNoteView(LoginRequiredMixin, TemplateView):
    template_name = "notes/note_home.html"


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['sender', 'recipient', 'msj', 'img']
    template_name = "notes/create_note.html"
    success_url = reverse_lazy('notes:home_notes')
    import logging
    db_logger = logging.getLogger('db')

    db_logger.info('info message')
    db_logger.warning('warning message')

    try:
        1/0
    except Exception as e:
        db_logger.exception(e)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })

