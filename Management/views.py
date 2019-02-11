from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .models import Client, Cost
from .mixins import DeleteViewAjax
from .utils import get_type_profit

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

#page Views
class CostsView(TemplateView):
    template_name = 'management/costs.html'

    def get_context_data(self, *args, **kwargs):
        type = Cost.TYPES.get_value(kwargs['type'])
        label = Cost.TYPES.get_label(kwargs['type'])
        context = {
            'types': (type.value[1] for type in Cost.TYPES),
            'type': label,
            'costs' : Cost.objects.filter(type=type),
            'profit': get_type_profit(type)
            }
        return context
