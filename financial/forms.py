from django import forms
from management.models import Client, Project
from .models import Service, CompanyCost, ClientCost, CostType

class InvoiceForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all())
    amount = forms.IntegerField()
    due_date = forms.DateTimeField()
    description = forms.CharField()

class CompanyCostForm(forms.ModelForm):
    class Meta:
        model = CompanyCost
        fields = '__all__'

class ClientCostForm(forms.ModelForm):
    class Meta:
        model = ClientCost
        fields = ('__all__')

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        exclude =  ['company']

class CostTypeForm(forms.ModelForm):
    class Meta:
        model = CostType
        fields = '__all__'
        widgets = {
            'company': forms.HiddenInput()
        }
