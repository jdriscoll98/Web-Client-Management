from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import json

from .utils import *
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
            'elementor': sum((cost.client_payment - cost.price) for cost in Cost.objects.filter(type=elementor)),
            'domains': sum((cost.client_payment - cost.price) for cost in  Cost.objects.filter(type=domains)),
            'servers': sum((cost.client_payment - cost.price) for cost in Cost.objects.filter(type=servers)),
            'other': sum((cost.client_payment - cost.price) for cost in Cost.objects.filter(type=other)),
               }
        return context
