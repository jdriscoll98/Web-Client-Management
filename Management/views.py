from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Client, Cost
from .mixins import DeleteViewAjax
from .utils import get_type_profit
# client views
class AddClient(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        context = super(AddClient, self).get_context_data(*args, **kwargs)
        return context

    def get_success_url(self, *args, **kwargs):
        next = reverse_lazy('management:add_cost', kwargs={'pk':self.object.pk, 'type':'elementor'})
        return next


class DeleteClient(LoginRequiredMixin, DeleteViewAjax):
    model = Client

class UpdateClient(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'

class DetailClient(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = Client.objects.get(pk=self.kwargs.get('pk'))
        context['elementor_cost'] = client.get_cost('elementor')
        context['server_hosting_cost'] = client.get_cost('server_hosting')
        context['domain_cost'] = client.get_cost('domains')
        context['gsuite_cost'] = client.get_cost('gsuite')
        return context
    # cost views

class AddCost(LoginRequiredMixin, CreateView):
    model = Cost
    fields = '__all__'

    def get_context_data(self, *args, **kwargs):
        context = super(AddCost, self).get_context_data(*args, **kwargs)
        type = Cost.TYPES.get_label(self.kwargs.get('type'))
        context['title'] = type
        context['next'] = reverse_lazy('management:client_detail', kwargs={'pk':self.kwargs.get('pk')})
        return context

    def get_initial(self):
        initial = super(AddCost, self).get_initial()
        initial = initial.copy()
        initial['client'] = self.kwargs.get('pk')
        try:
            type = Cost.TYPES.get_value(self.kwargs.get('type'))
            initial['type'] = type
        except Exception as e:
            print(e)
        return initial

    def get_success_url(self):
        return self.request.POST.get('next')




class UpdateCost(LoginRequiredMixin, UpdateView):
    model = Cost
    fields = '__all__'

class DeleteCost(LoginRequiredMixin, DeleteViewAjax):
    model = Cost

#page Views
class CostsView(TemplateView):
    template_name = 'management/costs.html'

    def get_context_data(self, *args, **kwargs):
        type = Cost.TYPES.get_value(kwargs['type'])
        label = Cost.TYPES.get_label(kwargs['type'])
        context = {
            'types': (type.value[1] for type in Cost.TYPES),
            'type': label,
            'costs' : Cost.TypeManager.type(type),
            'profit': get_type_profit(type)
            }
        return context
