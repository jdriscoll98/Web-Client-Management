from django import forms
from management.models import Client, Project
from .models import Service, Cost

class InvoiceForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    amount = forms.IntegerField()
    due_date = forms.DateTimeField()
    description = forms.CharField()
