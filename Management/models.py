from django.db import models
from django.urls import reverse
from datetime import timedelta
from financial.models import ClientCost, CompanyCost, CostType
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    members = models.ManyToManyField(User)
    stripe_secret = models.CharField(max_length=200, blank=True, null=True)
    stripe_public = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('management:company_page', kwargs={'pk':self.pk})

    def get_project_income(self):
        amount = 0
        for client in Client.objects.filter(company=self):
            amount += sum(project.amount for project in Project.objects.filter(client=client))
        return amount

    def get_client_costs(self, type):
        costs = []
        for client in Client.objects.filter(company=self):
            for cost in ClientCost.objects.filter(client=client):
                costs.append(cost)
        return costs


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, default=None,  on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(blank=True, null=True)
    folder_link = models.URLField(blank=True, null=True, unique=True)
    additional_information = models.TextField(blank=True, null=True)
    amount_owed = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('management:company_page', kwargs={'pk': self.company.pk})

    def get_cost(self, pk):
        type = CostType.objects.filter(pk=pk)
        if Cost.objects.filter(client=self, type=type).exists():
            cost = Cost.objects.get(client=self, type=type)
            return cost
        else:
            return None

    def get_profit(self, type):
        try:
            cost = Cost.objects.get(client=self, type=type)
        except:
            pass
        return cost.get_total_cost()

    def get_amount_owed(self):
        total = sum(cost.amount for cost in ClientCost.objects.filter(client=self))
        return total

    def get_customer_id(self):
        return self.customer_id


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    github_link = models.URLField(blank=True, null=True, unique=True)
    folder_link = models.URLField(blank=True, null=True, unique=True)

    def __str__(self):
        return str(self.name)
