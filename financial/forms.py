from django import forms
from management.models import Client, Project
from .models import Service, Cost

class InvoiceForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    amount = forms.IntegerField()
    due_date = forms.DateTimeField()
    description = forms.CharField()

class CompanyCost(forms.ModelForm):
    class Meta:
        model = Cost
        exclude = ['project', 'client_payment']
        widgets = {
            'client': forms.HiddenInput()
        }

class ClientCost(forms.ModelForm):
    class Meta:
        model = Cost
        fields = ('__all__')
