from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Client
from .mixins import DeleteViewAjax
# client views
class AddClient(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('management:homepage')

class DeleteClient(LoginRequiredMixin, DeleteViewAjax):
    model = Client

class UpdateClient(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'

class DetailClient(LoginRequiredMixin, DetailView):
    model = Client
    # cost views
