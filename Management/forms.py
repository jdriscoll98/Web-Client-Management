from django import forms
from .models import Project, Client

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
