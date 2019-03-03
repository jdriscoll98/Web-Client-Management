from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import json
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


from .utils import get_profit, get_total
from management.models import Client
from financial.models import Cost

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'website/homepage.html'

    def get_context_data(self, *args, **kwargs):
        elementor = Cost.TYPES.get_value('elementor')
        domains = Cost.TYPES.get_value('domains')
        servers = Cost.TYPES.get_value('server_hosting')
        other = Cost.TYPES.get_value('other')

        context = {
            'clients': Client.objects.all(),
            'elementor': get_profit(elementor),
            'domains': get_profit(domains),
            'servers': get_profit(servers),
            'other': get_profit(other),
            'total': get_total()
               }
        return context
