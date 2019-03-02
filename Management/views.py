from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Client, Project
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
        return context
    # project

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
        return context


    def get_success_url(self, **kwargs):
        next = self.request.POST.get('next', 'website:homepage')
        return next

class DeleteProject(LoginRequiredMixin, DeleteViewAjax):
    model = Project

class UpdateProject(LoginRequiredMixin, UpdateView):
    model = Project
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Project'
        return context

class DetailProject(LoginRequiredMixin, DetailView):
    model = Project
