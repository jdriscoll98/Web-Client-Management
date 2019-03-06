from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormView, DeleteView
from .models import Client, Project, Company
from financial.models import ClientCost, CompanyCost, Service
from .mixins import DeleteViewAjax
from .forms import ProjectForm, ClientForm, MemberForm, CompanyForm
from .utils import get_income_cost, get_total

# THE ISSUE BIGGER THAN ANYTHING ELSE, WHERE ARE YOUR COMMENTS? HOW WILL SOMEONE ELSE
# EVER BE ABLE TO KNOW WHAT YOU'RE THINKING? READABLE CODE IS GOOD, BUT SLIGHT COMMENTING
# MAKES IT EVEN BETTER.

# client views
class AddClient(LoginRequiredMixin, CreateView):
    form_class = ClientForm
    template_name = 'management/client_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Client'
        context['next'] = reverse('management:company_page', kwargs={'pk': self.kwargs.get('pk')})
        return context

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(*args, **kwargs)
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        initial['company'] = company
        return initial

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
        context['client_costs'] = ClientCost.objects.filter(client=self.object)
        return context

# member views
class AddNewMember(LoginRequiredMixin, FormView):
    form_class = MemberForm
    template_name = 'management/member_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = reverse('management:company_page', kwargs={'pk':
                                                        self.kwargs.get('pk')})
        return context

    # Don't leave exception printing code in unless required
    def form_valid(self, form, **kwargs):
        try:
            self.object = form.save()
            company = Company.objects.get(pk=self.kwargs.get('pk'))
            company.members.add(self.object)
            company.save()
        except Exception as e:
            print(e)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self, **kwargs):
        next = self.request.POST.get('next', reverse('website:homepage_view'))
        return next


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
        print(next) # Don't leave print stuff if not needed, and again don't declare variables
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
        company = Company.objects.get(pk=self.kwargs.get('pk'))
        # I want to avoid using hardcoded anything... lets talk about cleaning this up
        elementor = CompanyCost.TYPES.get_value('elementor')
        domains = CompanyCost.TYPES.get_value('domains')
        servers = CompanyCost.TYPES.get_value('server_hosting')
        project = CompanyCost.TYPES.get_value('project')
        context = {
            'company': company,
            'clients': Client.objects.filter(company=company),
            'members': company.members.all(),
            'costs': CompanyCost.objects.filter(company=company),
            'elementor': get_income_cost(company, elementor),
            'domains': get_income_cost(company, domains),
            'servers': get_income_cost(company, servers),
            'project': get_income_cost(company, project),
            'total': get_total(company),
            'services': Service.objects.filter(company=company)

        }
        return context


class AddCompany(LoginRequiredMixin, CreateView):
    form_class = CompanyForm
    template_name = 'management/company_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add Company'
        return context

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(*args, **kwargs)
        initial['members'] = [self.request.user]
        return initial

class DeleteCompany(LoginRequiredMixin, DeleteViewAjax):
    model = Company

class UpdateCompany(LoginRequiredMixin, UpdateView):
    model = Company
    fields = ('name', 'stripe_secret', 'stripe_public')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Company'
        return context

class UpdateCompanyMembers(LoginRequiredMixin, View):
    def get(self, *args,**kwargs):
        company = Company.objects.get(pk=self.kwargs.get('company'))
        current_members = company.members.all()
        print(current_members) # .....
        potential_members = User.objects.exclude(id__in=current_members.values_list('id', flat=True))
        print(potential_members)
        context = {
            'company': company,
            'users': User.objects.exclude(id__in=current_members.values_list('id', flat=True)),
        }
        return render(self.request, 'management/add_members.html', context)

    def post(self, *args, **kwargs):
        try:
            user = User.objects.get(pk=self.kwargs.get('user'))
            company = Company.objects.get(pk=self.kwargs.get('company'))
            company.members.add(user)
            company.save()
            success = True
            message = "Member added successfully"
        except Exception as e:
            success = False
            message = "Error adding memeber" + str(e) # Never leave messages showing this stuff to users
        return JsonResponse({'success':success, 'message': message})
