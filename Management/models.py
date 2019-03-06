from django.db import models
from django.urls import reverse
from datetime import timedelta
from financial.models import ClientCost, CompanyCost
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


class Client(models.Model):
    name = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(Company, default=None,  on_delete=models.CASCADE)
    customer_id = models.CharField(max_length=100, blank=True, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(blank=True, null=True)
    folder_link = models.URLField(blank=True, null=True)
    additional_information = models.CharField(max_length=250, blank=True, null=True)
    amount_owed = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('management:company_page', kwargs={'pk': self.company.pk})

    def get_cost(self, label):
        type = Cost.TYPES.get_value(label)
        if Cost.objects.filter(client=self, type=type).exists():
            # Why are you delcaring variables when you don't need to?
            return Cost.objects.get(client=self, type=type)
        # else: # No need for else statement
        return None

    def get_profit(self, type):
        # Why do you all cost.get_total_cost if it can fail, it's called outside
        # the try statement... you're only avoiding 1 error
        try:
            cost = Cost.objects.get(client=self, type=type)
        except:
            pass
        return cost.get_total_cost()

    def get_amount_owed(self):
        # Just return the sum, no need to make a variable... super slow
        return sum(cost.amount for cost in ClientCost.objects.filter(client=self))

    def get_customer_id(self):
        return self.customer_id


class Project(models.Model):
    name = models.CharField(max_length=100, unique=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    github_link = models.URLField(blank=True, null=True)
    folder_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return str(self.name)
