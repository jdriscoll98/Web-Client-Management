from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views import View

from .models import ClientCost, CompanyCost, Service, Cost

from .utils import (create_costs, send_invoice, get_invoices,
                    get_client_costs, get_invoice_items)

from .forms import InvoiceForm
from .forms import CompanyCostForm, ClientCostForm, ServiceForm

from management.models import Client, Project, Company
from .mixins import DeleteViewAjax

from datetime import datetime

import stripe
import json

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

class AddCompanycost(LoginRequiredMixin, CreateView):
    model = CompanyCost
    template_name = 'financial/cost_form.html'
    fields = '__all__'

class UpdateCost(LoginRequiredMixin, UpdateView):
    model = ClientCost
    fields = '__all__'

class DeleteCost(LoginRequiredMixin, DeleteViewAjax):
    model = ClientCost

class CostView(LoginRequiredMixin, TemplateView):
    model = ClientCost
    template_name = 'financial/cost_list.html'

    def get_context_data(self, **kwargs):
        label = self.kwargs.get('type')
        type = Cost.TYPES.get_value(self.kwargs.get('type'))
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        context = {
            'title':  Cost.TYPES.get_label(label),
            'company': company,
            'company_costs': CompanyCost.objects.filter(type=type),
            'client_costs': get_client_costs(company, type) # Lets talk about this, all that should need to
            # be passed in is the company... not all these other details
        }

        return context

#service views
class AddService(LoginRequiredMixin, CreateView):
    model = Service
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Service'
        context['next'] = reverse('management:company_page',kwargs={'pk': self.kwargs.get('pk')})
        return context

    def get_success_url(self, **kwargs):
        print('here')
        next = self.request.POST.get('next', None)
        print('now here') # bruh... cleanup ya dang debugging
        return next


class UpdateService(LoginRequiredMixin, UpdateView):
    model = Service
    fields = ('name', 'cost_per_hour')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Modify Service' # What is this about?
        return context

class DeleteService(LoginRequiredMixin, DeleteViewAjax):
    model = Service

class EstimatedCostGenerator(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        company =  Company.objects.get(pk=self.kwargs.get('pk'))
        context = {
            'company': self.kwargs.get('pk'), # Definitley not the way to do it, passing wat to much context
            'services' : Service.objects.filter(company=company),
            'clients' : Client.objects.filter(company=company),
            'projects': Project.objects.all(),
            'types': [x.value for x in Cost.TYPES if x.value[0] != 'pj' ]
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
        company = Company.objects.get(pk=self.kwargs.get('pk')) # No try statement?
        # key = company.stripe_secret # Why create seperate variable?
        # invoices = get_invoices(key) # Why create seperate variable?
        context =  {
            'company': company.pk,
            'invoices' : get_invoices(company.stripe_secret)
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
