from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.conf import settings
from .models import Client, Project
from financial.models import Cost
from .mixins import DeleteViewAjax
from .forms import ProjectForm

# client views
class AddClient(LoginRequiredMixin, CreateView):
    model = Client
    fields = '__all__'
    success_url = reverse_lazy('website:homepage_view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Client'
        return context

class DeleteClient(LoginRequiredMixin, DeleteViewAjax):
    model = Client

class UpdateClient(LoginRequiredMixin, UpdateView):
    model = Client
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Client'
        return context

class DetailClient(LoginRequiredMixin, DetailView):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(client=self.object)
        context['client_costs'] = Cost.objects.filter(client=self.object)
        return context

# project views
class AddProject(LoginRequiredMixin, CreateView):
    template_name = 'management/project_form.html'
    form_class = ProjectForm

    def get_initial(self, **kwargs):
        initial = super(AddProject, self).get_initial()
        try:
            initial['client'] = Client.objects.get(pk=self.kwargs.get('pk'))
        except Exception as e:
            print(e)
        return initial

    def get_context_data(self, **kwargs):
        context = super(AddProject, self).get_context_data(**kwargs)
        context['title'] = 'Add Project'
        context['next'] = reverse('management:detail_client', kwargs={'pk':self.kwargs.get('pk')})
        return context


    def get_success_url(self, **kwargs):
        print(self.request.POST.get('next'))
        next = self.request.POST.get('next', reverse('website:homepage_view'))
        print(next)
        return next

class DeleteProject(LoginRequiredMixin, DeleteViewAjax):
    model = Project

class UpdateProject(LoginRequiredMixin, UpdateView):
    model = Project
    template_name = 'management/project_form.html'
    form_class = ProjectForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Project'
        context['next'] =  reverse('management:detail_client', kwargs={'pk': self.kwargs.get('pk2')})
        return context

    def get_success_url(self, **kwargs):
        next = self.request.POST.get('next', reverse('website:homepage_view'))
        return next

#company Management
class CompanyPage(LoginRequiredMixin, TemplateView):
    template_name = 'management/company_page.html'

    def get_context_data(self, *args, **kwargs):
        client = Client.objects.get(name=settings.COMPANY_NAME)
        context = {
            'client': client,
            'costs': Cost.objects.filter(client=client)

        }
        return context
