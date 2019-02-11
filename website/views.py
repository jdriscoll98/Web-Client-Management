from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import json

from .utils import *
from management.utils import get_total_profit

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'website/homepage.html'

    def get_context_data(self, *args, **kwargs):
        profits, total = get_total_profit()

        context = {
            'elementor_profit':  profits['el'],
            'server_profit':  profits['sh'],
            'domain_profit':  profits['do'],
            'GSuite_profit': profits['gs'],
            'total': total
               }
        return context
