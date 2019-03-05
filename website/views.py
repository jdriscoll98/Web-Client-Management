from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
import json
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from management.forms import MemberForm
from .utils import get_profit, get_total
from management.models import Company
from financial.models import Cost

#-------------------------------------------------------------------------------
# Page Views
#-------------------------------------------------------------------------------
class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'website/homepage.html'

    def get_context_data(self, *args, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        companies = Company.objects.filter(members__in=[self.request.user])
        context = {
            'companies': companies
               }
        return context

class NewUser(CreateView):
    form_class = MemberForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('core:login')
