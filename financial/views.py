from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views import View

from .models import Cost, Service, Payment
from management.models import Client, Project
from .mixins import DeleteViewAjax
from .forms import EstimatedCostForm
# Create your views here.
class AddCost(LoginRequiredMixin, CreateView):
    model = Cost
    fields = '__all__'
    success_url = reverse_lazy('website:homepage_view')

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

class ListCost(LoginRequiredMixin, ListView):
    model = Cost
    paginate_by = 100

    def get_queryset(self, **kwargs):
        type = Cost.TYPES.get_value(self.kwargs.get('type'))
        queryset = Cost.objects.filter(type=type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Cost.TYPES.get_label(self.kwargs.get('type'))
        return context

class AddService(LoginRequiredMixin, CreateView):
    model = Service
    fields = '_all__'

class ListServices(LoginRequiredMixin, ListView):
    model = Cost
    paginate_by = 100
    queryset = Service.objects.all()

class EstimatedCostGenerator(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        context = {
            'services' : Service.objects.all(),
            'clients' : Client.objects.all(),
            'projects': Project.objects.all(),
        }
        return render(self.request, 'financial/estimated_cost_form.html', context)
