from django import forms
from management.models import Client, Project
from .models import Service, Cost

class EstimatedCostForm(forms.Form):
    client = forms.ModelChoiceField(queryset=Client.objects.all(), empty_label=None)
    project = forms.ModelChoiceField(queryset=Project.objects.all(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        services = Service.objects.all()
        project = Cost.TYPES.get_value('project')
        for service in services:
            field_name = str(service)
            self.fields[field_name] = forms.IntegerField()
        for type in Cost.TYPES:
            if type.value[0] is not project:
                field_name = type.value[1]
                print(field_name)
                self.fields[field_name] = forms.IntegerField()
