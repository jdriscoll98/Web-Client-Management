from django import forms
from .models import Project, Client, Company
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {'client': forms.HiddenInput()}

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        exclude = ['customer_id']
        widgets = {'company': forms.HiddenInput()}

class MemberForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', 'members',)
        widgets = {'members': forms.MultipleHiddenInput()}
