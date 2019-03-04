from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views import View

from .models import ClientCost, CompanyCost, Service
from .utils import create_costs, send_invoice, get_invoices
from .forms import InvoiceForm
from management.models import Client, Project
from .mixins import DeleteViewAjax
from datetime import datetime
import stripe
import json
from .forms import CompanyCost, ClientCost
#cost views
class AddCost(LoginRequiredMixin, CreateView):
    form_class = ClientCost
    template_name = 'financial/cost_form.html'
    success_url = reverse_lazy('website:homepage_view')

    def get_initial(self):
        initial = super(AddCost, self).get_initial()
        initial = initial.copy()
        client = self.kwargs.get('pk')
        initial['client'] = client
        return initial

class AddCompanycost(AddCost):
    form_class = CompanyCost

class UpdateCost(LoginRequiredMixin, UpdateView):
    model = ClientCost
    fields = '__all__'

class DeleteCost(LoginRequiredMixin, DeleteViewAjax):
    model = ClientCost

class ListCost(LoginRequiredMixin, ListView):
    model = ClientCost
    paginate_by = 100

    def get_queryset(self, **kwargs):
        type = ClientCost.TYPES.get_value(self.kwargs.get('type'))
        queryset = ClientCost.objects.filter(type=type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = ClientCost.TYPES.get_label(self.kwargs.get('type'))
        return context

#service views
class AddService(LoginRequiredMixin, CreateView):
    model = Service
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Service'
        return context

class UpdateService(LoginRequiredMixin, CreateView):
    model = Service
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modify Service'
        return context

#cost generator
class EstimatedCostGenerator(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        context = {
            'services' : Service.objects.all(),
            'clients' : Client.objects.all(),
            'projects': Project.objects.all(),
            'types': [x.value for x in ClientCost.TYPES if x.value[0] != 'pj' ]
        }
        return render(self.request, 'financial/estimated_cost_form.html', context)

    def post(self, *args, **kwargs):
        data = self.request.POST
        if create_costs(data):
            return redirect(reverse('website:homepage_view'))
        return redirect(reverse('financial:estimate'))

# invoice views
class ManageInvoices(LoginRequiredMixin, TemplateView):
    template_name = 'financial/invoices.html'

    def get_context_data(self, *args, **kwargs):
        invoices = get_invoices()
        context =  {
            'invoices' : invoices
        }
        return context

class AddInvoice(LoginRequiredMixin, FormView):
    form_class = InvoiceForm
    template_name = 'financial/invoice_form.html'
    success_url = reverse_lazy('financial:invoice')

    def form_valid(self, form):
        data = form.cleaned_data
        client = data['client']
        amount = data['amount']
        description = data['description']
        due_date =  int(data['due_date'].timestamp())
        send_invoice(client, amount, description, due_date)
        return HttpResponseRedirect(self.get_success_url())

class UpdateInvoice(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        return redirect('website:homepage_view')
