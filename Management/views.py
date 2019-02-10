from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView

from .models import Client, Cost
from .mixins import DeleteViewAjax

# client views
class AddClient(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'

class DeleteClient(LoginRequiredMixin, DeleteViewAjax):
    model = Client

class UpdateClient(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'

# cost views
class AddCost(LoginRequiredMixin, CreateView):
    model = Cost
    fields = '__all__'

class UpdateCost(LoginRequiredMixin, UpdateView):
    model = Cost
    fields = '__all__'

class DeleteCost(LoginRequiredMixin, DeleteViewAjax):
    model = Cost
