from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView

from .models import Client, Cost

# client views
class AddClient(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('website:homepage_view')

class RemoveClient(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('website:homepage_view')

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

class DeleteCost(LoginRequiredMixin, DeleteView):
    model = Cost
