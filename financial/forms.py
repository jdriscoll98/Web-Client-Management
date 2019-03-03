from django import forms
from management.models import Client, Project
from .models import Service

class EstimatedCostForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label=None)
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        services = Service.objects.all()
        for service in services:
            field_name = str(service)
            self.fields[field_name] = forms.IntegerField()
