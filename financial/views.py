from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views import View

from .models import ClientCost, CompanyCost, Service, CostType
from management.models import Client, Project, Company
from .forms import (CompanyCostForm, ClientCostForm, ServiceForm, InvoiceForm,
                    CostTypeForm)
from .utils import (create_costs, send_invoice, get_invoices, get_invoice_items)
from .mixins import DeleteViewAjax

from datetime import datetime
import stripe
import json
#client cost views
class AddClientCost(LoginRequiredMixin, CreateView):
    form_class = ClientCost
    template_name = 'financial/cost_form.html'
    success_url = reverse_lazy('website:homepage_view')

    def get_initial(self):
        initial = super(AddCost, self).get_initial()
        initial = initial.copy()
        client = Client.objects.get(pk=self.kwargs.get('pk'))
        initial['client'] = client
        return initial

class UpdateClientCost(LoginRequiredMixin, UpdateView):
    model = ClientCost
    fields = '__all__'

class DeleteClientCost(LoginRequiredMixin, DeleteViewAjax):
    model = ClientCost

class CostView(LoginRequiredMixin, TemplateView):
    model = ClientCost
    template_name = 'financial/cost_list.html'

    def get_context_data(self, **kwargs):
        type = CostType.objects.get(pk=self.kwargs.get('type'))
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        context = {
            'title': type.name,
            'company': company,
            'company_costs': CompanyCost.objects.filter(type=type),
            'client_costs': company.get_client_costs(type)
        }

        return context

#company cost views
class AddCompanyCost(LoginRequiredMixin, CreateView):
    model = CompanyCost
    template_name = 'financial/cost_form.html'
    fields = '__all__'

    def get_initial(self):
        initial = super(AddCost, self).get_initial()
        initial = initial.copy()
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        initial['company'] = company
        return initial

class UpdateCompanyCost(LoginRequiredMixin, UpdateView):
    model = CompanyCost
    template_name = 'financial/cost_form.html'
    fields = '__all__'

class DeleteCompanyCost(LoginRequiredMixin, DeleteViewAjax):
    model = CompanyCost

#cost type views
class AddCostType(LoginRequiredMixin, CreateView):
    form_class = CostTypeForm
    template_name = 'financial/costtype_form.html'

    def get_initial(self):
        initial = super(AddCostType, self).get_initial()
        initial = initial.copy()
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        initial['company'] = company
        return initial

class UpdateCostType(LoginRequiredMixin, UpdateView):
    model = CostType
    fields = ('name', 'payment_period')

class DeleteCostType(LoginRequiredMixin, DeleteViewAjax):
    model = CostType

#service views
class AddService(LoginRequiredMixin, CreateView):
    form_class = ServiceForm
    template_name = 'financial/service_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Service'
        return context

    def get_initial(self):
        initial = super(AddService, self).get_initial()
        initial = initial.copy()
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        initial['company'] = company
        return initial


class UpdateService(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ('name', 'cost_per_hour')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modify Service'
        return context

class DeleteService(LoginRequiredMixin, DeleteViewAjax):
    model = Service

#cost generator
class EstimatedCostGenerator(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        company =  Company.objects.get(pk=self.kwargs.get('pk'))
        context = {
            'company': self.kwargs.get('pk'),
            'services' : Service.objects.filter(company=company),
            'clients' : Client.objects.filter(company=company),
            'projects': Project.objects.all(),
            'types':  CostType.objects.filter(company=company)
        }
        return render(self.request, 'financial/estimated_cost_form.html', context)

    def post(self, *args, **kwargs):
        data = self.request.POST
        if create_costs(data):
            return redirect(reverse('management:company_page', kwargs={'pk':self.kwargs.get('pk')}))
        return redirect(reverse('financial:estimate', kwargs={'pk':self.kwargs.get('pk')}))

# invoice views
class ManageInvoices(LoginRequiredMixin, TemplateView):
    template_name = 'financial/invoices.html'

    def get_context_data(self, *args, **kwargs):
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        key = company.stripe_secret
        invoices = get_invoices(key)
        context =  {
            'company': company.pk,
            'invoices' : invoices
        }
        return context

class InvoiceDetails(LoginRequiredMixin, TemplateView):
    template_name = 'financial/invoice_items.html'

    def get_context_data(self, *args, **kwargs):
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        key = company.stripe_secret
        invoice_items = get_invoice_items(self.kwargs.get('id'), key)
        context = {
            'invoice_items': invoice_items
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
