from django.db import models
from django.urls import reverse
from enum import Enum
from datetime import timedelta
import stripe
# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100, unique="True")
    cost_per_hour = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name

class Cost(models.Model):
    #choices style from Two scoops of Django 1.11 best practice
    #lets you loop through choices easily
    class Meta:
        abstract = True

    class TYPES(Enum):
        elementor =  ('el', 'Elementor')
        server_hosting =  ('sh', 'Server Hosting')
        domains = ('do', 'Domains')
        project = ('pj', 'Project')
        plugin = ('pl', 'Plugin')
        theme = ('th', 'Theme')
        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

        @classmethod
        def get_label(cls, member):
            return cls[member].value[1]

    #using model managers to index data


    #another way to do choices
    BIWEEKLY = 'wk'
    MONTHLY = 'mo'
    ANNUALY = 'an'

    PAYMENT_PEROID = (
        (BIWEEKLY, 'Bi-weekly'),
        (MONTHLY, 'Monthly'),
        (ANNUALY, 'Annualy')
    )


    type = models.CharField(max_length=2, choices=[x.value for x in TYPES])
    amount = models.IntegerField(default=0)
    last_payment_date = models.DateTimeField(auto_now=True)
    payment_period = models.CharField(max_length=2, choices=PAYMENT_PEROID, default=BIWEEKLY)

    def get_next_payment(self):
        if self.payment_period == self.BIWEEKLY:
            next_payment = self.last_payment_date + timedelta(days=14)
        elif self.payment_period == self.MONTHLY:
            next_payment = self.last_payment_date + timedelta(weeks=4)
        else:
            next_payment = self.last_payment_date + timedelta(weeks=52)
        return next_payment

class ClientCost(Cost):
    client = models.ForeignKey('management.Client', on_delete=models.CASCADE)
    project = models.ForeignKey('management.Project', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.client) + ' | ' + self.type

class CompanyCost(Cost):
    company = models.ForeignKey('management.Company', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.company) + ' | ' + self.type
