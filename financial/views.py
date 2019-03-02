from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Cost, Service
from .mixins import DeleteViewAjax
# Create your views here.
class AddCost(LoginRequiredMixin, CreateView):
    model = Cost
    fields = '__all__'
    success_url = reverse_lazy('website:homepage')
    def get_initial(self):
        initial = super(AddCost, self).get_initial()
        initial = initial.copy()
        initial['client'] = self.kwargs.get('pk')
        return initial


class UpdateCost(LoginRequiredMixin, UpdateView):
    model = Cost
    fields = '__all__'

class DeleteCost(LoginRequiredMixin, DeleteViewAjax):
    model = Cost
